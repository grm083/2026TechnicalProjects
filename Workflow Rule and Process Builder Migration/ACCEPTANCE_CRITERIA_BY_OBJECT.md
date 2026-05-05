# Acceptance Criteria by Object
## Workflow Rules & Process Builder Migration

**Document Type:** Quality Assurance Acceptance Criteria
**Audience:** QA Testers, Test Leads, Business Analysts, UAT Participants
**Source Analysis:** `AUTOMATION_MIGRATION_ANALYSIS.md`
**Document Version:** 1.0
**Last Updated:** May 5, 2026

---

## Purpose & How To Use This Document

This document defines the **functional Acceptance Criteria (AC)** that must be satisfied to confirm a successful migration of Workflow Rules and Process Builders. The migration project is **organized by object**, so this document is also organized by object — one section per object touched by the migration.

### Important Principles

1. **Technology Agnostic** — These criteria describe **what the system must do**, never **how** it does it. A criterion does not care whether the logic is delivered by a Workflow Rule, a Process Builder, a Record-Triggered Flow, an Apex Trigger, a Platform Event, or any other mechanism. If the function is preserved, the AC passes.
2. **Pre/Post Parity is the Default Standard** — Unless explicitly stated, every AC describes behavior that existed *before* migration and must continue to behave *identically* after migration. QA's job is to confirm parity.
3. **Object-Scoped** — Each AC is owned by the object section in which it appears. Cross-object effects are noted in the "Cross-Object Impact" subsection of the originating object.
4. **Given / When / Then** — Each AC follows a Given/When/Then format so testers can build test cases directly from it.
5. **Sign-Off** — Each object section has a sign-off block. An object is "Migration Complete" only when **every AC in its section** has been validated and signed off.

### How a Tester Should Read an AC

> **AC-CASE-001:** *"Given a new Case is created with no ParentId, when the Case is saved, then the Reference Number field shall equal the Case Number."*

The tester:
- Sets up the **Given** state.
- Performs the **When** action.
- Verifies the **Then** outcome — without inspecting backend logs, code, or automation type.

### Severity / Priority Legend

| Priority | Meaning |
|---|---|
| **P0 — Blocker** | Must pass for go-live. Failure halts release. |
| **P1 — Critical** | Must pass for go-live; one-business-day fix SLA. |
| **P2 — Major** | Should pass for go-live; can ship with documented workaround. |
| **P3 — Minor** | Nice-to-have; tracked as defect, does not block. |

### Test Type Legend

| Type | Meaning |
|---|---|
| **F** | Functional — single-record happy path |
| **B** | Bulk — 200+ record load |
| **N** | Negative — invalid/edge inputs |
| **I** | Integration — external system involved |
| **R** | Regression — adjacent functionality unchanged |
| **P** | Performance — execution time / governor limits |

---

## Object Coverage Index

| # | Object | # of ACs | Has External Integration? |
|---|---|---|---|
| 1 | Case | 18 | Yes (Acorn) |
| 2 | Account | 6 | No |
| 3 | Contact | 8 | Yes (SMS opt-in API) |
| 4 | EmailMessage | 12 | Yes (Genesys, Indico) |
| 5 | Task | 6 | Yes (Genesys) |
| 6 | WorkOrder | 7 | Yes (Acorn) |
| 7 | Quote (SBQQ__Quote__c) | 8 | Yes (Acorn / API Hub) |
| 8 | QuoteLine (SBQQ__QuoteLine__c) | 2 | No |
| 9 | Business Rule (Business_Rule__c) | 9 | No |
| 10 | Comment (Comment__c) | 6 | Yes (Acorn) |
| 11 | Case Comment | 3 | No |
| 12 | Entitlement | 4 | No |
| 13 | Account Title (Account_Title__c) | 3 | No |
| 14 | Notification Contact (Notification_Contact__c) | 4 | No |
| 15 | Genesys Routing (Genesys_Routing__c) | 6 | Yes (Genesys) |
| 16 | Genesys Reporting (Genesys_Reporting__c) | 3 | Yes (Genesys) |
| 17 | Supplier | 5 | No |
| 18 | Vendor Service Location | 2 | No |
| 19 | SFDC Email Message (SFDCEmailMessage__c) | 2 | No |
| | **Cross-Cutting AC (all objects)** | 12 | — |
| | **TOTAL** | **126** | |

---

# 1. CASE OBJECT

**In-Scope Source Automations:**
- Process Builder: `Case_Update_Process` (Draft → archive)
- Workflow Rule: `Send Acorn New Case Information` (Active)
- Workflow Rule: `Set Reference Number` (Active)
- Workflow Rules: 15 inactive rules (archive only)

## 1.1 Reference Number Population

**AC-CASE-001 — Reference Number on Standalone Case Create** | P0 | F
- **Given** a user creates a new Case with no Parent Case populated,
- **When** the Case is saved,
- **Then** the Case Reference Number field shall be populated with the Case Number value.

**AC-CASE-002 — Reference Number Not Set on Child Case** | P1 | F
- **Given** a user creates a new Case **with** a Parent Case populated,
- **When** the Case is saved,
- **Then** the Case Reference Number field shall **not** be auto-populated by this rule (it must remain whatever the user entered, including blank).

**AC-CASE-003 — Reference Number Bulk Insert** | P0 | B
- **Given** 200 Cases are inserted in a single batch with no Parent Case,
- **When** the batch commits,
- **Then** every Case's Reference Number shall equal its Case Number with zero record-level errors.

**AC-CASE-004 — Reference Number Idempotency on Update** | P1 | R
- **Given** an existing Case whose Reference Number is already populated,
- **When** the Case is updated (any field other than Reference Number),
- **Then** the Reference Number shall not change.

## 1.2 Acorn Integration — "Send Acorn New Case Information"

**AC-CASE-005 — Acorn Outbound on New Service Case** | P0 | I
- **Given** a Case of record type "New Service Case" is created with `Integrate_with_Acorn__c = true` and the qualifying status conditions met,
- **When** the Case is saved,
- **Then** a Case payload shall be transmitted to the Acorn endpoint exactly once for that Case event.

**AC-CASE-006 — Acorn Outbound on Modify Existing Service Case** | P0 | I
- **Given** an existing Case of record type "Modify Existing Service Case" qualifies for transmission,
- **When** the qualifying status transition occurs,
- **Then** a Case payload shall be transmitted to Acorn with the modified Case data.

**AC-CASE-007 — Acorn Outbound on Pickup Case** | P0 | I
- **Given** a Case of record type "Pickup Case" qualifies for transmission,
- **When** the qualifying status transition occurs,
- **Then** a Case payload shall be transmitted to Acorn with the pickup data.

**AC-CASE-008 — Acorn Outbound Suppressed When Flag Off** | P0 | N
- **Given** a Case where `Integrate_with_Acorn__c = false`,
- **When** any qualifying status transition occurs,
- **Then** **no** payload shall be sent to Acorn for that event.

**AC-CASE-009 — Acorn Issue Id Used When Already Assigned** | P1 | I
- **Given** a Case that already has `Acorn_Issue_Id__c` populated,
- **When** the Case is updated and re-transmitted,
- **Then** the existing Acorn Issue Id shall be included in the payload (no new Acorn Issue Id shall be generated by Salesforce).

**AC-CASE-010 — Acorn Outbound Failure Handling** | P0 | I, N
- **Given** the Acorn endpoint is unavailable or returns a non-success response,
- **When** a qualifying Case event occurs,
- **Then** the failure shall be logged in a tester-visible location AND the Case save itself shall **not** be rolled back to the user.

**AC-CASE-011 — Acorn Bulk Transmission** | P0 | B, I
- **Given** 200 qualifying Cases are updated in a single batch,
- **When** the batch commits,
- **Then** every qualifying Case shall result in a transmission to Acorn with no governor-limit failures and no dropped records.

## 1.3 Status & Sub-Status Behavior (Replaces Inactive `Case_Update_Process`)

**AC-CASE-012 — Inactive Process Builder Has No Effect Post-Migration** | P1 | R
- **Given** the `Case_Update_Process` Process Builder was Inactive in the legacy state,
- **When** any Case event occurs that the legacy process *would* have evaluated had it been active,
- **Then** there shall be no observable behavior change attributable to that legacy automation (it must remain a no-op, identical to its pre-migration inactive behavior).

## 1.4 Inactive Workflow Rules — Archived (No-Op Verification)

**AC-CASE-013 — Inactive Rules Remain Inactive Post-Migration** | P1 | R
- **Given** the following rules were Inactive prior to migration: *Acorn W/O Is Populated, Close Case, Close Pickup Case, GENESYS Email2Case Workflow Rule, Override_SLA_Option, PO Mandatory or Not, Recreated Work Order Successful, SendBaleCaseToAcorn, Uncheck Ignore Duplicate on change, Update BackOffice Checkbox Workflow, Update Service Date with Local Time, UpdateCaseSla, WorkOrderCreated, isByPassDuplicateCase, Contact status*,
- **When** any Case event occurs that those rules would have evaluated,
- **Then** none of them shall produce a field update, outbound message, or other observable effect.

## 1.5 Cross-Object Impact

**AC-CASE-014 — Case → Work Order Status Synchronization Preserved** | P1 | R
- **Given** logic that previously synchronized Work Order status from Case status changes,
- **When** a Case status change occurs that is supposed to drive a Work Order update,
- **Then** the corresponding Work Order field shall update to the same value, in the same direction, as it did before migration. *(See also AC-WO-006.)*

**AC-CASE-015 — Case Comment Timestamp Roll-Up Preserved** | P1 | R
- **Given** a Case Comment is added to a Case,
- **When** the Case Comment commits,
- **Then** the parent Case shall reflect the Case Comment's created date in the corresponding Case field. *(See also AC-CC-001.)*

## 1.6 Performance & Stability

**AC-CASE-016 — Case Save Time Within Baseline** | P1 | P
- **Given** a single Case insert/update is performed,
- **When** the save completes,
- **Then** the average save time shall be **no worse than** the pre-migration baseline (target: equal-or-better).

**AC-CASE-017 — Case Bulk Save No Limit Exceptions** | P0 | B, P
- **Given** a batch of 200 Cases is inserted/updated,
- **When** the batch commits,
- **Then** zero limit-exceeded errors shall be raised (SOQL, DML, CPU, callouts, heap).

**AC-CASE-018 — Case Audit/History Continuity** | P2 | R
- **Given** any field change that triggers automation,
- **When** the change commits,
- **Then** the field history (if tracked) shall reflect the same final value as before migration.

### Sign-Off — Case
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-CASE-001 … 018 |
| Business Owner — Service Operations | | | |
| Integration Owner — Acorn | | | |

---

# 2. ACCOUNT OBJECT

**In-Scope Source Automations:**
- Process Builder: `Create_SLA_upon_activating_Account` (Active)

## 2.1 SLA / Entitlement Auto-Creation

**AC-ACCT-001 — SLA Created on Account Activation** | P0 | F
- **Given** an Account is in a not-yet-activated status with no Entitlements,
- **When** the Account status is changed to "Active",
- **Then** the system shall create the appropriate Entitlement record(s) related to that Account, matching the type and quantity that were created prior to migration for the same input.

**AC-ACCT-002 — No Duplicate Entitlement on Re-Save** | P0 | N
- **Given** an Account that already has the Entitlement record(s) the rule would create,
- **When** the Account is re-saved (in any way) while still active,
- **Then** **no** duplicate Entitlement records shall be created.

**AC-ACCT-003 — No Entitlement Created on Inactive Account** | P1 | N
- **Given** an Account whose status is not "Active",
- **When** the Account is created or updated,
- **Then** the SLA/Entitlement creation logic shall **not** fire.

**AC-ACCT-004 — Entitlement Linked to Correct Account** | P0 | F
- **Given** an Account is activated,
- **When** the Entitlement record(s) are created,
- **Then** every created Entitlement shall be related to the activating Account (no orphan or mis-linked Entitlements).

**AC-ACCT-005 — Bulk Account Activation** | P0 | B
- **Given** 200 Accounts are activated in a single batch,
- **When** the batch commits,
- **Then** every Account shall receive the correct Entitlement record(s) with no governor-limit errors and no missing Entitlements.

**AC-ACCT-006 — Pre-Existing Entitlement Trigger Coexists** | P1 | R
- **Given** any other Entitlement-side automation already in place,
- **When** an Account-driven Entitlement is created,
- **Then** the downstream automation behavior on that Entitlement shall match its pre-migration behavior. *(See also AC-ENT-001.)*

### Sign-Off — Account
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-ACCT-001 … 006 |
| Business Owner — Customer Onboarding | | | |

---

# 3. CONTACT OBJECT

**In-Scope Source Automations:**
- Process Builder: `Populate_Preferred_Language_from_Contact_to` (Active)
- Process Builder: `Update_Text_Notification_Opt_In` (Active)
- Workflow Rule: `Contact status updated` (Inactive — archive)
- Workflow Rule: `Text notification opt-out on number change` (Inactive — archive)

## 3.1 Preferred Language Propagation

**AC-CONT-001 — Preferred Language Propagated to Related Object** | P1 | F
- **Given** a Contact has Preferred Language populated and is linked to the target related record,
- **When** the Contact is saved (insert or relevant update),
- **Then** the Preferred Language value on the related target record shall match the Contact's value.

**AC-CONT-002 — Preferred Language Updates on Change** | P1 | F
- **Given** a Contact's Preferred Language value is changed,
- **When** the Contact is saved,
- **Then** the related target record's Preferred Language shall update to the new value.

**AC-CONT-003 — Preferred Language Bulk Update** | P1 | B
- **Given** 200 Contacts have their Preferred Language updated in a single batch,
- **When** the batch commits,
- **Then** every related target record shall reflect the new value with no errors.

## 3.2 Text Notification Opt-In Management

**AC-CONT-004 — Opt-In Flag Drives External SMS API Call** | P0 | I
- **Given** a Contact's `Text_Notifications_Opt_In__c` is changed from false → true (with valid mobile phone),
- **When** the Contact is saved,
- **Then** the external SMS opt-in service shall receive an opt-in request for that mobile number.

**AC-CONT-005 — Opt-Out Flag Drives External SMS API Call** | P0 | I
- **Given** a Contact's `Text_Notifications_Opt_In__c` is changed from true → false,
- **When** the Contact is saved,
- **Then** the external SMS opt-in service shall receive an opt-out request.

**AC-CONT-006 — Mobile Phone Change Triggers Re-Sync** | P1 | I
- **Given** a Contact is opted-in and the mobile phone number changes,
- **When** the Contact is saved,
- **Then** the external SMS service shall be notified of the new number using the equivalent opt-in/opt-out behavior that existed before migration.

**AC-CONT-007 — SMS API Failure Does Not Block Save** | P0 | I, N
- **Given** the external SMS service is down or returns an error,
- **When** a qualifying Contact change occurs,
- **Then** the Contact save shall succeed, the failure shall be logged, and the failed call shall be retryable.

## 3.3 Inactive Workflow Rules

**AC-CONT-008 — Archived Contact Workflow Rules Remain No-Op** | P2 | R
- **Given** the legacy "Contact status updated" and "Text notification opt-out on number change" rules were Inactive,
- **When** a Contact change occurs that those rules would have evaluated,
- **Then** there shall be no observable effect from either legacy rule.

### Sign-Off — Contact
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-CONT-001 … 008 |
| Business Owner — Customer Communications | | | |
| Integration Owner — SMS Provider | | | |

---

# 4. EMAILMESSAGE OBJECT

**In-Scope Source Automations:**
- Process Builder: `Email_to_Case` (Active) — invokes EmailMessageHelper, EmailMessageContactMapping, Genesys Routing flow, 1:1 match flow, Indico
- Process Builder: `EMailMessageUpdate` (Active) — invocable, called by other automation

## 4.1 Inbound Email Processing

**AC-EM-001 — Inbound Email Creates / Attaches to Case** | P0 | F, I
- **Given** an inbound email arrives at the Email-to-Case mailbox,
- **When** the EmailMessage record is created,
- **Then** the email shall be associated with the correct Case (new or existing) per the same matching logic that applied pre-migration.

**AC-EM-002 — `To_Be_Processed__c` Drives Processing** | P0 | F
- **Given** an EmailMessage with `To_Be_Processed__c = true`,
- **When** the EmailMessage is saved,
- **Then** the email processing chain shall execute (helper invocation, contact mapping, routing).

**AC-EM-003 — `IndicoStatus__c` Routes Through Indico** | P0 | I
- **Given** an EmailMessage qualifies for Indico ML processing,
- **When** the EmailMessage is saved with the qualifying status,
- **Then** the email shall be sent to Indico and the IndicoStatus field shall progress through the same lifecycle states observed pre-migration.

## 4.2 Contact Mapping (1:1 Match)

**AC-EM-004 — Single Matching Contact Linked** | P0 | F
- **Given** an inbound email's "From" address matches exactly one Contact,
- **When** the EmailMessage is processed,
- **Then** the email shall be associated with that Contact.

**AC-EM-005 — Multiple Matches Resolve Per Pre-Migration Rule** | P1 | F
- **Given** an inbound email's "From" address matches more than one Contact,
- **When** the EmailMessage is processed,
- **Then** the resolution behavior shall be identical to pre-migration (same Contact selected, or same fall-through behavior).

**AC-EM-006 — No Matching Contact Handled Gracefully** | P1 | N
- **Given** an inbound email's "From" address matches no Contact,
- **When** the EmailMessage is processed,
- **Then** the email shall still be saved, the Case shall still be created/attached, and the system shall behave identically to pre-migration.

## 4.3 Genesys Routing Subflow

**AC-EM-007 — Email Routed to Genesys** | P0 | I
- **Given** an EmailMessage is processed and meets Genesys routing criteria,
- **When** the routing step executes,
- **Then** a Genesys routing payload shall be transmitted exactly once. *(See also AC-GR-001.)*

## 4.4 EmailMessageUpdate Invocable

**AC-EM-008 — Invocable Called from Other Automation Updates Email Fields** | P1 | F
- **Given** another automation invokes the EmailMessage update routine with valid parameters,
- **When** invocation completes,
- **Then** the target EmailMessage fields shall be updated to the values that the legacy invocable produced.

**AC-EM-009 — All Legacy Callers Still Function** | P0 | R
- **Given** every automation that previously called `EMailMessageUpdate`,
- **When** each caller executes,
- **Then** the EmailMessage update step shall succeed (i.e., no caller is broken by a renamed/removed handle).

## 4.5 Bulk & Performance

**AC-EM-010 — Bulk Email Processing** | P0 | B, P
- **Given** 200 EmailMessages are inserted in a single transaction,
- **When** the transaction commits,
- **Then** every email shall be processed end-to-end without governor-limit errors and within the established performance baseline.

**AC-EM-011 — Email Volume Throughput Meets SLA** | P0 | P
- **Given** the steady-state inbound email rate measured pre-migration,
- **When** the same rate is replayed post-migration,
- **Then** end-to-end processing latency shall be equal-to-or-better than baseline.

## 4.6 Failure Handling

**AC-EM-012 — Apex Helper or Subflow Failure Does Not Lose Email** | P0 | N, I
- **Given** any downstream component (EmailMessageHelper, EmailMessageContactMapping, Genesys subflow, Indico) fails,
- **When** the EmailMessage is processed,
- **Then** the EmailMessage record shall persist, the failure shall be logged in a tester-visible location, and the email shall be re-processable.

### Sign-Off — EmailMessage
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-EM-001 … 012 |
| Business Owner — Service Center / Email Channel | | | |
| Integration Owner — Genesys | | | |
| Integration Owner — Indico | | | |

---

# 5. TASK OBJECT

**In-Scope Source Automations:**
- Process Builder: `Update_Case_for_Task_Process` (Draft — archive)
- Workflow Rule: `Update Attempt for Notify Customer Of Service Update task` (Active)

## 5.1 Notification Attempt Tracking

**AC-TASK-001 — First Notification Attempt Defaulted** | P1 | F
- **Given** a Task is created with `Process__c = "Notify Customer Of Service Update"` and no Attempt value,
- **When** the Task is saved,
- **Then** the Attempt field shall be populated with the same default value that the legacy rule produced (1 on insert).

**AC-TASK-002 — Attempt Updates from 1 → 2** | P1 | F
- **Given** an existing Task with `Process__c = "Notify Customer Of Service Update"` and `Attempt__c = 1`,
- **When** the Task is saved under the conditions that previously triggered the workflow rule,
- **Then** the Attempt field shall be updated to 2.

**AC-TASK-003 — Other Process Values Untouched** | P1 | N
- **Given** a Task whose `Process__c` is **not** "Notify Customer Of Service Update",
- **When** the Task is saved,
- **Then** the Attempt update logic shall not fire.

## 5.2 Draft Process Builder Verification

**AC-TASK-004 — Archived Draft Has No Effect** | P2 | R
- **Given** the legacy `Update_Case_for_Task_Process` was Draft/Inactive,
- **When** any Task event occurs that the draft process would have evaluated,
- **Then** there shall be no observable effect attributable to that legacy automation.

## 5.3 Genesys Task Routing (Cross-Object)

**AC-TASK-005 — Task Routes to Genesys** | P0 | I
- **Given** a Task that meets the Genesys routing criteria,
- **When** the Task is saved,
- **Then** a Task routing payload shall be transmitted exactly once to Genesys. *(See also AC-GR-002.)*

## 5.4 Bulk

**AC-TASK-006 — Bulk Task Insert** | P1 | B
- **Given** 200 Tasks are inserted in a single batch,
- **When** the batch commits,
- **Then** every qualifying Task shall have its Attempt field set correctly with no governor-limit errors.

### Sign-Off — Task
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-TASK-001 … 006 |
| Business Owner — Service Operations | | | |
| Integration Owner — Genesys | | | |

---

# 6. WORKORDER OBJECT

**In-Scope Source Automations:**
- Process Builder: `Work_Order_Process` (Draft — archive)
- Workflow Rule: `Integrate Work Order with Acorn` (Active)

## 6.1 Acorn Work Order Integration

**AC-WO-001 — Work Order Sent to Acorn on Create** | P0 | I
- **Given** a Work Order is created and `Acorn_WorkOrder_Id__c` is blank,
- **When** the Work Order is saved,
- **Then** a Work Order payload shall be transmitted exactly once to the Acorn endpoint.

**AC-WO-002 — No Re-Send When Acorn ID Already Populated** | P0 | N
- **Given** a Work Order whose `Acorn_WorkOrder_Id__c` is already populated,
- **When** the Work Order is saved,
- **Then** **no** payload shall be transmitted to Acorn for that save.

**AC-WO-003 — Bypass Validation Suppresses Send** | P1 | N
- **Given** the saving user has `User.Bypass_Validation__c = true`,
- **When** a Work Order would otherwise qualify for transmission,
- **Then** **no** payload shall be transmitted to Acorn.

**AC-WO-004 — Acorn Failure Logged, Save Succeeds** | P0 | I, N
- **Given** the Acorn endpoint is down or returns an error,
- **When** a qualifying Work Order is saved,
- **Then** the Work Order save itself shall succeed, the failure shall be logged, and the call shall be retryable.

**AC-WO-005 — Bulk Work Order Insert** | P0 | B, I
- **Given** 200 qualifying Work Orders are inserted,
- **When** the batch commits,
- **Then** every qualifying Work Order shall be transmitted to Acorn with no governor-limit errors and no dropped records.

## 6.2 Cross-Object & Draft Process Verification

**AC-WO-006 — Case → Work Order Status Sync Preserved** | P1 | R
- **Given** legacy logic that synchronized Work Order status from Case status changes,
- **When** the qualifying Case event occurs,
- **Then** the Work Order field shall update identically to pre-migration. *(Mirrors AC-CASE-014.)*

**AC-WO-007 — Archived Draft `Work_Order_Process` Has No Effect** | P2 | R
- **Given** the legacy `Work_Order_Process` Process Builder was Draft/Inactive,
- **When** any Work Order event occurs that the draft would have evaluated,
- **Then** there shall be no observable effect from the legacy automation.

### Sign-Off — WorkOrder
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-WO-001 … 007 |
| Business Owner — Field Service | | | |
| Integration Owner — Acorn | | | |

---

# 7. QUOTE OBJECT (SBQQ__Quote__c)

**In-Scope Source Automations:**
- Process Builder: `Update_To_Chatter_From_Quote` (Active)
- Workflow Rule: `Send Quote to API Hub` (Active)

## 7.1 API Hub / Acorn Integration

**AC-QUOTE-001 — Quote Sent to API Hub on Approval** | P0 | I
- **Given** a Quote whose `Acorn_integration_required__c` is true and meets the qualifying criteria,
- **When** the Quote status changes to "Approved",
- **Then** a Quote payload shall be transmitted exactly once to the API Hub endpoint.

**AC-QUOTE-002 — Manual Resync Flag Triggers Send** | P0 | I
- **Given** a Quote whose `DoResyncOutBoundcall__c` flag is set to true by a user,
- **When** the Quote is saved,
- **Then** a Quote payload shall be transmitted to the API Hub AND the `DoResyncOutBoundcall__c` flag shall be set back to false.

**AC-QUOTE-003 — Resync Flag Reset After Send** | P1 | I
- **Given** AC-QUOTE-002 has fired,
- **When** the user re-opens the Quote,
- **Then** `DoResyncOutBoundcall__c` shall display as false.

**AC-QUOTE-004 — No Send When Status Is Not Approved And Resync Flag False** | P1 | N
- **Given** a Quote that does not meet either trigger condition,
- **When** the Quote is saved,
- **Then** no payload shall be transmitted.

**AC-QUOTE-005 — API Hub Failure Logged, Save Succeeds** | P0 | I, N
- **Given** the API Hub endpoint is down or returns an error,
- **When** a qualifying Quote is saved,
- **Then** the Quote save shall succeed, the failure shall be logged, and the call shall be retryable.

## 7.2 Chatter Notification

**AC-QUOTE-006 — Chatter Post Created on Qualifying Quote Change** | P2 | F
- **Given** a Quote experiences the same status/field change that the legacy `Update_To_Chatter_From_Quote` reacted to,
- **When** the Quote is saved,
- **Then** a Chatter feed item shall be posted on the Quote with the same content/recipients as pre-migration.

## 7.3 Bulk

**AC-QUOTE-007 — Bulk Quote Approval** | P0 | B, I
- **Given** 200 Quotes are approved in a single batch,
- **When** the batch commits,
- **Then** every Quote shall be transmitted to API Hub with no governor-limit errors.

## 7.4 CPQ Lifecycle

**AC-QUOTE-008 — Quote-to-Order Process Unaffected** | P1 | R
- **Given** the standard Salesforce CPQ Quote-to-Order flow,
- **When** a Quote is approved end-to-end,
- **Then** Order generation, asset creation, and downstream CPQ behavior shall match pre-migration.

### Sign-Off — Quote
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-QUOTE-001 … 008 |
| Business Owner — Sales Operations | | | |
| CPQ SME | | | |
| Integration Owner — Acorn / API Hub | | | |

---

# 8. QUOTE LINE OBJECT (SBQQ__QuoteLine__c)

**In-Scope Source Automations:**
- Workflow Rule: `Update Exception Details` (Inactive — archive)

**AC-QL-001 — Archived Rule Has No Effect** | P2 | R
- **Given** the legacy `Update Exception Details` rule was Inactive,
- **When** any Quote Line event occurs,
- **Then** there shall be no observable behavior change attributable to that legacy rule.

**AC-QL-002 — Quote Line CPQ Lifecycle Unchanged** | P1 | R
- **Given** standard CPQ Quote Line operations (insert, update, delete, configuration),
- **When** any Quote Line event occurs,
- **Then** the system shall behave identically to pre-migration.

### Sign-Off — Quote Line
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-QL-001 … 002 |

---

# 9. BUSINESS RULE OBJECT (Business_Rule__c)

**In-Scope Source Automations:**
- Workflow Rule: `Business Rule Expiration` (Active, time-based)
- Workflow Rule: `BusinessRuleWorkFlowChannelReq` (Active)
- Workflow Rule: `BusinessRuleWorkFlowSpecailInstructions` (Active)
- Workflow Rule: `End Date in Past` (Active)
- Workflow Rule: `Update_Alias_BusinessRuleName` (Active)

## 9.1 Time-Based Expiration

**AC-BR-001 — Active Rule Deactivates One Day After End Date** | P0 | F
- **Given** a Business Rule with `Active__c = true` and `End_Date__c` set to a future date,
- **When** the system clock advances to one day past End Date,
- **Then** the Active flag shall be set to false automatically.

**AC-BR-002 — End Date Change Reschedules Deactivation** | P1 | F
- **Given** a scheduled deactivation is pending,
- **When** the End Date is updated to a new future date,
- **Then** the deactivation shall fire one day after the **new** End Date, not the original.

**AC-BR-003 — End Date Change Cancels Deactivation If Made Permanent** | P1 | F
- **Given** a scheduled deactivation is pending,
- **When** End Date is cleared or set to a date that no longer qualifies,
- **Then** the pending deactivation shall not fire.

**AC-BR-004 — Pending Time-Based Actions Migrated** | P0 | R
- **Given** Business Rules that had pending time-based actions queued **before** migration,
- **When** the system reaches their scheduled time **after** migration,
- **Then** every previously-queued deactivation shall fire as scheduled (no orphaned schedule).

## 9.2 Immediate End Date Validation

**AC-BR-005 — End Date In The Past Deactivates Immediately** | P1 | F, N
- **Given** a Business Rule is saved with `End_Date__c` < today,
- **When** the record is saved,
- **Then** the Active flag shall be set to false in the same save.

## 9.3 Channel Requirements & Special Instructions Flags

**AC-BR-006 — Channel Requirements Flag Set When Field Populated** | P1 | F
- **Given** a Business Rule's `Channel_Req__c` field is populated (any non-blank value),
- **When** the record is saved,
- **Then** `Is_Channel_Requirements__c` shall be true.

**AC-BR-007 — Special Instructions Flag Set When Field Populated** | P1 | F
- **Given** a Business Rule's `Special_Ins__c` field is populated,
- **When** the record is saved,
- **Then** `Is_Special_Instructions__c` shall be true.

## 9.4 Alias Defaulting

**AC-BR-008 — Alias Defaults To Name When Blank** | P1 | F
- **Given** a Business Rule is inserted (or cloned) with `Alias__c` blank,
- **When** the record is saved,
- **Then** `Alias__c` shall equal the `Name` field value.

## 9.5 Bulk

**AC-BR-009 — Bulk Business Rule Insert/Update** | P1 | B
- **Given** 200 Business Rules are inserted in a single batch,
- **When** the batch commits,
- **Then** all four field-update behaviors above shall apply to every qualifying record without governor-limit errors.

### Sign-Off — Business Rule
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-BR-001 … 009 |
| Business Owner — Operations / Business Rules Admin | | | |

---

# 10. COMMENT OBJECT (Comment__c)

**In-Scope Source Automations:**
- Workflow Rule: `Populate Acorn_SUser_ID__c` (Active)
- Workflow Rule: `Task Values to Acorn Invocation Rule` (Active)

## 10.1 Acorn User ID Defaulting

**AC-CMT-001 — Acorn SUser ID Defaulted From Running User** | P1 | F
- **Given** a Comment is created with `Acorn_SUser_ID__c` blank,
- **When** the Comment is saved,
- **Then** the field shall be populated with the running user's `Acorn_SUser_ID__c`.

**AC-CMT-002 — Existing Acorn SUser ID Preserved** | P1 | N
- **Given** a Comment is created with `Acorn_SUser_ID__c` already populated,
- **When** the Comment is saved,
- **Then** the existing value shall not be overwritten.

## 10.2 Acorn Outbound Integration

**AC-CMT-003 — Comment Sent to Acorn on Create** | P0 | I
- **Given** a Comment that meets the legacy "Task Values to Acorn" criteria,
- **When** the Comment is created,
- **Then** a payload shall be transmitted exactly once to Acorn.

**AC-CMT-004 — Acorn Tracking Number Change Re-Sends** | P1 | I
- **Given** an existing Comment whose `Acorn_Tracking_Number__c` changes,
- **When** the Comment is saved,
- **Then** an updated payload shall be transmitted to Acorn.

**AC-CMT-005 — Acorn Failure Handling** | P0 | I, N
- **Given** the Acorn endpoint is unavailable,
- **When** a qualifying Comment event occurs,
- **Then** the Comment save shall succeed, the failure shall be logged, and the call shall be retryable.

## 10.3 Bulk

**AC-CMT-006 — Bulk Comment Insert** | P1 | B
- **Given** 200 Comments are inserted in a single batch,
- **When** the batch commits,
- **Then** every qualifying Comment shall transmit to Acorn and have its Acorn SUser ID defaulted with no governor-limit errors.

### Sign-Off — Comment
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-CMT-001 … 006 |
| Business Owner — Service Operations | | | |
| Integration Owner — Acorn | | | |

---

# 11. CASE COMMENT OBJECT

**In-Scope Source Automations:**
- Workflow Rule: `Update CaseComment Createddate on Case` (Active)

**AC-CC-001 — Parent Case Reflects Case Comment Created Date** | P1 | F
- **Given** a Case Comment is added to a Case,
- **When** the Case Comment commits,
- **Then** the parent Case's `CaseComment_CreateDate__c` shall equal the Case Comment's CreatedDate.

**AC-CC-002 — Most-Recent Comment Date Wins** | P1 | F
- **Given** a Case has multiple Case Comments added in sequence,
- **When** each Case Comment commits,
- **Then** the parent Case's `CaseComment_CreateDate__c` shall reflect the same value the legacy rule would have produced (typically the most-recent comment's CreatedDate).

**AC-CC-003 — Bulk Case Comment Insert** | P1 | B
- **Given** 200 Case Comments are inserted across multiple Cases in one batch,
- **When** the batch commits,
- **Then** every parent Case shall reflect the correct CreatedDate without governor-limit errors.

### Sign-Off — Case Comment
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-CC-001 … 003 |
| Business Owner — Service Operations | | | |

---

# 12. ENTITLEMENT OBJECT

**In-Scope Source Automations:**
- Workflow Rule: `Update Entitlement Name` (Active)

**AC-ENT-001 — Entitlement Name Auto-Generated** | P1 | F
- **Given** an Entitlement is created or updated where its driving fields are populated (Account, Service, Service Guarantee Category, etc.),
- **When** the record is saved,
- **Then** the `Name` field shall be set to the same value the legacy formula produced for the same input.

**AC-ENT-002 — Entitlement Name Recalculates on Driving Field Change** | P1 | F
- **Given** an existing Entitlement,
- **When** any driving field changes,
- **Then** the `Name` field shall recalculate to match the legacy formula's output.

**AC-ENT-003 — Bulk Entitlement Insert** | P1 | B
- **Given** 200 Entitlements are inserted (e.g., from Account activation per AC-ACCT-005),
- **When** the batch commits,
- **Then** every Entitlement shall have a correctly-formatted Name with no governor-limit errors.

**AC-ENT-004 — Entitlement Naming Coexists With Other Entitlement Logic** | P2 | R
- **Given** any other Entitlement-side logic in place,
- **When** an Entitlement is created/updated,
- **Then** downstream behavior on that Entitlement shall match pre-migration.

### Sign-Off — Entitlement
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-ENT-001 … 004 |
| Business Owner — Service Contracts | | | |

---

# 13. ACCOUNT TITLE OBJECT (Account_Title__c)

**In-Scope Source Automations:**
- Workflow Rule: `Avoid duplicate account title` (Active)

**AC-AT-001 — Duplicate Title Field Concatenates Name + Account ID** | P1 | F
- **Given** an Account Title record is created or updated,
- **When** the record is saved,
- **Then** `Duplicate_Title__c` shall equal `Name` concatenated with the related Account's Id (matching the legacy rule's exact format).

**AC-AT-002 — Duplicate Title Recalculates on Name or Account Change** | P1 | F
- **Given** an existing Account Title,
- **When** the Name or Account relationship changes,
- **Then** `Duplicate_Title__c` shall recalculate accordingly.

**AC-AT-003 — Bulk Account Title Insert** | P1 | B
- **Given** 200 Account Titles are inserted in a single batch,
- **When** the batch commits,
- **Then** every record shall have the correct `Duplicate_Title__c` value.

### Sign-Off — Account Title
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-AT-001 … 003 |
| Business Owner — Account Administration | | | |

---

# 14. NOTIFICATION CONTACT OBJECT (Notification_Contact__c)

**In-Scope Source Automations:**
- Workflow Rule: `Adding contact mobile phone` (Active)

**AC-NC-001 — ISD Phone Formatted With Country Prefix** | P1 | F
- **Given** a Notification Contact is created/updated and the related Contact has a Mobile Phone value,
- **When** the record is saved,
- **Then** `ISD_Phone__c` shall equal `"+1"` concatenated with the related Contact's Mobile Phone.

**AC-NC-002 — Blank Mobile Phone Handled Gracefully** | P2 | N
- **Given** the related Contact has no Mobile Phone value,
- **When** a Notification Contact is saved,
- **Then** the system shall behave identically to pre-migration (e.g., `ISD_Phone__c` blank or `"+1"` only — whichever the legacy rule produced).

**AC-NC-003 — ISD Phone Updates When Contact's Mobile Phone Changes** | P2 | F
- **Given** the related Contact's Mobile Phone is updated,
- **When** the related Notification Contact is re-saved (or via the same trigger pattern as pre-migration),
- **Then** `ISD_Phone__c` shall reflect the new value.

**AC-NC-004 — Bulk Notification Contact Insert** | P2 | B
- **Given** 200 Notification Contacts are inserted in a batch,
- **When** the batch commits,
- **Then** every record shall have a correctly-formatted `ISD_Phone__c`.

### Sign-Off — Notification Contact
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-NC-001 … 004 |
| Business Owner — Customer Communications | | | |

---

# 15. GENESYS ROUTING OBJECT (Genesys_Routing__c)

**In-Scope Source Automations:**
- Workflow Rule: `Email to Case Genesys Routing` (Active, 20+ field outbound)
- Workflow Rule: `Task Genesys Routing Payload` (Active, 25+ field outbound)

**AC-GR-001 — Email-to-Case Genesys Routing Payload Sent** | P0 | I
- **Given** a Genesys Routing record is created with the email-to-case record type and qualifying media type,
- **When** the record is saved,
- **Then** the full email-to-case routing payload shall be transmitted exactly once to Genesys, containing the same set of fields and values as pre-migration.

**AC-GR-002 — Task Genesys Routing Payload Sent** | P0 | I
- **Given** a Task-related Genesys Routing record qualifies for routing,
- **When** the record is saved,
- **Then** the full Task routing payload shall be transmitted exactly once to Genesys.

**AC-GR-003 — Payload Field Parity (Email Routing)** | P0 | I
- **Given** a routing event is captured pre- and post-migration for the same input data,
- **When** the payloads are compared,
- **Then** every field name and value in the post-migration payload shall match the pre-migration payload (no missing or added fields).

**AC-GR-004 — Payload Field Parity (Task Routing)** | P0 | I
- **Given** a Task routing event is captured pre- and post-migration for the same input data,
- **When** the payloads are compared,
- **Then** every field shall match exactly.

**AC-GR-005 — Genesys Failure Handling** | P0 | I, N
- **Given** the Genesys endpoint is unavailable or returns an error,
- **When** a qualifying routing event fires,
- **Then** the failure shall be logged, the originating Salesforce record save shall succeed, and the routing shall be retryable.

**AC-GR-006 — Bulk Routing Throughput** | P0 | B, I, P
- **Given** 200 routing-eligible records are saved in a single batch,
- **When** the batch commits,
- **Then** every record shall transmit a routing payload to Genesys with no governor-limit errors and within the established throughput baseline.

### Sign-Off — Genesys Routing
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-GR-001 … 006 |
| Business Owner — Contact Center Operations | | | |
| Integration Owner — Genesys | | | |

---

# 16. GENESYS REPORTING OBJECT (Genesys_Reporting__c)

**In-Scope Source Automations:**
- Workflow Rule: `Send to Genesys Reporting` (Active)

**AC-GREP-001 — Reporting Payload Sent on Create** | P1 | I
- **Given** a Genesys Reporting record is created,
- **When** the record is saved,
- **Then** a reporting payload shall be transmitted exactly once to the Genesys reporting endpoint.

**AC-GREP-002 — Reporting Failure Handling** | P1 | I, N
- **Given** the Genesys reporting endpoint is unavailable,
- **When** a Genesys Reporting record is saved,
- **Then** the failure shall be logged and the call shall be retryable; the Salesforce save shall succeed.

**AC-GREP-003 — Bulk Reporting Throughput** | P1 | B, I
- **Given** 200 Genesys Reporting records are inserted,
- **When** the batch commits,
- **Then** every record shall transmit successfully with no governor-limit errors.

### Sign-Off — Genesys Reporting
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-GREP-001 … 003 |
| Business Owner — Contact Center Analytics | | | |
| Integration Owner — Genesys | | | |

---

# 17. SUPPLIER OBJECT

**In-Scope Source Automations:**
- Process Builder: `Supplier_Score_Trending` (Active)

**AC-SUP-001 — Supplier Score Calculated on Save** | P1 | F
- **Given** a Supplier record with the input fields used by the legacy scoring logic,
- **When** the record is saved,
- **Then** the calculated score field shall match the value the legacy logic produced for the same input (validated against pre-migration parallel-run dataset).

**AC-SUP-002 — Trending Indicator Reflects Direction Of Change** | P1 | F
- **Given** a Supplier whose score changes between two consecutive saves,
- **When** the second save commits,
- **Then** the trending indicator field shall reflect "up", "down", or "flat" exactly as the legacy logic did.

**AC-SUP-003 — Date-Based Calculations Honor System Date** | P1 | F
- **Given** the legacy logic uses date-based math (e.g., score over time window),
- **When** the same calculation runs post-migration,
- **Then** results shall match for the same input date.

**AC-SUP-004 — Bulk Supplier Update** | P1 | B
- **Given** 200 Supplier records updated in a single batch,
- **When** the batch commits,
- **Then** every record shall have correctly-calculated score and trend without governor-limit errors.

**AC-SUP-005 — Historical Trending Continuity** | P1 | R
- **Given** Suppliers that had historical trend data captured pre-migration,
- **When** post-migration runs continue from that data,
- **Then** historical trend continuity shall be preserved (no reset, no gap).

### Sign-Off — Supplier
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-SUP-001 … 005 |
| Business Owner — Supplier Management | | | |

---

# 18. VENDOR SERVICE LOCATION OBJECT

**In-Scope Source Automations:**
- Process Builder: `Delete_Vendor_Service_Location_Code` (Draft — archive)

**AC-VSL-001 — Archived Draft Has No Effect** | P2 | R
- **Given** the legacy `Delete_Vendor_Service_Location_Code` Process Builder was Draft/Inactive,
- **When** any Vendor Service Location event occurs that the draft would have evaluated,
- **Then** there shall be no observable effect (specifically: no records shall be auto-deleted by the legacy logic).

**AC-VSL-002 — Standard CRUD Unaffected** | P2 | R
- **Given** standard create / read / update / delete operations on Vendor Service Location records,
- **When** those operations occur,
- **Then** the system shall behave identically to pre-migration.

### Sign-Off — Vendor Service Location
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-VSL-001 … 002 |

---

# 19. SFDC EMAIL MESSAGE OBJECT (SFDCEmailMessage__c)

**In-Scope Source Automations:**
- Workflow Rule: `Send to Indico` (Inactive — archive)

**AC-SEM-001 — Archived Indico Rule Has No Effect** | P2 | R
- **Given** the legacy `Send to Indico` rule was Inactive,
- **When** any SFDCEmailMessage event occurs,
- **Then** there shall be no observable effect attributable to that legacy rule (Indico processing is now handled exclusively via the EmailMessage object — see AC-EM-003).

**AC-SEM-002 — Standard CRUD Unaffected** | P2 | R
- **Given** standard CRUD on SFDCEmailMessage records,
- **When** those operations occur,
- **Then** the system shall behave identically to pre-migration.

### Sign-Off — SFDC Email Message
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-SEM-001 … 002 |

---

# CROSS-CUTTING ACCEPTANCE CRITERIA (All Objects)

These ACs are not owned by a single object but must be validated as part of overall sign-off. Each one is a **regression-style** AC that protects the system as a whole.

**AC-X-001 — No Active Legacy Automation Remains** | P0 | R
- **Given** the migration is declared complete,
- **When** the org's automation inventory is exported,
- **Then** every Workflow Rule and Process Builder that was in scope shall be either Inactive or removed from the metadata.

**AC-X-002 — No Duplicate Effect From Old + New Logic** | P0 | R
- **Given** a single record save event,
- **When** the event fires,
- **Then** every field update shall occur exactly once (verified by field history / audit trail showing one transition, not two).

**AC-X-003 — No Outbound Message Fires Twice** | P0 | I, R
- **Given** any in-scope outbound integration (Acorn, Genesys, API Hub, Indico, SMS),
- **When** a single qualifying event occurs,
- **Then** the corresponding outbound payload shall transmit exactly once.

**AC-X-004 — Order Of Execution Stable** | P1 | R
- **Given** any save involving multiple in-scope automations on the same object,
- **When** the save commits,
- **Then** the final field values shall match pre-migration values for identical input data (i.e., no race-condition reordering produces different results).

**AC-X-005 — Bulk Load Of 200 Records Succeeds For Every Object** | P0 | B, P
- **Given** a 200-record DML on each in-scope object,
- **When** each batch commits,
- **Then** zero limit-exceeded exceptions shall be raised on any object.

**AC-X-006 — Performance Equal-Or-Better Vs Baseline** | P1 | P
- **Given** a documented pre-migration performance baseline (single-record save time, bulk save time),
- **When** the same operations are measured post-migration,
- **Then** every measurement shall be within 10% of, or better than, the baseline.

**AC-X-007 — Error Visibility For Integrations** | P0 | I
- **Given** any in-scope integration call,
- **When** that call fails,
- **Then** the failure shall be visible to a tester / support engineer through a documented log location, not silently swallowed.

**AC-X-008 — Retry Mechanism Documented & Functional** | P1 | I
- **Given** any in-scope integration call has failed and been logged,
- **When** the documented retry procedure is executed,
- **Then** the call shall succeed (assuming the downstream system is now healthy).

**AC-X-009 — Pending Time-Based Schedules Migrated Without Loss** | P0 | R
- **Given** any time-based schedule (e.g., Business Rule Expiration) had pending entries pre-migration,
- **When** the migration is complete,
- **Then** every pending schedule shall fire at its originally-scheduled time.

**AC-X-010 — User Notifications Continuity** | P2 | R
- **Given** any user-facing notification (Chatter, Tasks, emails) that legacy automation produced,
- **When** the same triggering condition occurs post-migration,
- **Then** the notification shall be delivered to the same user(s) with equivalent content.

**AC-X-011 — Permission / Profile Sensitivity Preserved** | P1 | R
- **Given** legacy automation that behaved differently for certain users (e.g., System Admin only, Bypass Validation flag),
- **When** users with those attributes save records post-migration,
- **Then** the same conditional behavior shall apply.

**AC-X-012 — Rollback Plan Verified** | P0 | R
- **Given** the migration's documented rollback plan,
- **When** rollback is dry-run-tested in a sandbox environment,
- **Then** the system shall return to its pre-migration functional state with no data loss.

### Sign-Off — Cross-Cutting
| Role | Name | Date | AC IDs Signed |
|---|---|---|---|
| QA Lead | | | AC-X-001 … 012 |
| Release Manager | | | |
| Technical Architect | | | |

---

# OVERALL PROJECT SIGN-OFF

The migration is considered **functionally complete** only when every per-object section above is signed off **and** the Cross-Cutting section is signed off.

| Sign-Off Item | Status | Date |
|---|---|---|
| All 19 object sections signed off | ☐ | |
| Cross-Cutting section signed off | ☐ | |
| Performance baseline met (AC-X-006) | ☐ | |
| Integration error visibility verified (AC-X-007) | ☐ | |
| Rollback plan dry-run verified (AC-X-012) | ☐ | |
| **MIGRATION COMPLETE — APPROVED FOR PRODUCTION** | ☐ | |

| Final Approver | Role | Signature | Date |
|---|---|---|---|
| | QA Director | | |
| | Technical Architect | | |
| | Business Sponsor | | |
| | Release Manager | | |

---

## Appendix A — Traceability Matrix (Object → Source Automation → AC IDs)

| Object | Legacy Automation | AC IDs |
|---|---|---|
| Case | Send Acorn New Case Information (WR) | AC-CASE-005 … 011 |
| Case | Set Reference Number (WR) | AC-CASE-001 … 004 |
| Case | Case_Update_Process (PB, draft) | AC-CASE-012 |
| Case | 15 inactive WRs | AC-CASE-013 |
| Account | Create_SLA_upon_activating_Account (PB) | AC-ACCT-001 … 006 |
| Contact | Populate_Preferred_Language_from_Contact_to (PB) | AC-CONT-001 … 003 |
| Contact | Update_Text_Notification_Opt_In (PB) | AC-CONT-004 … 007 |
| Contact | 2 inactive WRs | AC-CONT-008 |
| EmailMessage | Email_to_Case (PB) | AC-EM-001 … 007, 010 … 012 |
| EmailMessage | EMailMessageUpdate (PB) | AC-EM-008 … 009 |
| Task | Update Attempt for Notify Customer… (WR) | AC-TASK-001 … 003 |
| Task | Update_Case_for_Task_Process (PB, draft) | AC-TASK-004 |
| WorkOrder | Integrate Work Order with Acorn (WR) | AC-WO-001 … 005 |
| WorkOrder | Work_Order_Process (PB, draft) | AC-WO-007 |
| Quote | Send Quote to API Hub (WR) | AC-QUOTE-001 … 005, 007 |
| Quote | Update_To_Chatter_From_Quote (PB) | AC-QUOTE-006 |
| Quote Line | Update Exception Details (WR, inactive) | AC-QL-001 … 002 |
| Business Rule | All 4 active WRs | AC-BR-001 … 009 |
| Comment | Populate Acorn_SUser_ID__c (WR) | AC-CMT-001 … 002 |
| Comment | Task Values to Acorn (WR) | AC-CMT-003 … 005 |
| Case Comment | Update CaseComment Createddate on Case (WR) | AC-CC-001 … 003 |
| Entitlement | Update Entitlement Name (WR) | AC-ENT-001 … 004 |
| Account Title | Avoid duplicate account title (WR) | AC-AT-001 … 003 |
| Notification Contact | Adding contact mobile phone (WR) | AC-NC-001 … 004 |
| Genesys Routing | Email to Case Genesys Routing (WR) | AC-GR-001, 003, 005 … 006 |
| Genesys Routing | Task Genesys Routing Payload (WR) | AC-GR-002, 004, 005 … 006 |
| Genesys Reporting | Send to Genesys Reporting (WR) | AC-GREP-001 … 003 |
| Supplier | Supplier_Score_Trending (PB) | AC-SUP-001 … 005 |
| Vendor Service Location | Delete_Vendor_Service_Location_Code (PB, draft) | AC-VSL-001 … 002 |
| SFDC Email Message | Send to Indico (WR, inactive) | AC-SEM-001 … 002 |

---

## Appendix B — Notes For Test Case Authors

1. **Build a parallel-run dataset.** For every active automation, capture pre-migration before/after field values for a representative sample of records. Replay the same inputs post-migration and diff. Any divergence is a defect.
2. **Snapshot outbound payloads.** For Acorn, Genesys, API Hub, Indico, and SMS calls, capture the exact request body pre-migration (sandbox or via recorded mocks). Diff the post-migration payload byte-for-byte where feasible (AC-GR-003, AC-GR-004 explicitly require this).
3. **Don't assert on automation type.** If an AC is failing because "the Workflow Rule no longer exists" — that's expected. The AC must be re-tested against the new implementation; only the *function* matters.
4. **Use the Test Type tags (F/B/N/I/R/P)** to plan coverage. Every object should have at least one F, one B, and (where relevant) one I and one N test case.
5. **Bulk tests use 200 records** by convention (Salesforce bulk-trigger boundary). Larger volumes are encouraged for performance ACs.

---

**End of Document.**
