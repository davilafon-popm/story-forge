# story-forge

**Write near-final user stories from requirements and designs — in any language, with any tracker, wiki and design tool.**

[Español](README.es.md) · License: [Apache 2.0](LICENSE) · Status: early release (0.1.0)

story-forge is a method for product owners, packaged as a Claude plugin. It turns a ticket, its requirement page and its design into a detailed user story with numbered acceptance criteria, named services, one design image per criterion and your team's standards applied. Then it reviews the story, publishes it into the ticket you name, and learns from each sprint's bugs.

## Why

Most of a PO's time on a story is not writing: it is confirming scope, chasing texts in the design, exporting screens, applying the team's unwritten rules and answering the same QA questions every sprint. story-forge makes those steps explicit, repeatable and improvable.

## What a story looks like

Excerpt of the fictional example in [`examples/`](examples/) (English version, Northwind profile: headings and "AC" numbering enabled):

```
AC5. Successful confirmation

Given the user reviewed the summary on "Confirm",
when they tap "Schedule" and the Scheduling registry service confirms the record,
then the system shows "Done!" with the text "Your transfer is scheduled.".

* Without the service's confirmation, the success screen is not shown.

Visual reference: image 04-done.png
```

Each story also comes with a **decisions table** (what was decided and from which source), at most N **blocking questions** with a recommended answer, a **lint** result and suggested **test cases**.

## What it does

| Step | Skill | What you get |
|---|---|---|
| Configure | `sf-setup` | A team profile: tools, markets, languages, fallbacks, model routing |
| Check scope | `sf-precheck` | Proof that ticket, requirement and design describe the same flow |
| Read the design | `sf-design-reader` | Texts, controls, notes and one PNG per screen, with fallbacks for quotas |
| Write | `sf-write-story` | A near-final story, a decisions table and at most N blocking questions |
| Whole flow | `sf-backlog` | An epic and its stories, after one review round |
| Review | `sf-lint` | Findings per criterion with severity and fix |
| Publish | `sf-publish` | The story in the ticket, images under each criterion |
| Research | `sf-research` | External facts with sources (regulation, practices, docs) |
| Learn | `sf-retro` | New rules for your knowledge base from the sprint's bugs |
| Orchestrate | `sf-workflow` | All of the above, with subagents and the right model per step |

## Design principles

- **Tool-agnostic.** Skills speak of tracker, wiki and design tool; your profile says which ones (Jira, Azure DevOps, Linear, Confluence, Notion, Figma, Penpot…). See [CONNECTORS.md](plugins/story-forge/CONNECTORS.md).
- **Any language.** Story language, labels and Given/When/Then keywords come from the profile and `templates/i18n.yaml`.
- **Alternatives for every fragile step.** Quotas, permissions and vendor UIs change; each step has ordered fallbacks. See the [options matrix](plugins/story-forge/reference/options-matrix.md).
- **Several markets.** Countries, brands or units keep separate knowledge bases and data.
- **Human in control.** Nothing is written to your tracker or wiki without your explicit request or approval.
- **Learns.** Retros turn bugs and corrections into rules.

## Scope and requirements

- **Agnostic to your tools, not to the AI.** story-forge is a Claude plugin: it relies on Claude skills, subagents (optional) and, for some fallbacks, Claude's app browser or Claude in Chrome. Your tracker, wiki and design tool can be anything with a connector, an API or a manual fallback.
- **Connectors** for your tracker and wiki in your Claude workspace (or the `manual` strategies).
- **Python 3.10+** only if you use the design scripts: `pip install -r requirements.txt`.
- **Maturity.** The method was used in real projects (Jira, Confluence, Figma) before being packaged; story-forge 0.1.0 itself is new. Report what works and what breaks with your tools.

## Install

**Claude Code**

```
/plugin marketplace add davilafon-popm/story-forge
/plugin install story-forge@story-forge
```

While the repository is private, adding the marketplace needs a GitHub account with access to it.

**Claude (Cowork / desktop)**: zip the folder `plugins/story-forge` (its contents at the zip root), rename it to `story-forge.plugin` and add it as a plugin. Your organization may also distribute it through its plugin catalog.

The plugin needs its whole folder (templates, knowledge base, references): uploading single skills on their own is not supported.

Then say "set up story-forge". The `sf-setup` skill asks a few questions and writes your profile. Step-by-step guide: [docs/getting-started.md](docs/getting-started.md).

## Repository map

```
plugins/story-forge/        the plugin: skills, agents, templates, starter knowledge base, reference
profiles/examples/          fictional team profiles
examples/                   fictional inputs + expected stories (evaluation cases)
docs/                       architecture, getting started, privacy
tests/ · tools/             automated tests and repository checks
```

## Contributing

Improvements to the method, new languages, tool adapters and starter rules are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) ([español](CONTRIBUTING.es.md)). Never include real company data in examples or rules. Security issues: see [SECURITY.md](SECURITY.md). Who decides what: see [GOVERNANCE.md](GOVERNANCE.md) — each Product Owner can change their own implementation unless their organization does not allow it.

## Disclaimer

story-forge is an independent project. It is not affiliated with, endorsed by or sponsored by Anthropic, Atlassian, Figma, Microsoft, Notion, Linear or any other vendor named here; product names are used only to describe compatibility. Some optional fallbacks automate a vendor's web interface or read an unofficial file format: you are responsible for using them in line with each tool's terms of service and your organization's policies, and they may stop working when the vendor changes its product.

## Author

Method and original skills by **David Dávila**. See [NOTICE](NOTICE).
