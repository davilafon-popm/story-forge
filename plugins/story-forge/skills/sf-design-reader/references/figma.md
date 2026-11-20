# Figma guide

> **Before using the local-file or browser-export strategies:** they read Figma's unofficial file format and automate Figma's web interface. Check that this is allowed by Figma's terms and your organization's policies; prefer the official connector or REST API when they are available to you. story-forge is not affiliated with Figma.

Scripts are in `skills/sf-design-reader/scripts/` (paths relative to the plugin root). Commands and options are in English; the original Spanish names still work as aliases.

## Local file (`local-file`)

**How the user gets it:** in Figma, File › Save local copy. Needs edit permission or a file that allows viewers to copy; otherwise duplicate the file to an own team and export from there. For a huge file, copy only the flow's screens to a new file and export that (but then node ids change: see "copies" below).

**Dependency:** `pip install fig2sketch` (MIT). The script only uses its `figformat` decoder, which makes no network calls.

```bash
python scripts/fig_local.py structure file.fig                  # pages
python scripts/fig_local.py structure file.fig --node 123-456   # children and subsections
python scripts/fig_local.py flow file.fig --node 123-456 --file-key <KEY> --output design-summaries/<market>
```

- First run decodes the file (about 100 s and up to ~4 GB RAM for a 130 MB file) and leaves a gzipped JSON cache (never pickle); later runs take seconds. Warn the user before the first run.
- Over ~30 screens: work per subsection with `--group <name>`.
- Screens are frames between 280 and 2000 px wide (mobile and web).
- Unnamed screens are labelled with their title in «quotes».
- **Copies:** a local copy made by pasting screens into a new file has different node ids; links and images must come from the original file.
- **Fragility:** the .fig format is not official. If decoding fails, try `pip install -U fig2sketch`; if it still fails, move to the next strategy.

## REST API (`rest-api`)

Needs network access to `api.figma.com` and a read-only personal token in `FIGMA_TOKEN` or `~/.figma_token`, set by the user. Never ask for the token in the chat.

```bash
python scripts/figma_rest.py flow "<link with node-id>"      # 1 call: per-screen summary
python scripts/figma_rest.py images "<link>" [--ids a-b]    # 1 call: screen images
python scripts/figma_rest.py limits                        # calls made today and this month
```

72 h cache; `--refresh` only if the design changed. On HTTP 429 the script stops without retrying and prints the wait time. Limits depend on plan and seat; viewer seats on starter plans get very few calls. Reference: Figma's REST API rate-limit documentation.

## Browser export (`browser-export`)

Uses Figma's own Export inside the app browser (Claude Browser or Claude in Chrome) with the user's session. No quota, nothing downloaded to the computer: export blobs are captured inside the page. Needs the link of the section in the original file.

**Warn the user first:** they must sign in themselves; if a frame's export setting is PDF, it will be switched to PNG (an export setting of the shared file, not the design). Do a one-screen test and show it before exporting the rest.

1. Open the section link; set the viewport to 1440×900.
2. Inject `scripts/browser_export_helpers.js` whole with the page-script tool (once per page load; re-inject after navigating).
3. Select the section, press Enter (selects children and expands the layer tree), run `await __list()` → `[id, name]` without notes or connectors.
4. Map screens to criteria keys `[["NN-description", "<id>"], …]`. Many screens share a name: match by order with the design summary and confirm with the contact sheet.
5. `__batch(list)` runs in the background; poll `__progress()` every 10–20 s until `finished: true`; re-run `__batch` for keys with errors.
6. Fetch each image with **one** page-script call per key: `__fetch("NN-description")`. Never several per call: combined output gets truncated and images arrive corrupted.
7. Decode: `python -I scripts/decode_captures.py --output <folder> --contact-sheet <result files>`. It validates each PNG, extracts the largest PNG when Figma returned a ZIP, and creates `_contact-sheet.png`.
8. Save PNGs to `design.images_folder`; restore the viewport; report `formatChanged` (frames whose export format changed).

**If the layer panel does not respond:** export the whole section once and crop each screen with a canvas in the page.

**Fragility:** depends on Figma's web UI (test ids, button labels "Export"/"Exportar"). When Figma changes its UI, update the selectors in `browser_export_helpers.js` and open a pull request.

## Official connector (`official-connector`)

Use the Figma MCP/connector operations for screenshots and design context when the team has quota. Prefer it when available and stable for the team; keep `local-file` first for texts if quota is scarce.
