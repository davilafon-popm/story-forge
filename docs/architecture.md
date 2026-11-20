# Architecture

story-forge separates **what** a good user story needs (method) from **where** the information lives (tools) and **who** does each step (models).

```mermaid
flowchart TD
    P[Team profile<br/>story-forge.profile.yaml] --> W
    subgraph Method["Method (skills)"]
      W[sf-workflow] --> PC[sf-precheck]
      PC --> SR[sources-reader]
      PC --> DX[sf-design-reader / screen-exporter]
      SR --> D[Decisions & blocking questions]
      DX --> D
      D --> WR[sf-write-story / story-writer]
      WR --> L[sf-lint / story-reviewer]
      L --> PU[sf-publish / tracker-publisher]
      PU --> RT[sf-retro]
      RT --> KB
    end
    subgraph Market["Per market (country, brand, unit)"]
      T[(Tracker)]
      WK[(Wiki / specs)]
      KB[(Knowledge base<br/>H rules · R behaviors · flow map)]
      DS[(Design file)]
    end
    SR --> T & WK & KB & DS
    DX --> DS
    PU --> T
```

## Layers

| Layer | Content | Changes when |
|---|---|---|
| Method | Skills `sf-*`, decision policy, templates, lint checklist | The community improves the method |
| Knowledge | Each market's writing rules, standard behaviors, flow → source map | A retro finds a new rule |
| Configuration | Team profile: tools, sites, projects, languages, strategies, model routing | The team changes tools or adds a market |
| Adapters | Connectors (MCP) and tool guides (`references/`, `plugins/story-forge/reference/tool-adapters.md`) | A vendor changes its API or UI |

## Principles

1. **Tool-agnostic method.** Skills speak of tracker, wiki and design tool and read the team profile; product details live in `reference/` and `references/`.
2. **Every fragile step has alternatives** (see `plugins/story-forge/reference/options-matrix.md`), ordered by the team.
3. **Markets are isolated.** A story reads and writes only its market's knowledge base and data.
4. **Decide, cite, or ask.** The decision policy produces near-final stories with at most N blocking questions.
5. **AI decides and writes; scripts move files.**
6. **The human approves every write** to the tracker or the knowledge base.
7. **Continuous learning.** Retros turn bugs and corrections into rules.
