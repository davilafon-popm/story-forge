# Evaluation checklist / Lista de evaluación

Use it to compare a generated story with `expected-story.md` after changing skills, models or templates. A run **passes** when every "Must" item is met.

| # | Level | Check |
|---|---|---|
| 1 | Must | Scope matches the ticket: recurring, third-party; one-time and editing are out of scope. |
| 2 | Must | All UI texts are literal from `design-summary.md`, in quotes. |
| 3 | Must | The designer note (max 12 active schedules) appears as a criterion and is cited. |
| 4 | Must | Success is shown only with the service's confirmation. |
| 5 | Must | Error handling exists for the scheduling service (P5) and the limits service. |
| 6 | Must | No invented service names: unknown ones are `[Pending: …]`. |
| 7 | Must | The fee question is asked (amounts/fees are blocking), with a recommendation. |
| 8 | Must | Every criterion has a visual reference or says there is no screen. |
| 9 | Should | Date validation uses the design's exact message. |
| 10 | Should | Decisions table separates sourced decisions from assumptions. |
| 11 | Should | At most `story.max_blocking_questions` questions. |
| 12 | Should | Rule citations (by name, e.g., "Applies rule *Error state with Retry*") sit in a rule bullet, not inside Given/When/Then. |
