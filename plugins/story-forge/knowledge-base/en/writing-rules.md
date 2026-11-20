# User story writing rules

**Status:** ACTIVE · **Last updated:** YYYY-MM-DD · **Market:** {name}

Rules for writing stories, cited by name and updated with corrections that repeat (see sf-retro). This is story-forge's starter set: adapt it to your team; change the origin when a rule comes from one of your tickets.

## A. Sources and texts

| Name | Rule | Origin |
|---|---|---|
| Literal design texts | **Use the design's literal texts** (titles, buttons, messages, labels), even if they look provisional. If they look provisional, use them anyway and add a note; do not replace them with a pending item. | Starter set |
| Check before leaving a pending item | **Check the design and this standard before leaving a pending item.** If the design already shows the behavior (a modal, an error screen, a disabled state), describe it. | Starter set |
| Designer notes are rules | **Designer notes are business rules.** Turn them into criteria and cite the note. If they contradict the requirement, record a pending item; do not pick one. | Starter set |
| Sample data are not requirements | **Design sample data are not requirements.** Masked phones, amounts, names and sample dates never become rules. | Starter set |

## B. Behaviors and edges

| Name | Rule | Origin |
|---|---|---|
| Apply standard behaviors | **Apply standard behaviors.** If the story has filters, lists, downloads, forms or empty states, include the applicable Active rules or cite them by name ("Applies rules *From after To* and *Two empty states*"). | Starter set |
| Define the edges | **Define the edges.** Every story states what happens with empty data, connection or service errors and limit values. What cannot be defined becomes an explicit pending item, never silence. | Starter set |
| Declare exceptions | **Declare exceptions.** "Exception to rule *Download what the user sees*: …". | Starter set |

## C. Pending items and relations

| Name | Rule | Origin |
|---|---|---|
| Pending items only for business decisions | **Pending items are only for real business decisions:** amounts, limits, fees, regulatory or legal topics, scope between stories and contradictions between sources. Each includes a recommended proposal. | Starter set |
| Only confirmed related stories | **Do not list unconfirmed related stories.** | Starter set |
| Gap found by QA | **Gap found by QA.** If QA reports a behavior neither the story nor the standard defines, it is not a development bug: record it as "To be defined" in the standard and, once decided, adjust the story or handle it as a change request. | Starter set |

## D. Images

| Name | Rule | Origin |
|---|---|---|
| One image per criterion | **One screen image under each criterion,** embedded in the ticket description; never loose attachments. If a criterion has no screen, say so explicitly. | Starter set |
