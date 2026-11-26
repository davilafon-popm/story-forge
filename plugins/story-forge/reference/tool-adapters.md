# Tool adapters

How each operation the skills need maps to each tool. **Used** means the mapping was used in real projects with the method predecessor of story-forge; **Verified** means it was confirmed with story-forge itself; **Expected** means the operation exists in the tool but a contributor still needs to confirm the mapping. Pull requests welcome.

## Trackers

| Operation | Jira (Used) | Azure DevOps (Expected) | Linear (Expected) | GitHub Issues (Expected) |
|---|---|---|---|---|
| Read issue with parent, links, subtasks | Atlassian connector `getJiraIssue` | Work item get with relations | Issue query with parent and children | Issue get; sub-issues |
| Search | JQL search | WIQL query | Issue filter | Search issues |
| Update description | Edit issue / REST v2 wiki markup or v3 ADF | Update work item `System.Description` (HTML) | Update issue description (markdown) | Update issue body (markdown) |
| Attach image inline | REST attachments + `!file.png!` in wiki markup; from the page with Claude in Chrome `file_upload` (Verified 2026-11-25) | Attachments API + `<img>` in HTML | File upload + markdown image | Upload via UI/API + markdown image |
| Epic / parent | Epic issue type; `parent` field | Epic/Feature work item; parent link | Project or parent issue | Milestone or parent issue |

## Wikis and knowledge bases

| Operation | Confluence (Used) | Notion (Expected) | SharePoint (Expected) | Git repo (Expected) |
|---|---|---|---|---|
| Search page | CQL search | Search | Search | File search |
| Read page | Get page (storage/HTML/markdown) | Fetch page | Get page/file | Read file |
| Update rule table | Update page keeping the rest of the body | Update block | Update file | Commit + pull request |

## Design tools

See `../skills/sf-design-reader/references/`.

## Contributing an adapter

1. Fill the column for your tool with the connector's real operation names.
2. Add any special formatting rules (e.g., how images are embedded).
3. Note limits and permissions that trigger a fallback.
4. Mark the column "Verified" only after using it with story-forge on real tickets.
