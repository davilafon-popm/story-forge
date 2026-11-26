# Options matrix: alternatives for every fragile step

**Last reviewed:** 2026-11-26. Vendors change quotas, permissions and interfaces often: check the sources below before relying on a limit, and send a pull request when something changed.

Every step that depends on quotas, permissions, a vendor's UI or an unofficial format has at least two alternatives. Teams choose and order them in their profile; skills fall back automatically to the next option.

Legend — **Robustness**: how likely it keeps working over time. **Cost**: quota, money or people's time.

## 1. Reading design texts (`design.read_text`)

| Option | Robustness | Cost | Needs | Breaks when | Choose it if |
|---|---|---|---|---|---|
| `local-file` | Medium | None | A local copy of the design file with original ids; decoder library | The vendor changes its file format | Quota is scarce and you write many stories |
| `official-connector` | High | Quota | Connector enabled and a seat with access | Quota runs out | You have a paid seat with enough quota |
| `rest-api` | High | Quota | Token in an environment variable | Token expires; limits for viewer seats | You want scripted, cached reads |
| `manual` | Very high | User time | Nothing | Never | Nothing else is available |

## 2. Screen images (`design.images`)

| Option | Robustness | Cost | Needs | Breaks when | Choose it if |
|---|---|---|---|---|---|
| `official-connector` | High | Quota | Connector with export/screenshot | Quota runs out | Quota is available |
| `rest-api` | High | Quota | Token | Token or limits | Batch exports with cache |
| `browser-export` | Low–medium | None | App browser, user signed in | The vendor's web UI changes (selectors, labels) | No quota and the PO has export rights |
| `designer-export` | Very high | Designer time | A folder of PNGs named by screen | Never | Stable teams with a designer in the loop |
| `none` | Very high | None | — | Never | Images are not required; criteria link to design nodes |

## 3. Images inside the tracker (`publishing.images_inline`)

| Option | Robustness | Cost | Needs | Breaks when | Choose it if |
|---|---|---|---|---|---|
| `browser-extension` | Medium–high | None | Claude in Chrome connected to the same organization; tracker session in Chrome; images in the session workspace | Extension disconnected or signed out of the tracker | Default: zero clicks, no tokens, no network allowlist. Verified on Jira Cloud (2026-11-25) |
| `api-token` | High | None | Token with write scope in env; network allowlist reaching the tracker | Token expires, policy forbids tokens, or the network blocks the tracker | You can create a personal token and Claude's network reaches the tracker |
| `browser-session` | Medium | User clicks every story | App browser, signed in; user selects files | Same-origin API blocked; UI changes | Fallback when the extension is not connected |
| `wiki-page` | High | Two places to sync | Wiki write access | Never | Tracker blocks attachments |
| `manual` | Very high | User time | — | Never | Last resort |

## 4. External research (`research.web`)

| Option | Robustness | Cost | Needs | Choose it if |
|---|---|---|---|---|
| `native` | High | Low | Admin enables web search for the organization | Available in your plan |
| `search-connector` | High | Varies | A search MCP | Your org prefers a specific search provider |
| `browser` | Medium | None | App browser; public search pages | Native search is disabled |
| `off` | — | — | — | Research is not allowed |

## 5. Knowledge base storage (`knowledge_base.storage`)

| Option | Pros | Cons |
|---|---|---|
| `wiki` | Where business people already read; comments and history | Tied to a wiki vendor; edits through connectors |
| `repo` | Versioned, reviewable by pull request, vendor-neutral, works offline | Business readers need access to the repo or a rendered site |

## 6. Subagents and model routing (`agents`)

| Option | Pros | Cons |
|---|---|---|
| Enabled (default routing) | Long reads and mechanical loops out of the main context; cheaper models where quality is equal; parallel steps | Each subagent starts cold; handoffs must be precise |
| Enabled, custom routing | Tune cost vs. quality per team (e.g., Opus for drafting on regulated products) | Needs measuring (see usage log in sf-workflow) |
| Disabled | Simplest; works in any surface | Everything consumes the main model's context and cost |

## 7. Market separation

| Option | When |
|---|---|
| One market | Single product/country |
| Several markets, separate knowledge bases (default) | Different regulations, data or teams per country/brand |
| Several markets sharing writing rules, separate behaviors | Same team, different products — point `writing_rules` to the same page/file on purpose |

## Sources

Opened and checked on 2026-11-20.

- Figma REST API rate limits (updated limits in effect since 2025-11-17; Figma may change them): [developers.figma.com/docs/rest-api/rate-limits](https://developers.figma.com/docs/rest-api/rate-limits/)
- Jira Cloud REST API v3, issue attachments: [developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/)
- Azure DevOps Work Item Tracking, Attachments – Create (chunked upload above 130 MB): [learn.microsoft.com/…/wit/attachments/create](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/attachments/create)
- Claude Code plugin marketplaces (`marketplace.json` requires a name, an owner and a plugins array; private repositories supported): [code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

Statements about Penpot, Sketch and Adobe XD are general knowledge that still needs a contributor to confirm with each vendor's documentation.
