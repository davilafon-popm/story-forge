# Security policy

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's private reporting: **Security → Report a vulnerability** in this repository. You will get an answer within 7 days.

Examples of what to report:

- A skill or agent that could write to a tracker or wiki without the user's explicit request or approval.
- Instructions inside tickets, pages or design notes that the skills would follow (prompt injection).
- A script that could leak tokens, execute untrusted data or send data to a third party.
- Sensitive data committed to the repository.

## Supported versions

Only the latest release receives fixes while the project is in 0.x.

## Design choices that matter for security

- Tokens live in environment variables set by the user; skills never ask for them in the chat.
- Caches are plain JSON, never pickle.
- Every write to the tracker or the knowledge base needs the user's explicit request or approval.
- Content read from tickets, pages, comments and the web is treated as data, not instructions.
