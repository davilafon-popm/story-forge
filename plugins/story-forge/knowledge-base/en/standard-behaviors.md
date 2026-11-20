# Standard behaviors

**Status:** ACTIVE · **Last updated:** YYYY-MM-DD · **Market:** {name}

Each rule has a short, unique name, and stories cite it by that name ("Applies rule *Error state with Retry*"). Names do not depend on order, so adding, moving or deleting rules never breaks a citation; if you rename a rule, search the stories that cite it. Statuses: **ACTIVE** (applies), **TO BE DEFINED** (has a proposal; until decided, stories treat it as an explicit pending item) and **APPROVED – IN BACKLOG**.

This is story-forge's starter set, born from real bugs in transactional apps. Values in braces are your team's decision. Delete sections that do not apply and add your own through retros.

## 1. Date range filter (From / To)

| Name | Rule | Status | Origin |
|---|---|---|---|
| Default period | By default the list shows the last {N} days; it never loads empty if records exist in that period. | TO BE DEFINED | Starter set |
| Maximum range | The queryable range is at most {N} days. | TO BE DEFINED | Starter set |
| From after To | If the user picks "From" after "To", the system keeps "To" and shows a validation message. | ACTIVE | Starter set |
| Apply with both dates | **Proposal:** "Apply" is enabled only when both dates are selected. | TO BE DEFINED | Starter set |

## 2. Amount range filter

| Name | Rule | Status | Origin |
|---|---|---|---|
| Equal minimum and maximum | Minimum equals maximum. **Proposal:** allow it; returns records for that exact amount. | TO BE DEFINED | Starter set |
| Only one amount | Only one amount entered. **Proposal:** "Apply" stays disabled until both are entered. | TO BE DEFINED | Starter set |

## 3. Empty and error states

| Name | Rule | Status | Origin |
|---|---|---|---|
| Two empty states | The empty state distinguishes "no records in the period" from "no results for the search or filter", with different messages. | ACTIVE | Starter set |
| Error state with Retry | On connection or service errors, the empty state is not shown: an error state with "Retry" is shown. | ACTIVE | Starter set |
| Generic error screen | Generic error screen: title, text with the market's support phone, and "Retry" (texts per design). | TO BE DEFINED | Starter set |

## 4. Language

| Name | Rule | Status | Origin |
|---|---|---|---|
| Selected language everywhere | All texts, messages, states and reports follow the selected language, including no-results messages. | ACTIVE | Starter set |

## 5. Report downloads (PDF, XLS, CSV)

| Name | Rule | Status | Origin |
|---|---|---|---|
| Report per design | Report content and layout follow the approved design, with all its fields. | ACTIVE | Starter set |
| CSV keeps accents | CSV uses an encoding that keeps accents when opened in spreadsheets. | ACTIVE | Starter set |
| XLS header does not cover data | The XLS header or banner does not cover report data. | ACTIVE | Starter set |
| Download what the user sees | **Proposal:** downloads respect active filters and search; the report contains what the user sees. | TO BE DEFINED | Starter set |

## 6. Transaction or record lists

| Name | Rule | Status | Origin |
|---|---|---|---|
| Date and time per record | Each record shows date and time. | ACTIVE | Starter set |
| Consistent credit and debit signs | **Proposal:** same credit/debit signs and colors across products. | TO BE DEFINED | Starter set |

## 7. Button and action enablement

| Name | Rule | Status | Origin |
|---|---|---|---|
| Confirm disabled without changes | In update forms, the confirm button stays disabled while nothing has changed. | ACTIVE | Starter set |
| Actions per product type | **Proposal:** a table per product type with visible and enabled actions, referenced from stories. | TO BE DEFINED | Starter set |

## 8. Keyboard

| Name | Rule | Status | Origin |
|---|---|---|---|
| Active field visible with keyboard | When the keyboard opens, the active field (including search) stays visible. | ACTIVE | Starter set |

## 9. List and detail consistency

| Name | Rule | Status | Origin |
|---|---|---|---|
| Detail matches list | Detail values (balances, rates, statuses) match the list; the detail never shows zero when the list shows a value. | ACTIVE | Starter set |

## 10. Sign-up or onboarding flows

| Name | Rule | Status | Origin |
|---|---|---|---|
| Confirm before leaving | Leaving mid-flow shows a confirmation modal with options to leave or continue (texts per design). | ACTIVE | Starter set |
| Support phone on validation error | On an error validating customer data, the flow's error screen shows the market's support phone. | ACTIVE | Starter set |
| Required permissions | System permissions the flow needs (camera, location…) are mandatory to continue and requested with the native dialog. | ACTIVE | Starter set |
