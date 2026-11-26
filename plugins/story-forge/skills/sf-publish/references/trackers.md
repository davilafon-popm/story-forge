# Tracker notes for inline images

How to embed one image under each criterion, per tracker. Add yours with a pull request and fill its column in `reference/tool-adapters.md`.

- **Jira (Cloud)**: with `browser-extension`, run these calls from the ticket page in Chrome, using the files that `file_upload` loaded into the injected input (`FormData` with `file`). Attachments via `POST /rest/api/3/issue/{key}/attachments` with header `X-Atlassian-Token: no-check`; the simplest inline embedding is writing the description in wiki markup via `PUT /rest/api/2/issue/{key}` with `!NN-description.png|width=900!` under each "Visual reference:" line. In wiki markup: bold `*text*`, bullets `* `, escape `\[ \]`, and remove stray `*`. Verify with `GET /rest/api/3/issue/{key}?fields=description,attachment` that there is one `mediaSingle` per image. To edit an existing description without losing format, modify the ADF text nodes and `PUT` v3.
- **Azure DevOps**: upload with the attachments API, then reference the returned URL in the work item's HTML description under each criterion.
- **GitHub / GitLab issues**: upload through the web UI or API and embed the returned image URLs in markdown.
- **Linear and others**: use the connector's attachment or image upload operation, then embed the returned URL in the description.
