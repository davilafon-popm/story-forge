#!/usr/bin/env python3
"""Scan the repository for data that must not be published.

Generic patterns run always. Private terms (company, client, site names) are
read from `.sanitize-denylist` (git-ignored), one per line, case-insensitive.

A line containing the marker `sanitize: allow` is skipped (use it only for test
fixtures that plant fake secrets on purpose).

Usage: python tools/sanitize_check.py [--root .]
Exit code 1 when something is found.
"""
import argparse
import pathlib
import re
import sys

GENERIC = {
    "atlassian site": re.compile(r"\b[a-z0-9-]+\.atlassian\.net\b", re.I),
    "atlassian cloud id": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "figma file key": re.compile(r"figma\.com/(?:design|file)/(?!EXAMPLE)[A-Za-z0-9]{15,}"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z][A-Za-z0-9-]*(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b"),
    "token-like secret": re.compile(r"\b(?:figd_|ghp_|github_pat_|xox[bpas]-|ATATT)[A-Za-z0-9_\-]{10,}"),
    "confluence page id": re.compile(r"/pages/\d{6,}"),
}
ALLOW = {"your-site.atlassian.net"}
SKIP_DIRS = {".git", "__pycache__"}
SKIP_FILES = {"LICENSE", "sanitize_check.py", ".sanitize-denylist", ".sanitize-denylist.example"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".py", ".js", ".txt", ""}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    a = p.parse_args()
    root = pathlib.Path(a.root).resolve()
    deny = []
    dl = root / ".sanitize-denylist"
    if dl.exists():
        deny = [l.strip() for l in dl.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    hits = 0
    for f in root.rglob("*"):
        if not f.is_file() or set(f.relative_to(root).parts) & SKIP_DIRS or f.name in SKIP_FILES:
            continue
        if f.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if "sanitize: allow" in line:
                continue
            for label, rx in GENERIC.items():
                for m in rx.finditer(line):
                    if m.group(0).lower() in ALLOW:
                        continue
                    hits += 1
                    print(f"{f.relative_to(root)}:{n}: {label}: {m.group(0)}")
            low = line.lower()
            for term in deny:
                if term.lower() in low:
                    hits += 1
                    print(f"{f.relative_to(root)}:{n}: denylist term: {term}")
    print(f"{hits} finding(s)")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
