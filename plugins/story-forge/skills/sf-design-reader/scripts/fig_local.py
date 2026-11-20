#!/usr/bin/env python3
"""
fig_local.py — Reads a local Figma .fig file (File › Save local copy) OFFLINE,
without using Figma API or connector quota, and writes a per-screen summary
for user stories.

Uses the fig2sketch decoder (MIT license), installed separately:
    pip install fig2sketch          # provides the figformat module

Commands (Spanish aliases kept for backward compatibility):
  structure <file.fig> [--node 123-456]          pages, or children of a node   (alias: estructura)
  flow      <file.fig> --node 123-456             markdown summary of a flow     (alias: flujo)
Options: --file-key KEY (to build Figma links), --output DIR, --include-hidden, --group TEXT

The first run decodes the file (1-2 min for large files) and leaves a reduced
JSON cache next to the summary; later runs are immediate. The cache is plain
JSON (never pickle), so a shared or downloaded cache cannot execute code.

Note: .fig is an unofficial format. Check that reading it is allowed by the
vendor's terms and your organization's policies.
"""
import argparse
import gc
import gzip
import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

UINT_MAX = 4294967295
KEEP = {"guid", "type", "name", "visible", "size", "transform", "parentIndex", "textData", "symbolData",
        "prototypeInteractions", "prototypeStartingPoint", "overrideKey", "componentPropAssignments",
        "componentPropRefs", "internalOnly", "phase", "isStateGroup", "connectorStart", "connectorEnd",
        "connectorText"}
OV_KEEP = ("textData", "overriddenSymbolID", "visible", "prototypeInteractions", "componentPropAssignments")
JUNK = re.compile(r"[\ud800-\udfff\ue000-\uf8ff\U000f0000-\U0010ffff]")
NOISE = re.compile(r"(^|[ /(])(battery|status|statusbar|status bar|face|eyes|nose|eyebrows|mouth|hair|"
                   r"woman-face|man-face|home indicator|keyboard|teclado)", re.I)
INPUT_HINTS = re.compile(r"(input|text ?field|campo|select|dropdown|combo|checkbox|check|radio|toggle|switch|"
                         r"button|bot[oó]n|btn|cta|date|fecha|otp|pin|search|buscador|slider|stepper|upload|tab|link)", re.I)


def fail(m):
    print("ERROR: " + m, file=sys.stderr); sys.exit(1)


def g(x):
    if x is None: return None
    if isinstance(x, dict): return (x["sessionID"], x["localID"])
    return tuple(x)


def clean(s):
    return JUNK.sub("", s or "").replace("\u2028", " ").strip()


# ------------------------------------------------------------ decoding
def load(path, outdir):
    st = os.stat(path)
    tag = hashlib.md5(f"{Path(path).name}{st.st_size}{st.st_mtime}".encode()).hexdigest()[:10]
    cache = Path(outdir) / f".cache_{tag}.json.gz"
    if cache.exists():
        return load_cache(cache)
    try:
        from figformat import decodefig  # pip install fig2sketch
    except ImportError:
        fail("fig2sketch is missing. Install it with: pip install fig2sketch")
    print(f"Decoding {Path(path).name} (may take 1-2 min)…", file=sys.stderr)
    t = time.time()
    fig, _ = decodefig.decode(path)
    nodes = fig["nodeChanges"]; fig.clear(); gc.collect()
    slim = []
    for i in range(len(nodes)):
        n = nodes[i]; nodes[i] = None
        if n.get("phase") == "REMOVED": continue
        d = {k: v for k, v in n.items() if k in KEEP}
        if "textData" in d: d["textData"] = {"characters": d["textData"].get("characters", "")}
        sd = d.get("symbolData")
        if sd:
            ov = []
            for o in sd.get("symbolOverrides") or []:
                oo = {"guidPath": [g(x) for x in o["guidPath"]["guids"]]}
                for k in OV_KEEP:
                    if k in o: oo[k] = {"characters": o[k].get("characters", "")} if k == "textData" else o[k]
                if len(oo) > 1: ov.append(oo)
            d["symbolData"] = {"symbolID": g(sd.get("symbolID")), "symbolOverrides": ov}
        slim.append(d)
    del nodes; gc.collect()
    Path(outdir).mkdir(parents=True, exist_ok=True)
    save_cache(slim, cache)
    print(f"Done in {time.time()-t:.0f} s · {len(slim)} nodes · cache {cache}", file=sys.stderr)
    return slim


def _json_default(o):
    if isinstance(o, (bytes, bytearray)):
        return None  # binary blobs are not needed for summaries
    if isinstance(o, (set, frozenset)):
        return list(o)
    return str(o)


def save_cache(slim, cache):
    with gzip.open(cache, "wt", encoding="utf-8") as f:
        json.dump(slim, f, default=_json_default)


def load_cache(cache):
    """Load the JSON cache and restore tuples where the walker needs hashable keys."""
    with gzip.open(cache, "rt", encoding="utf-8") as f:
        slim = json.load(f)
    for d in slim:
        sd = d.get("symbolData")
        if sd:
            if sd.get("symbolID") is not None:
                sd["symbolID"] = tuple(sd["symbolID"])
            for o in sd.get("symbolOverrides") or []:
                o["guidPath"] = [tuple(x) for x in o["guidPath"]]
    return slim


class Doc:
    def __init__(self, nodes):
        self.by = {}; self.kids = defaultdict(list); self.canon = {}
        for n in nodes:
            gid = g(n["guid"]); self.by[gid] = n
            ok = g(n.get("overrideKey"))
            key = ok if ok and ok[0] != UINT_MAX else gid
            self.canon[gid] = key
            if ok and ok[0] != UINT_MAX: self.by.setdefault(ok, n)
        for n in nodes:
            p = n.get("parentIndex")
            if p: self.kids[g(p["guid"])].append((p["position"], g(n["guid"])))
        for k in self.kids: self.kids[k].sort()
        self.root = next(g(n["guid"]) for n in nodes if n["type"] == "DOCUMENT")

    def children(self, gid): return [self.by[c] for _, c in self.kids.get(gid, [])]
    def key(self, n): return self.canon[g(n["guid"])]
    def parent(self, n):
        p = n.get("parentIndex"); return self.by.get(g(p["guid"])) if p else None

    def comp_name(self, sym):
        if not sym: return "?"
        par = self.parent(sym)
        if par and (par.get("isStateGroup") or par["type"] in ("FRAME", "SYMBOL")) and "=" in sym["name"]:
            return f"{par['name']} ({sym['name']})"
        return sym["name"]


def pos(n):
    t = n.get("transform")
    return (t[0][2], t[1][2]) if t else (0, 0)


# -------------------------------------------------------------- traversal
def walk(doc, n, ox, oy, ctx, out, inc_hidden, path=None, ov=None, props=None):
    """ctx: None outside instances. path: tuple of keys inside the root instance."""
    x, y = pos(n); ax, ay = ox + x, oy + y
    o = {}
    me = None
    if path is not None:
        me = path + (doc.key(n),)          # guidPath = nested instances + final node
        o = ov.get(me, {})
    vis = o.get("visible", n.get("visible", True))
    for r in n.get("componentPropRefs") or []:
        if r.get("componentPropNodeField") == "VISIBLE" and props and g(r["defID"]) in props:
            v = props[g(r["defID"])].get("boolValue")
            if v is not None: vis = v
    if vis is False and not inc_hidden:
        return
    typ = n["type"]
    for it in (o.get("prototypeInteractions") or n.get("prototypeInteractions") or []):
        if it.get("isDeleted"): continue
        for a in it.get("actions") or []:
            dest = g(a.get("transitionNodeID"))
            out["inter"].append((n.get("name", ""), (it.get("event") or {}).get("interactionType", "?"),
                                 a.get("navigationType") or a.get("connectionType"), dest))
    if typ == "TEXT":
        txt = None
        if "textData" in o: txt = o["textData"]["characters"]
        for r in n.get("componentPropRefs") or []:
            if r.get("componentPropNodeField") == "TEXT_DATA" and props and g(r["defID"]) in props:
                tv = props[g(r["defID"])].get("textValue")
                if tv: txt = tv.get("characters", txt)
        if txt is None: txt = (n.get("textData") or {}).get("characters", "")
        txt = clean(txt)
        if txt and not re.fullmatch(r"\d{1,2}:\d{2}", txt): out["texts"].append((round(ay / 8), ax, txt))
        return
    if typ == "INSTANCE":
        sd = n.get("symbolData") or {}
        sid = g(o.get("overriddenSymbolID")) or sd.get("symbolID")
        sym = doc.by.get(sid)
        cname = doc.comp_name(sym)
        base = me if me is not None else ()
        if NOISE.search(cname): return
        nov = dict(ov or {})
        for so in sd.get("symbolOverrides") or []:
            k = base + tuple(so["guidPath"])
            cur = nov.setdefault(k, {})
            for f, v in so.items():
                if f != "guidPath": cur.setdefault(f, v)
        nprops = {}
        for a in (o.get("componentPropAssignments") or []) + (n.get("componentPropAssignments") or []):
            nprops.setdefault(g(a["defID"]), a.get("value", {}))
        lab = []
        sub = {"texts": lab, "inter": out["inter"], "comps": out["comps"], "ctrls": out["ctrls"]}
        if sym:
            for c in doc.children(g(sym["guid"])):
                walk(doc, c, ax, ay, True, sub, inc_hidden, base, nov, nprops)
        out["texts"].extend(lab)
        out["comps"][cname] = out["comps"].get(cname, 0) + 1
        if INPUT_HINTS.search(cname) or INPUT_HINTS.search(n.get("name", "")):
            first = next((t for _, _, t in sorted(lab)), "")
            out["ctrls"].append((round(ay / 8), ax, cname + (f" — «{first[:80]}»" if first else "")))
        return
    for c in doc.children(g(n["guid"])):
        walk(doc, c, ax, ay, ctx, out, inc_hidden, path, ov, props)


def abs_pos(doc, n):
    x = y = 0
    while n and n["type"] not in ("CANVAS", "DOCUMENT"):
        a, b = pos(n); x += a; y += b; n = doc.parent(n)
    return x, y


def collect(doc, n, group=""):
    """Return screens [(group, node)], notes and connectors inside n."""
    screens, notes, conns = [], [], []
    for c in doc.children(g(n["guid"])):
        t = c["type"]; s = c.get("size") or {}
        if c.get("visible") is False: continue
        if t == "SECTION":
            a, b, d = collect(doc, c, (group + " › " if group else "") + c["name"])
            screens += a; notes += b; conns += d
        elif t == "CONNECTOR":
            conns.append(c)
        elif c["name"].strip().lower() in ("note", "nota", "notes", "notas"):
            notes.append((group, c))
        elif t in ("FRAME", "INSTANCE", "SYMBOL") and s.get("x", 0) >= 280 and s.get("y", 0) >= 400 and s.get("x", 0) <= 2000:
            screens.append((group, c))
    return screens, notes, conns


def link(fk, gid):
    return f"https://www.figma.com/design/{fk}?node-id={gid[0]}-{gid[1]}" if fk else ""


def cmd_flow(a):
    doc = Doc(load(a.file, a.output))
    nid = tuple(int(v) for v in re.split("[-:]", a.node))
    root = doc.by.get(nid) or fail(f"Node {a.node} not found in the file.")
    screens, notes, conns = collect(doc, root)
    if a.group:
        q = a.group.lower()
        screens = [x for x in screens if q in x[0].lower()]
        notes = [x for x in notes if q in x[0].lower()]
        if not screens: fail(f"No group contains «{a.group}». Run 'structure --node' to list the groups.")
    if not screens and root["type"] in ("FRAME", "INSTANCE"): screens = [("", root)]
    ap = {g(s["guid"]): abs_pos(doc, s) for _, s in screens}
    # order: by group position, then left→right, top→bottom
    screens.sort(key=lambda gs: (round(ap[g(gs[1]["guid"])][1] / 3000), ap[g(gs[1]["guid"])][0]))
    page = root
    while page and page["type"] != "CANVAS": page = doc.parent(page)
    md = [f"# Design summary (local file) · {Path(a.file).stem}",
          f"Page: {page['name'].strip() if page else '?'} · Node: {root['name']} (`{nid[0]}:{nid[1]}`, {root['type']})",
          f"{len(screens)} screens · {len(notes)} designer notes · {len(conns)} connectors · generated {time.strftime('%Y-%m-%d %H:%M')}",
          "Source: offline reading of the .fig file (no API calls).", ""]
    labels = {}; outs = {}
    for i, (_grp, s) in enumerate(screens, 1):
        out = {"texts": [], "inter": [], "comps": {}, "ctrls": []}
        if s["type"] == "INSTANCE":
            walk(doc, s, -pos(s)[0], -pos(s)[1], None, out, a.include_hidden)
        else:
            for c in doc.children(g(s["guid"])):
                walk(doc, c, 0, 0, None, out, a.include_hidden)
        outs[g(s["guid"])] = out
        nm = s["name"].strip()
        if not nm.strip(" .") or re.fullmatch(r"(frame|screen|pantalla)\s*\d*", nm, re.I):
            tx = [t for _, _, t in sorted(out["texts"]) if len(t) > 3]
            nm = f"«{tx[1] if len(tx) > 1 else (tx[0] if tx else 'no texts')}»"[:70]
        labels[g(s["guid"])] = f"P{i} {nm}"
    def lbl(gid):
        if gid in labels: return labels[gid]
        n = doc.by.get(gid)
        while n and g(n["guid"]) not in labels: n = doc.parent(n)
        if n: return labels[g(n["guid"])]
        n = doc.by.get(gid)
        if not n: return str(gid)
        if n["name"].strip().lower() in ("note", "nota"):
            o = {"texts": [], "inter": [], "comps": {}, "ctrls": []}; walk(doc, n, 0, 0, None, o, False)
            t = " ".join(x for _, _, x in sorted(o["texts"])); return f"Note «{t[:60]}…»"
        if n["type"] in ("SECTION",): return f"Section {n['name']}"
        return f"[{n['type'].lower()} {n['name']}]"
    # connectors
    flow = []
    for c in conns:
        s = g((c.get("connectorStart") or {}).get("endpointNodeID")); e = g((c.get("connectorEnd") or {}).get("endpointNodeID"))
        txt = clean((c.get("connectorText") or {}).get("characters", "")) if isinstance(c.get("connectorText"), dict) else ""
        if s and e: flow.append(f"{lbl(s)} → {lbl(e)}" + (f" ({txt})" if txt else ""))
    if flow:
        md += ["**Drawn flow connectors:**"] + [f"- {f}" for f in dict.fromkeys(flow)] + [""]
    if notes:
        md.append("**Designer notes:**")
        for grp, nt in sorted(notes, key=lambda gn: abs_pos(doc, gn[1])[::-1]):
            out = {"texts": [], "inter": [], "comps": {}, "ctrls": []}
            walk(doc, nt, 0, 0, None, out, a.include_hidden)
            t = " / ".join(x for _, _, x in sorted(out["texts"]))
            if t: md.append(f"- {('['+grp+'] ') if grp else ''}{t}")
        md.append("")
    md.append("**Screen index:**")
    lastg = object()
    for grp, s in screens:
        if grp != lastg: md.append(f"- _{grp or 'root'}_:"); lastg = grp
        md[-1] += f" {labels[g(s['guid'])]} ·"
    md.append("")
    last = None
    for grp, s in screens:
        if grp != last:
            md.append(f"\n## Group: {grp or '(node root)'}\n"); last = grp
        out = outs[g(s["guid"])]
        gid = g(s["guid"]); sz = s.get("size") or {}
        md.append(f"### {labels[gid]}")
        meta = f"- id `{gid[0]}:{gid[1]}` · {int(sz.get('x',0))}×{int(sz.get('y',0))}"
        if s["type"] == "INSTANCE": meta += f" · component: {doc.comp_name(doc.by.get((s.get('symbolData') or {}).get('symbolID')))}"
        if a.file_key: meta += f" · [open]({link(a.file_key, gid)})"
        md.append(meta)
        seen = []
        for _, _, t in sorted(out["texts"]):
            if t not in seen: seen.append(t)
        md.append("- **Texts:** " + (" | ".join(seen) if seen else "(no texts)"))
        ctr = list(dict.fromkeys(c for _, _, c in sorted(out["ctrls"])))
        if ctr: md.append("- **Controls:** " + "; ".join(ctr))
        inter = list(dict.fromkeys(f"{w} ({ev}) → {lbl(d) if d else nav}" for w, ev, nav, d in out["inter"]))
        if inter: md.append("- **Navigation:** " + "; ".join(inter))
        top = sorted(out["comps"].items(), key=lambda kv: -kv[1])[:12]
        top = [kv for kv in top if not re.match(r"icons? ", kv[0])][:8]
        if top: md.append("- Components: " + ", ".join(f"{k}×{v}" if v > 1 else k for k, v in top))
    Path(a.output).mkdir(parents=True, exist_ok=True)
    suf = ("_" + re.sub(r"\W+", "-", a.group.lower())) if a.group else ""
    dest = Path(a.output) / f"{Path(a.file).stem}_{nid[0]}-{nid[1]}{suf}.md"
    dest.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md)); print(f"\n[summary saved to {dest}]", file=sys.stderr)


def cmd_structure(a):
    doc = Doc(load(a.file, a.output))
    if a.node:
        nid = tuple(int(v) for v in re.split("[-:]", a.node)); base = doc.by.get(nid) or fail("node not found")
    else:
        base = doc.by[doc.root]
    print(f"# {base['name']} ({base['type']})")
    for c in doc.children(g(base["guid"])):
        if c.get("internalOnly"): continue
        gid = g(c["guid"]); sz = c.get("size") or {}
        size = f"{int(sz.get('x', 0))}×{int(sz.get('y', 0))}"
        print(f"- {c['type']:9} `{gid[0]}-{gid[1]}` {c['name'].strip()!r}  {size}  children={len(doc.kids.get(gid, []))}")


COMMANDS = {"flow": ("flujo", cmd_flow), "structure": ("estructura", cmd_structure)}


def build_parser():
    p = argparse.ArgumentParser(description="Read a local .fig file (no API calls) to write user stories.")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, (alias, _) in COMMANDS.items():
        sp = sub.add_parser(name, aliases=[alias])
        sp.add_argument("file", help="path to the .fig file")
        sp.add_argument("--node", "--nodo", dest="node", required=(name == "flow"), help="node id, e.g. 123-456")
        sp.add_argument("--file-key", default="", help="file key of the ORIGINAL file, to build links")
        sp.add_argument("--output", "--salida", dest="output", default="figma-out", help="output and cache folder")
        sp.add_argument("--include-hidden", "--incluir-ocultos", dest="include_hidden", action="store_true")
        sp.add_argument("--group", "--grupo", dest="group", default="", help="only screens in sections whose name contains this text")
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    cmd = {k: fn for k, (alias, fn) in COMMANDS.items()} | {alias: fn for k, (alias, fn) in COMMANDS.items()}
    cmd[a.cmd](a)


if __name__ == "__main__":
    main()
