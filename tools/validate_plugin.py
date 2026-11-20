#!/usr/bin/env python3
"""Validate the plugin structure: manifests, skill and agent frontmatter."""
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

root = pathlib.Path(__file__).resolve().parents[1]
plugin = root / "plugins" / "story-forge"
errors = []

for mf in [root / ".claude-plugin" / "marketplace.json", plugin / ".claude-plugin" / "plugin.json"]:
    try:
        data = json.loads(mf.read_text(encoding="utf-8"))
        if not re.fullmatch(r"[a-z0-9-]+", data.get("name", "")):
            errors.append(f"{mf}: name must be kebab-case")
    except Exception as e:
        errors.append(f"{mf}: {e}")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    return yaml.safe_load(text.split("---\n", 2)[1])


for skill in sorted((plugin / "skills").iterdir()):
    f = skill / "SKILL.md"
    try:
        fm = frontmatter(f)
        if fm.get("name") != skill.name:
            errors.append(f"{f}: name '{fm.get('name')}' != folder '{skill.name}'")
        d = fm.get("description", "")
        if not d or len(d) > 1024:
            errors.append(f"{f}: description missing or over 1024 characters ({len(d)})")
    except Exception as e:
        errors.append(f"{f}: {e}")

for agent in sorted((plugin / "agents").glob("*.md")):
    try:
        fm = frontmatter(agent)
        for k in ("name", "description", "model", "color"):
            if k not in fm:
                errors.append(f"{agent}: missing {k}")
        if fm.get("model") not in ("inherit", "haiku", "sonnet", "opus"):
            errors.append(f"{agent}: invalid model {fm.get('model')}")
    except Exception as e:
        errors.append(f"{agent}: {e}")

for y in list(root.rglob("*.yaml")):
    try:
        yaml.safe_load(y.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{y}: {e}")

print("\n".join(errors) if errors else "plugin OK")
sys.exit(1 if errors else 0)
