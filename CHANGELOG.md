# Changelog

All notable changes are listed here. Versioning policy: see [CONTRIBUTING.md](CONTRIBUTING.md#versioning).

## 0.2.0 — 2026-11-26

### Added

- **Images into the ticket without picking files.** New first publishing strategy `browser-extension`: Claude in Chrome loads the story's PNGs into the ticket page with its `file_upload` tool, checks name, size and SHA-256 against the originals, then uploads and embeds them from the same page. Verified on Jira Cloud (2026-11-25). Explained in [docs/image-upload.md](docs/image-upload.md) ([español](docs/image-upload.es.md)).
- GOVERNANCE.md and GOVERNANCE.es.md: the method is maintained upstream by its author; each Product Owner can change their own implementation unless their organization does not allow it.
- Profile section `governance` (`kb_changes: po | organization`, `approver`), asked by sf-setup and applied by sf-retro.

### Changed

- Default order of `publishing.images_inline`: `browser-extension`, `api-token`, `browser-session`, `wiki-page`, `manual`. `browser-session` (the user picks files) is now a fallback. sf-publish, the tracker-publisher agent, the Jira tracker notes, the options matrix (reviewed 2026-11-26), the tool adapters and the getting-started guides were updated.
- Install instructions: one-step `/plugin install story-forge --marketplace davilafon-popm/story-forge` (Claude Code 2.1.275+), two-step fallback kept; removed the private-repository note. Install from the public repository verified with the Claude Code CLI (marketplace and plugin manifests validate; 10 skills and 7 agents load).
- Rules are cited by name instead of numeric codes (R1.3, H1). Knowledge-base tables have a "Name" column; skills, templates, examples and the lint check use names.

## 0.1.0 — 2026-11-20

First release.

### Method and plugin

- Skills: sf-setup, sf-workflow, sf-precheck, sf-write-story, sf-backlog, sf-design-reader, sf-lint, sf-publish, sf-research, sf-retro.
- Subagents with per-role model routing (profile overrides each agent's default): sources-reader, screen-exporter, story-writer, story-reviewer, tracker-publisher, bug-classifier, web-researcher.
- Team profile with ordered fallback strategies for design texts, design images, inline images in the tracker and web research.
- Templates and Given/When/Then keywords for Spanish and English (keywords also for Portuguese and French).
- Starter knowledge base (writing rules H1–H11, standard behaviors R1–R10) in Spanish and English.
- Reference inside the plugin: options matrix (with sources and review date) and tool adapters.
- Every skill and agent treats tickets, pages, comments and web content as data, never as instructions.

### Design scripts

- `fig_local.py` (local .fig reader), `figma_rest.py` (REST client with cache), `browser_export_helpers.js` (browser export), `decode_captures.py` (capture decoder and contact sheet).
- English commands and messages, with the original Spanish names kept as aliases.
- `fig_local.py` cache is gzipped JSON (no pickle).

### Repository

- Tests (pytest), reference and link checker, sensitive-data scan, plugin validation, ruff and JavaScript syntax check in CI with read-only permissions; Dependabot.
- Fictional evaluation cases in Spanish and English with a pass/fail checklist.
- SECURITY, CODE_OF_CONDUCT, CODEOWNERS, issue templates, CONTRIBUTING in English and Spanish, disclaimer.
