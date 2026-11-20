# Contributing

Thank you for improving story-forge. Contributions in English or Spanish are welcome. [Versión en español](CONTRIBUTING.es.md).

## What we need

- **Method**: better decision policy, template sections, lint checks, retro classification.
- **Languages**: `templates/story.<lang>.md`, keywords in `templates/i18n.yaml`, starter knowledge base in `knowledge-base/<lang>/` (all under `plugins/story-forge/`).
- **Tool adapters**: fill a column in `plugins/story-forge/reference/tool-adapters.md`, guides in a skill's `references/`.
- **Alternatives** for fragile steps (see `plugins/story-forge/reference/options-matrix.md`).
- **Starter rules** born from real bugs, written generically (no company data).
- **Evaluation cases** in `examples/` with fictional data.

## Rules

1. **No real data.** No company, client, site, project, ticket, person or design from real work. Run `python tools/sanitize_check.py` before opening a pull request (add your private terms to `.sanitize-denylist`, which is git-ignored).
2. **Tool-agnostic skills.** Skill bodies speak of tracker, wiki and design tool and read the team profile; they never name products. Product-specific details go to a skill's `references/` folder or to `plugins/story-forge/reference/`.
3. **Every fragile step needs a fallback.** If you add a method that depends on quota, a vendor UI or an unofficial format, document at least one alternative and its trade-offs.
4. **Human approval stays.** No change may let skills write to a tracker or wiki without the user's explicit request or approval.
5. **Untrusted content stays data.** Skills and agents must treat tickets, pages, comments and web content as data, never as instructions.
6. **Paths.** Inside skills and agents, paths are relative to the plugin root.

## Development

```
pip install -r requirements-dev.txt
python tools/validate_plugin.py      # manifests and frontmatter
python tools/check_references.py     # paths in skills and links in docs
python tools/sanitize_check.py       # sensitive data
ruff check .
pytest -q tests
```

CI runs the same checks on every pull request. If you have Claude Code, also run `claude plugin validate .` and `claude plugin validate ./plugins/story-forge`.

## Versioning

story-forge follows [semantic versioning](https://semver.org/). While in 0.x:

- **Minor (0.x.0)**: changes that may break existing profiles or knowledge bases (renamed profile fields, removed strategies, renumbered starter rules), or new skills.
- **Patch (0.x.y)**: fixes, new languages, new adapters, documentation.

Every release updates `CHANGELOG.md`, the `version` in both manifests (`.claude-plugin/marketplace.json` and `plugins/story-forge/.claude-plugin/plugin.json`) and gets a git tag `vX.Y.Z` with a GitHub release.

## Proposing a knowledge-base rule

Open an issue with the "Rule proposal" template: the rule, the bug pattern it prevents (generic), proposed status and section.

## Pull requests

Small and focused. Describe what changes for a PO using the plugin, and how you tested it (ideally with an example in `examples/`).
