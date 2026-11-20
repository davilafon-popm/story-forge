#!/usr/bin/env python3
"""
figma_rest.py — Reads Figma through its official REST API (no MCP) and writes
a compact Markdown summary for user stories. Standard library only.

Token: environment variable FIGMA_TOKEN, or the file ~/.figma_token
       (personal access token with read-only file scope). Never paste it in a chat.

Commands (Spanish aliases kept for backward compatibility):
  flow      <link>   1 call: full node tree -> per-screen .md summary      (alias: flujo)
  images    <link>   1 call: PNG of ALL screens in the node, downloaded     (alias: imagenes)
  structure <link>   1 light call (depth=2): screens and ids                (alias: estructura)
  limits             calls made so far (local log)                          (alias: limites)

Common options:
  --refresh          ignore the cache and call again       (alias: --refrescar)
  --ttl HOURS        cache lifetime (default 72 h)
  --output DIR       output folder (default ./figma-out)    (alias: --salida)
  --include-hidden   include hidden layers                  (alias: --incluir-ocultos)

Example:
  python figma_rest.py flow "https://www.figma.com/design/AbC123/App?node-id=12-345"
  python figma_rest.py images "https://www.figma.com/design/AbC123/App?node-id=12-345" --scale 1
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

API = "https://api.figma.com/v1"
CACHE_DIR = Path(os.environ.get("FIGMA_CACHE_DIR", Path.home() / ".cache" / "figma-rest-hu"))
LOG_FILE = CACHE_DIR / "calls.log"

INPUT_HINTS = re.compile(
    r"(input|text ?field|campo|select|dropdown|combo|checkbox|check|radio|toggle|switch|"
    r"button|bot[oó]n|btn|cta|date ?picker|fecha|otp|pin|search|buscador|slider|stepper|upload|tab)",
    re.I,
)


# ----------------------------------------------------------------- utilidades
def fail(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def get_token():
    tok = os.environ.get("FIGMA_TOKEN")
    if not tok:
        p = Path.home() / ".figma_token"
        if p.exists():
            tok = p.read_text().strip()
    if not tok:
        fail(
            "Figma token not found. Set it with\n"
            "  export FIGMA_TOKEN=<your token>   (or save it in ~/.figma_token)\n"
            "Create it in Figma > Settings > Security > Personal access tokens, "
            "with read-only file content scope."
        )
    return tok


def parse_link(link):
    """Return (file_key, node_id with ':' or None, base_url)."""
    m = re.search(r"figma\.com/(?:design|file|proto|board)/([A-Za-z0-9]+)(?:/branch/([A-Za-z0-9]+))?", link)
    if not m:
        # a bare file key is accepted
        if re.fullmatch(r"[A-Za-z0-9]{10,}", link):
            return link, None, f"https://www.figma.com/design/{link}"
        fail(f"Unrecognized Figma link: {link}")
    key = m.group(2) or m.group(1)  # branches are queried directly
    q = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
    node = q.get("node-id", [None])[0]
    if node:
        node = node.replace("-", ":")
    return key, node, f"https://www.figma.com/design/{key}"


def log_call(endpoint, status):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{status}\t{endpoint}\n")


def api_get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Figma-Token": get_token()})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            log_call(path, r.status)
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log_call(path, e.code)
        body = e.read().decode("utf-8", "ignore")[:400]
        if e.code == 429:
            ra = e.headers.get("Retry-After", "?")
            tipo = e.headers.get("X-Figma-Rate-Limit-Type", "")
            plan = e.headers.get("X-Figma-Plan-Tier", "")
            fail(
                f"Figma answered 429 (rate limit). Retry-After: {ra} s. "
                f"Limit type: {tipo or 'n/a'}. Plan: {plan or 'n/a'}.\n"
                "Not retrying automatically, to save quota. "
                "Use the existing cache or wait the indicated time.",
                code=3,
            )
        if e.code in (401, 403):
            fail(f"Figma rejected the token or you have no access to the file ({e.code}). {body}", code=4)
        if e.code == 404:
            fail(f"File or node not found (404). Check the link. {body}", code=5)
        fail(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        fail(
            f"Could not reach api.figma.com ({e.reason}). "
            "In a network-restricted environment, run this script where "
            "api.figma.com is reachable (your own terminal, for example)."
        )


def cached(name, ttl_h, refresh, fetch):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    p = CACHE_DIR / name
    if p.exists() and not refresh and (time.time() - p.stat().st_mtime) < ttl_h * 3600:
        print(f"(cache) {p}", file=sys.stderr)
        return json.loads(p.read_text())
    data = fetch()
    p.write_text(json.dumps(data))
    return data


def safe(s):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)[:80]


# ------------------------------------------------------------- tree analysis
def bbox(n):
    b = n.get("absoluteBoundingBox") or {}
    return b.get("x", 0), b.get("y", 0), b.get("width", 0), b.get("height", 0)


def is_screen_like(n):
    if n.get("type") not in ("FRAME", "COMPONENT", "INSTANCE", "COMPONENT_SET"):
        return False
    _, _, w, h = bbox(n)
    return w >= 280 and h >= 400


def find_screens(root):
    """Decide which nodes are 'screens' inside the requested node."""
    t = root.get("type")
    if t in ("CANVAS", "SECTION", "GROUP", "DOCUMENT"):
        out = []
        for c in root.get("children", []):
            if c.get("type") in ("SECTION", "GROUP", "CANVAS"):
                out.extend(find_screens(c))
            elif is_screen_like(c) or c.get("type") == "FRAME":
                out.append(c)
        return out
    if t == "FRAME":
        kids = [c for c in root.get("children", []) if is_screen_like(c)]
        if len(kids) >= 2:  # container frame holding several screens
            return kids
    return [root]


def walk(n, include_hidden, depth=0):
    if not include_hidden and n.get("visible") is False:
        return
    yield n, depth
    for c in n.get("children", []) or []:
        yield from walk(c, include_hidden, depth + 1)


def screen_summary(s, id_to_name, base_url, include_hidden):
    texts, inputs, comps, inter = [], [], Counter(), []
    for n, _ in walk(s, include_hidden):
        typ = n.get("type")
        name = n.get("name", "")
        if typ == "TEXT":
            chars = (n.get("characters") or "").strip()
            if chars:
                x, y, _, _ = bbox(n)
                texts.append((round(y / 8), x, chars.replace("\n", " ⏎ ")))
        if typ == "INSTANCE":
            comps[name] += 1
            props = n.get("componentProperties") or {}
            pv = ", ".join(
                f"{k.split('#')[0]}={v.get('value')}" for k, v in props.items()
                if isinstance(v, dict) and v.get("type") in ("VARIANT", "BOOLEAN", "TEXT")
            )
            if INPUT_HINTS.search(name) and n is not s:
                label = ""
                for c, _ in walk(n, include_hidden):
                    if c.get("type") == "TEXT" and (c.get("characters") or "").strip():
                        label = c["characters"].strip().replace("\n", " ")
                        break
                inputs.append(f"{name}" + (f" — «{label}»" if label else "") + (f" [{pv}]" if pv else ""))
        for it in n.get("interactions") or []:
            trig = (it.get("trigger") or {}).get("type", "?")
            for a in it.get("actions") or []:
                if not a:
                    continue
                dest = a.get("destinationId")
                nav = a.get("navigation") or a.get("type")
                desc = f"{trig} on «{name}» → {nav}"
                if dest:
                    desc += f" «{id_to_name.get(dest, dest)}»"
                elif a.get("url"):
                    desc += f" {a['url']}"
                inter.append(desc)
        if n.get("transitionNodeID"):
            inter.append(f"click on «{name}» → «{id_to_name.get(n['transitionNodeID'], n['transitionNodeID'])}»")

    texts.sort()
    seen, lines = set(), []
    for _, _, t in texts:
        if t not in seen:
            seen.add(t)
            lines.append(t)

    _, _, w, h = bbox(s)
    link = f"{base_url}?node-id={s['id'].replace(':', '-')}"
    md = [f"## Screen: {s.get('name')}", f"- id: `{s['id']}` · {int(w)}×{int(h)} px · [open in Figma]({link})"]
    md.append("\n**Texts (reading order):**")
    md += [f"- {t}" for t in lines] or ["- (no texts)"]
    if inputs:
        md.append("\n**Detected controls / fields:**")
        md += [f"- {i}" for i in dict.fromkeys(inputs)]
    if inter:
        md.append("\n**Prototype interactions:**")
        md += [f"- {i}" for i in dict.fromkeys(inter)]
    if comps:
        md.append("\n**Components used:** " + ", ".join(f"{k} ×{v}" if v > 1 else k for k, v in comps.most_common(25)))
    return "\n".join(md)


# ------------------------------------------------------------------- commands
def fetch_node(key, node, args, depth=None):
    params = {"geometry": "omit"}
    if depth:
        params["depth"] = depth
    tag = f"{safe(key)}_{safe(node or 'root')}_d{depth or 'all'}.json"
    if node:
        params["ids"] = node
        data = cached(tag, args.ttl, args.refrescar, lambda: api_get(f"/files/{key}/nodes", params))
        entry = (data.get("nodes") or {}).get(node)
        if not entry:
            fail(f"Node {node} was not in the response. Does the link point to the right node?")
        return data.get("name", key), entry["document"]
    # no node-id: whole file (may be heavy) -> limited depth
    params["depth"] = depth or 3
    data = cached(tag, args.ttl, args.refrescar, lambda: api_get(f"/files/{key}", params))
    return data.get("name", key), data["document"]


def cmd_flujo(args):
    key, node, base = parse_link(args.link)
    fname, root = fetch_node(key, node, args)
    id_to_name = {n["id"]: n.get("name", "") for n, _ in walk(root, True)}
    screens = find_screens(root)
    out = [
        f"# Figma · {fname}",
        f"Node: {root.get('name')} (`{root.get('id')}`, {root.get('type')}) · {len(screens)} screen(s)",
        f"Source: Figma REST API · generated {time.strftime('%Y-%m-%d %H:%M')}",
        "",
        "**Screen order:** " + " → ".join(s.get("name", "?") for s in screens),
        "",
    ]
    for s in screens:
        out.append(screen_summary(s, id_to_name, base, args.incluir_ocultos))
        out.append("")
    Path(args.salida).mkdir(parents=True, exist_ok=True)
    dest = Path(args.salida) / f"{safe(key)}_{safe(node or 'root')}.md"
    dest.write_text("\n".join(out))
    ids = Path(args.salida) / f"{safe(key)}_{safe(node or 'root')}_screens.json"
    ids.write_text(json.dumps([{"id": s["id"], "name": s.get("name")} for s in screens], ensure_ascii=False, indent=1))
    print("\n".join(out))
    print(f"\n[summary saved to {dest}]", file=sys.stderr)


def cmd_estructura(args):
    key, node, base = parse_link(args.link)
    fname, root = fetch_node(key, node, args, depth=2)
    print(f"# {fname} · {root.get('name')} ({root.get('type')})")
    for c in root.get("children", []) or []:
        print(f"- {c.get('type'):10} `{c['id']}`  {c.get('name')}  {base}?node-id={c['id'].replace(':', '-')}")


def cmd_imagenes(args):
    key, node, base = parse_link(args.link)
    if args.ids:
        ids = [i.replace("-", ":") for i in args.ids.split(",")]
    else:
        _, root = fetch_node(key, node, args)
        ids = [s["id"] for s in find_screens(root)]
    if not ids:
        fail("No screens to export.")
    params = {"ids": ",".join(ids), "format": args.formato, "scale": args.escala}
    tag = f"img_{safe(key)}_{safe('_'.join(ids))[:60]}_{args.formato}_{args.escala}.json"
    # Figma image URLs expire: short cache
    data = cached(tag, min(args.ttl, 24), args.refrescar, lambda: api_get(f"/images/{key}", params))
    if data.get("err"):
        fail(f"Figma could not render: {data['err']}")
    outdir = Path(args.salida) / "screens"
    outdir.mkdir(parents=True, exist_ok=True)
    for nid, url in (data.get("images") or {}).items():
        if not url:
            print(f"- {nid}: no image (empty or invisible node)")
            continue
        f = outdir / f"{safe(key)}_{nid.replace(':', '-')}.{args.formato}"
        if not f.exists() or args.refrescar:
            urllib.request.urlretrieve(url, f)  # CDN download: not an API call
        print(f"- `{nid}` → {f}  ·  {base}?node-id={nid.replace(':', '-')}")


def cmd_limites(args):
    if not LOG_FILE.exists():
        print("No calls logged yet.")
        return
    rows = [l.split("\t") for l in LOG_FILE.read_text().splitlines() if l]
    today = time.strftime("%Y-%m-%d")
    month = time.strftime("%Y-%m")
    n_today = sum(r[0].startswith(today) for r in rows)
    n_month = sum(r[0].startswith(month) for r in rows)
    print(f"Calls today: {n_today} · this month: {n_month} · total: {len(rows)}")
    for r in rows[-10:]:
        print("  " + "  ".join(r))


def build_parser():
    p = argparse.ArgumentParser(description="Read Figma through the REST API (no MCP) to write user stories.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, link=True):
        if link:
            sp.add_argument("link", help="Figma link with node-id, or a file key")
        sp.add_argument("--refresh", "--refrescar", dest="refrescar", action="store_true", help="ignore the cache")
        sp.add_argument("--ttl", type=float, default=72, help="cache lifetime in hours")
        sp.add_argument("--output", "--salida", dest="salida", default="figma-out", help="output folder")
        sp.add_argument("--include-hidden", "--incluir-ocultos", dest="incluir_ocultos", action="store_true")

    common(sub.add_parser("flow", aliases=["flujo"]))
    common(sub.add_parser("structure", aliases=["estructura"]))
    sp = sub.add_parser("images", aliases=["imagenes"])
    common(sp)
    sp.add_argument("--ids", help="comma-separated node ids; default: every screen in the node")
    sp.add_argument("--format", "--formato", dest="formato", default="png", choices=["png", "jpg", "svg", "pdf"])
    sp.add_argument("--scale", "--escala", dest="escala", default="1")
    common(sub.add_parser("limits", aliases=["limites"]), link=False)
    return p


COMMANDS = {"flow": "cmd_flujo", "flujo": "cmd_flujo", "structure": "cmd_estructura", "estructura": "cmd_estructura",
            "images": "cmd_imagenes", "imagenes": "cmd_imagenes", "limits": "cmd_limites", "limites": "cmd_limites"}


def main(argv=None):
    args = build_parser().parse_args(argv)
    globals()[COMMANDS[args.cmd]](args)


if __name__ == "__main__":
    main()
