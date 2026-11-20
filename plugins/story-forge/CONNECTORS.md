# Connectors

story-forge never assumes a specific product. Skills speak of a **tracker**, a **wiki**, a **design tool** and **web research**; the team profile (`story-forge.profile.yaml`) says which product, site and connector fills each role, per market. There are no placeholders to replace in the skills.

| Role | Profile fields | Used with (method predecessor) | Expected to work (needs a contributor to verify) |
|---|---|---|---|
| Tracker | `markets[].tracker` | Jira | Azure DevOps, Linear, GitHub Issues, GitLab, YouTrack |
| Wiki and knowledge base | `markets[].wiki`, `markets[].knowledge_base` | Confluence | Notion, SharePoint, Google Docs, a git repository with markdown |
| Design tool | `markets[].design` | Figma | Penpot, Sketch, Adobe XD (through exported PNGs and texts) |
| Web research | `research.web` | Built-in web search, app browser | Any web-search connector |

"Used with (method predecessor)" means the method was used in real projects with those tools before it was packaged as story-forge. See `reference/tool-adapters.md` for the operation-by-operation mapping and its verification status.

## Minimum operations per role

A connector is enough when it can do these operations. If it cannot, the skills fall back to the next strategy in the profile (for example, `manual`).

- **Tracker**: read an issue (title, description, status, parent/epic, links, subtasks); search issues; update the description of one issue; attach a file (optional, see `sf-publish`).
- **Wiki**: search pages; read a page; update a page (only for knowledge-base rules, always after approval).
- **Design tool**: read the texts of a frame/node; export a frame as PNG (optional, see `sf-design-reader`).

## Adding a tool

1. Set the product in the `tool` field of the profile.
2. Fill its column in `reference/tool-adapters.md` (operation → connector call) and, if needed, add a guide under the relevant skill's `references/`.
3. Open a pull request. Product names belong in `reference/` and `references/`, never in skill bodies.
