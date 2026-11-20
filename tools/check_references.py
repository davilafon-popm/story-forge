#!/usr/bin/env python3
"""Check that every file path mentioned in skills, agents and reference docs exists.

Skills and agents state that their paths are relative to the plugin root, so
backticked paths that start with a known plugin folder are resolved there.
Relative markdown links in every .md file are resolved from the file itself.
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
plugin = root / "plugins" / "story-forge"
PLUGIN_DIRS = ("templates/", "knowledge-base/", "reference/", "skills/", "agents/")
errors = []

code_path = re.compile(r"`((?:templates|knowledge-base|reference|skills|agents)/[^`\s<>{}*]+)`")
for f in list(plugin.rglob("*.md")):
    text = f.read_text(encoding="utf-8")
    for m in code_path.finditer(text):
        target = m.group(1).rstrip(".,;:)")
        if not (plugin / target).exists():
            errors.append(f"{f.relative_to(root)}: `{target}` not found under plugins/story-forge/")

md_link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
for f in root.rglob("*.md"):
    if ".git" in f.parts:
        continue
    for m in md_link.finditer(f.read_text(encoding="utf-8")):
        t = m.group(1)
        if re.match(r"[a-z]+:", t):
            continue
        if not (f.parent / t).exists():
            errors.append(f"{f.relative_to(root)}: link to {t} is broken")

print("\n".join(errors) if errors else "references OK")
sys.exit(1 if errors else 0)
