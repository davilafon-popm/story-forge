# Privacy and sensitive data

story-forge reads your tickets, requirements and designs through your own connectors and session. Nothing is sent anywhere else by the plugin itself.

## What must never be committed to this repository

- Real team profiles (`*.profile.yaml` outside `profiles/examples/`).
- Company or client names, site URLs, cloud ids, project keys, page ids, design file keys.
- Real ticket keys, customer data, phone numbers, screenshots of real designs.
- Tokens, passwords or cookies of any kind.

## Safeguards

- `.gitignore` excludes real profiles and image folders.
- `tools/sanitize_check.py` scans the repository with generic patterns (tokens, emails, Atlassian/Figma ids) and with your private denylist `.sanitize-denylist` (git-ignored; one term per line, e.g. your company name). CI runs the generic scan on every pull request.
- Skills never ask for tokens in the chat; tokens live in environment variables set by the user.
- With `ai_mentions_allowed: false`, nothing written to your tools mentions AI assistance.
