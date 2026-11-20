## NW-101 – Schedule a recurring transfer to a third-party account

**Epic:** NW-100 – Scheduled transfers  
**Product / Market:** Northwind App – United States  
**Channel:** Mobile

**User story**

**As a** customer with enrolled third-party accounts,  
**I want** to schedule a recurring transfer,  
**so that** I don't repeat periodic payments by hand.

**Functional description**

From "Schedule transfer" the user picks "From account", "To account" (enrolled third parties only), "Amount" and "Recurring". "Continue" opens "Recurrence", where they set "Frequency" (Weekly, Every two weeks or Monthly), "Start date" (from tomorrow) and, optionally, "End date". On "Confirm" they review the summary; tapping "Schedule" creates the schedule through the Scheduling registry service, and "Done!" appears only with its confirmation.

**Scope**

* Recurring schedules to enrolled third-party accounts.
* Date, daily limit and maximum active schedules validations.
* Confirmation and error handling of the registration.

**Out of scope**

* One-time schedules (covered in NW-102).
* Editing and cancelling schedules (covered in NW-103).
* Schedule history.

**Preconditions**

* Signed in.
* At least one active source account and one enrolled third-party account.

**References**

Design: Schedule transfer – section node in the original file  
Requirement: Scheduled › Third-party accounts › Recurring  
Related stories: NW-102 (one-time; shares screens S1 and S3)

**Dependencies**

* Services: Limits lookup (customer's daily limit); Scheduling registry (creates the schedule); active schedules lookup: [Pending: service name].
* Design: S1 Schedule transfer, S2 Recurrence, S3 Confirm, S4 Done!, S5 Error.
* Other stories: NW-102.
* Configuration: maximum-schedules message (see questions).

**Acceptance criteria**

AC1. Choose recurrence

Given the user filled from account, to account and amount on "Schedule transfer",  
when they select "Recurring" and tap "Continue",  
then the system shows "Recurrence" with the frequencies "Weekly", "Every two weeks" and "Monthly".

* "Continue" stays disabled until required fields are complete.

Visual reference: image 01-schedule.png

AC2. Date validation

Given the user is on "Recurrence",  
when they enter an "End date (optional)" equal to or before the "Start date",  
then the system shows "The end date must be after the start date." and does not let them continue.

* The earliest start date is tomorrow.

Visual reference: image 02-recurrence-date-error.png

AC3. Amount above the daily limit

Given the user entered an amount,  
when the Limits lookup service reports it exceeds the daily limit,  
then the system does not let them continue and shows [Pending: daily limit message].

Visual reference: no screen in the design

AC4. Maximum active schedules

Given the customer has 12 active schedules,  
when they try to create a new one,  
then the system does not let them continue and shows the limit message (see question 2).

* Rule from the designer note "Max 12 active schedules per customer".

Visual reference: no screen in the design

AC5. Successful confirmation

Given the user reviewed the summary on "Confirm",  
when they tap "Schedule" and the Scheduling registry service confirms the record,  
then the system shows "Done!" with the text "Your transfer is scheduled.".

* Without the service's confirmation, the success screen is not shown.

Visual reference: image 04-done.png

AC6. Error while creating the schedule

Given the user tapped "Schedule",  
when the Scheduling registry service returns an error or does not answer,  
then the system shows "We couldn't schedule your transfer." with the "Retry" button.

* No success state is shown and no schedule is created. Applies rule *Error state with Retry*.

Visual reference: image 05-error.png

**Decisions taken**

| Decision | Source |
|---|---|
| Maximum 12 active schedules | Designer note |
| Earliest start date: tomorrow | Requirement |
| Daily limit checked when continuing from S1 | Assumption |

**Blocking questions**

1. Is there a fee for scheduled transfers? → Recommended: the same as an immediate third-party transfer.
2. Which message appears at 12 active schedules? → Recommended: "You've reached the maximum of 12 active scheduled transfers."

**Review (sf-lint):** 0 blocks · 0 fix · 1 suggestion (AC3: ask design for a daily-limit screen).
