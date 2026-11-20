<!--
"Detailed functional story" template (English).
No markdown headings: structure with bold labels.
Inside a block, line breaks use two trailing spaces.
-->
**{KEY} – {Short flow title}**  
**Epic:** {KEY} – {Epic name}  
**Product / Market:** {team.product} – {market.name}  
**Channel:** {Mobile | Web | Both}

**User story**

**As a** {type of customer or user},  
**I want** {action or capability},  
**so that** {benefit or need it solves}.

**Functional description**

One or two paragraphs: entry point (previous screen, button or menu), exact name of each screen or sheet as it appears in the design, default values, rules that apply and what happens when moving forward. If it is an improvement, what changes versus current behavior.

**Scope**

* Included capability, in short sentences.

**Out of scope**

* Excluded capability and the story that covers it (with its key).
* Elements visible in the design with no behavior defined in this story.

**Preconditions**

* Access condition, session or process state, data the user must have.

**References**

Design: {flow name and link to the node in the original file}  
Requirement: {link}  
Related stories: {key, name and reason; confirmed relations only}

**Dependencies**

* Services: each service by its function, with its inventory name or [Pending: service name].
* Design: required screens, sheets and states.
* Other stories: keys it depends on.
* Configuration: texts, messages, parameters, permissions.

**Acceptance criteria**

1. Short behavior name

Given {context or initial condition},  
when {user action or system event},  
then {observable, verifiable result}.

* Rule, validation or detail of this criterion. Applies rule *From after To*.
* Enablement condition or additional behavior.

Visual reference: image 01-description.png

2. Next behavior

(Same format.)
