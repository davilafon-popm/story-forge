# Design images in the ticket without picking files

[Español](image-upload.es.md) · Added in 0.2.0

## The problem

Every story embeds one design image under each acceptance criterion. Getting the images out of the design tool was already automated, but the last step still needed a person: in many setups the Product Owner had to open a file picker and select the PNGs for every story.

That step is not a bug in a single session. The images live on disk, and the tracker needs them inside a web page or through its API. Each usual route can be closed:

- **Claude's app browser** can call the tracker from the ticket page, but it cannot put a file into a page. Only a person can choose files in the picker.
- **Tracker connectors** may not upload attachments (some connector versions only read and write text).
- **Claude's network** may not reach the tracker's API, because the organization's network allowlist does not include it. Then a script with a token cannot upload either.

## The solution: Claude in Chrome

Claude in Chrome (the browser extension) has a `file_upload` tool that loads files into a file input on a page, with no picker. story-forge 0.2.0 uses it as the first publishing strategy (`browser-extension`):

1. Claude opens the ticket in Chrome, where you are already signed in to the tracker.
2. It loads the story's PNGs into a hidden file input on the page.
3. It checks name, size and SHA-256 of every file against the originals.
4. From the same page, it uploads them with the tracker's attachments API and writes the description with each image under its criterion.
5. It verifies the ticket and removes the input.

Verified on Jira Cloud on 2026-11-25: the files arrived in the page byte-for-byte identical to the originals.

## What you need

- Claude in Chrome installed, connected and signed in to the **same organization** as your Claude conversation.
- Your tracker open in Chrome with your session (Claude never types passwords; if the session expires, it asks you to sign in).
- `browser-extension` first in `publishing.images_inline` in your team profile (the default from 0.2.0).

Good to know:

- `file_upload` accepts files from Claude's session workspace, not paths in your own folders. The image step already leaves the PNGs there; if they only exist in your folder, Claude copies them first.
- At most 3.8 MB per call. A typical screen PNG is 25–80 KB, so a whole story fits in one call.

## If you cannot use the extension

The other strategies stay available, in the order your profile sets: `api-token` (a token in an environment variable, when Claude's network reaches the tracker), `browser-session` (you pick the files), `wiki-page` and `manual`. See [the options matrix](../plugins/story-forge/reference/options-matrix.md).
