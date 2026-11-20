# Getting started

1. **Install** the plugin (see README).
2. **Configure**: say "set up story-forge". Answer the questions (tracker, wiki, design tool, language, markets, fallbacks). The profile is saved as `story-forge.profile.yaml` in your working folder or Claude Project.
3. **Knowledge base**: if your team has no written rules yet, accept the offer to create the starter set (`knowledge-base/<language>/`) in your wiki or as markdown files. Adapt values in braces.
4. **Flow map**: add the flows you are working on to the flow → source map (requirement and design link per flow and channel).
5. **First story**: "write the story ABC-123" (add requirement and design links if they are not in the map). Answer the blocking questions, review the draft.
6. **Publish**: "update ABC-123 with this story".
7. **Retro**: at the end of the sprint, "run the story retro for sprint N" and approve the rules worth keeping.

## Try it without real data

Use `examples/es-scheduled-transfer/`: give the requirement and design summary to `sf-write-story` and compare the result with `expected-story.md` using `sf-lint`.

## Tips

- Keep the most capable model for the main conversation; subagents use cheaper models where quality is equal.
- If design quota is scarce, put `local-file` first for texts and `browser-export` or `designer-export` first for images.
- Read the usage log line at the end of each run and adjust `agents.routing`.
