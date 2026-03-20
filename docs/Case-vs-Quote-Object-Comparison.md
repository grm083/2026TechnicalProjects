# Case vs. SBQQ__Quote__c: Monolith Comparison Analysis

> **Date:** March 20, 2026
> **Scope:** Full codebase analysis of object metadata, Apex, LWC, Aura, Flows, and test infrastructure
> **Volume Reference:** Since January 1, 2025 — **918,841 Cases** | **111,528 Quotes**

---

## Executive Summary

Case and SBQQ__Quote__c are the two largest object ecosystems in this org. Despite serving different business functions, both have grown into monolithic pillars with extensive custom code, integrations, and UI components. This analysis compares them across architecture, code quality, UI modernization, automation, testing, and operational maturity to identify where each excels and where each needs investment.

**Bottom line:** Case is the higher-volume, broader workhorse with more UI surface area but weaker architectural discipline. Quote is the more architecturally intentional system with better separation of concerns and test investment, but suffers from God-class controllers and fragile edge-case handling in its approval engine.

---

## 1. Object Footprint at a Glance

| Dimension | Case | SBQQ__Quote__c | Verdict |
|-----------|------|-----------------|---------|
| **Custom Fields** | 321 | 154 | Case is 2x larger in schema surface |
| **Record Types** | 11 | 1 | Case has far more operational variants |
| **Validation Rules** | 14 | 14 | Parity |
| **Page Layouts** | 11 | 1 | Case has layout sprawl; Quote is consolidated |
| **List Views** | 7 | 19 | Quote has significantly more curated views |
| **Quick Actions** | — | 14 | Quote has a rich action palette; Case relies on overrides |
| **Permission Sets** | — | 9+ (dedicated) | Quote has granular, role-based security |
| **Field Sets** | 1 | 3 | Quote leverages CPQ field sets properly |
| **Volume (since Jan 2025)** | 918,841 | 111,528 | Case handles 8.2x the transaction volume |
| **Volume per Field** | 2,862 records/field | 724 records/field | Case fields work harder per-record |

---

## 2. Apex Ecosystem Comparison

### 2a. Scale

| Metric | Case | SBQQ__Quote__c |
|--------|------|-----------------|
| **Apex Triggers** | 5 | 4 |
| **Production Apex Classes** | 85+ | 70 |
| **Estimated Production Lines** | ~28,228 | ~36,883 |
| **Test Classes** | 38 | 32+ |
| **Estimated Test Lines** | ~9,150 (sampled) | ~36,706 |
| **Test:Production Ratio** | ~1.16:1 | ~4.25:1 |
| **Largest Single Class** | GetCaseInformation (2,762 lines) | QuoteProcurementController (5,642 lines) |

### 2b. Architecture Quality

| Criterion | Case | SBQQ__Quote__c |
|-----------|------|-----------------|
| **Trigger Handler Pattern** | Yes (TriggerDispatcher) | Yes (handler with CPQ integration) |
| **Single Trigger per Object** | **No** — 5 triggers (violation) | **No** — 4 triggers (violation) |
| **Selector Layer** | **None** | Yes (QuoteSelector, QuoteLineSelector) |
| **Service Layer** | **None** | Partial (QuoteLineServices) |
| **Domain Layer** | **None** | **None** |
| **Recursion Guards** | Yes (RecurrsiveTriggerHandler) | Yes (same framework + SBQQ.TriggerControl) |
| **Exception Handling** | Broad catch-all, exposes stack traces | Structured logging via UTIL_LoggingService |
| **Static Variable Hygiene** | **Poor** — public static maps on Handler | **Moderate** — global state in QuoteApproval |

### 2c. Code Smell Comparison

| Smell | Case | SBQQ__Quote__c |
|-------|------|-----------------|
| **God Classes** | GetCaseInformation (2,762 lines, 15+ methods mixing UI/service/domain) | QuoteProcurementController (5,642 lines, 50+ methods) — **worse** |
| **SOQL in Loops** | CaseController line 342 (Database.query in asset loop) | QuoteProcurementController lines 107-118, 281, 436-450 — **worse, multiple instances** |
| **Hard-coded Strings** | Moderate (record type names, statuses) | **Heavy** — 50+ magic strings ('FRCH', 'SOC', 'SCH', 'STP', 'REB', 'D', 'M', 'Y', 'W') |
| **Missing Bulkification** | Some areas | QuoteProcurementController lines 52-61, 107-109, 149-153 — **worse** |
| **Unsafe Array Access** | Not observed | QuoteApproval line 1440 (`approvalLogs[0]` without size check) — **NPE risk** |
| **Dynamic SOQL** | CaseController lines 342, 461 | Not observed — **Case is worse here** |

---

## 3. UI Component Comparison

### 3a. Component Inventory

| Component Type | Case | SBQQ__Quote__c |
|----------------|------|-----------------|
| **LWC Components** | 3 | 4 |
| **Aura Components** | 45 | 11 |
| **Total UI Components** | 48 | 15 |
| **LWC:Aura Ratio** | 1:15 (6.3% LWC) | 1:2.75 (27% LWC) |

### 3b. Modernization Assessment

| Criterion | Case | SBQQ__Quote__c |
|-----------|------|-----------------|
| **LWC Adoption** | **Minimal** — 3 components, mostly supplementary | **Better** — 4 components including the primary quoteOrderComp (2,445 lines) |
| **LWC Quality** | Modern syntax (@wire, @track, @api, MessageContext) | Modern syntax with async patterns; minor setTimeout anti-pattern |
| **Aura Helper/Controller Separation** | 86% compliance | ~100% compliance |
| **Aura Technical Debt** | **Heavy** — 45 components is a large legacy surface | **Moderate** — 11 components, manageable migration scope |
| **Action Override** | CaseCreationComponent (Aura) overrides New action | CPQ standard buttons (EditLines, GenerateDocument, etc.) |

**Key Insight:** Case has 3x more Aura components to eventually migrate to LWC. Quote started smaller and has a higher LWC adoption ratio, making it better positioned for the Aura-to-LWC transition.

---

## 4. Automation & Flow Comparison

| Dimension | Case | SBQQ__Quote__c |
|-----------|------|-----------------|
| **Flows** | 3 | 9 |
| **Largest Flow** | Case_Update_Process (6,096 lines) | Quote_Status_Change_Flow |
| **Flow Complexity** | 1 massive flow + 2 supporting | 9 focused, single-purpose flows |
| **Platform Events** | CasetoQuoteAutomation__e (produces) | CasetoQuoteAutomation__e (consumes) |
| **Batch Jobs** | 6+ (delete, purge, status update, Genesys, email linking, escalation close) | 3 (Genesys creation, priority change) |
| **Scheduled Jobs** | Multiple (purge, status, Genesys) | 2 (Genesys, priority) |

**Key Insight:** Case has a single monolithic flow (Case_Update_Process at 6,096 lines) that is a maintenance risk. Quote's 9 smaller, purpose-built flows are healthier. However, Case has more batch infrastructure reflecting its higher operational volume.

---

## 5. Integration Landscape

| Integration | Case | SBQQ__Quote__c |
|-------------|------|-----------------|
| **Acorn** | Full bi-directional (create, reassign, reopen) | Read-only status tracking (5 fields) |
| **Genesys** | Task creation for PI tasks | Full routing integration (routing records, user assignment) |
| **OfficeTrax** | Case import and field locking | — |
| **CPQ Engine** | — | Deep integration (SBQQ.TriggerControl, calculation engine, document generation) |
| **MAS System** | — | Make-to-order library integration |
| **Work Orders** | Auto-creation from cases | — |
| **Platform Events** | Producer (CasetoQuoteAutomation__e) | Consumer |
| **REST APIs** | AcornCaseDetailsResource, CreatePickupCaseAPI, GetIVRCasePrompt | — |
| **Email Handlers** | CaseApprovalHandler (inbound) | QuoteApprovalHandler, QuoteEmailHandler (inbound) |

**Key Insight:** Case has broader external integration surface (Acorn, OfficeTrax, REST APIs, IVR). Quote has deeper integration with internal Salesforce systems (CPQ engine, MAS). Both share Genesys and cross-connect via platform events.

---

## 6. Testing Maturity

| Metric | Case | SBQQ__Quote__c |
|--------|------|-----------------|
| **Test:Production Ratio** | ~1.16:1 | ~4.25:1 |
| **Test Classes** | 38 | 32+ |
| **Missing Test Coverage** | **CaseController.cls (569 lines) — NO test class** | No obvious gaps in class-level coverage |
| **Test Granularity** | Mostly 1:1 mapping | Multiple test classes per production class (approval scenarios) |
| **Edge Case Coverage** | Not assessed | **Poor** — QuoteApproval has NPE risks at lines 60, 1440 |
| **Test Data Strategy** | Direct DML in tests | Direct DML in tests |

**Key Insight:** Quote invests significantly more in test volume (4.25:1 ratio vs 1.16:1). However, Case has a critical gap with an entirely untested controller class. Quote's higher test volume masks quality concerns — many edge cases in the approval engine remain uncovered.

---

## 7. Scorecard

| Category | Case | Quote | Notes |
|----------|------|-------|-------|
| **Schema Design** | C+ | B | Case has field sprawl (321); Quote is leaner and better organized |
| **Record Type Strategy** | B+ | C | Case has 11 purpose-specific types; Quote has only 1, limiting workflow flexibility |
| **Validation Rules** | B | B | Both at 14, reasonable coverage |
| **Trigger Architecture** | C | B- | Both violate single-trigger rule; Quote has better error logging |
| **Separation of Concerns** | D | C+ | Case has zero architectural layers; Quote has selectors + partial services |
| **God Class Risk** | D+ | D | Both have massive classes; Quote's is twice as large (5,642 vs 2,762 lines) |
| **SOQL Hygiene** | C- | D+ | Both have issues; Quote has more SOQL-in-loop instances |
| **Test Investment** | C+ | A- | Quote's 4.25:1 ratio is strong; Case has a fully untested controller |
| **LWC Modernization** | D+ | C+ | Both lag, but Quote's higher LWC ratio and smaller Aura footprint are advantages |
| **Aura Quality** | B | B+ | Both have good helper/controller separation |
| **Flow Architecture** | D+ | B+ | Case's single 6K-line flow is a liability; Quote has 9 focused flows |
| **Integration Maturity** | B+ | B | Case has broader integration surface; both are functional |
| **Operational Scale** | A | B | Case handles 8.2x volume; its infrastructure reflects that |
| **Permission Model** | C | A- | Quote has 9+ dedicated permission sets; Case lacks granular security |
| **Quick Actions / UX** | C | B+ | Quote has 14 purpose-built quick actions; Case relies on overrides |

---

## 8. Where Each Object is Doing Well

### Case Strengths
1. **Volume handling at scale** — 918,841 records since Jan 2025, supported by 6+ batch jobs for lifecycle management (purge, status updates, email linking)
2. **Record type strategy** — 11 record types enable distinct workflows for Pickup, New Service, Repair, Interruption, Integration, Vendor, etc.
3. **Integration breadth** — Bi-directional Acorn integration, OfficeTrax sync, REST APIs for external consumption, IVR prompt generation
4. **Aura component richness** — 45 components provide comprehensive UI coverage for case creation, asset management, SLA tracking, task assignment, and team views
5. **Business process coverage** — Validation rules, SLA/entitlement calculations, and work order auto-creation form a complete service management lifecycle

### Quote Strengths
1. **Architectural intentionality** — Selector layer (QuoteSelector, QuoteLineSelector), service layer (QuoteLineServices), and structured exception logging show deliberate design
2. **Test investment** — 4.25:1 test-to-production ratio with scenario-specific test classes (bundle auto, bundle manual, multiple BR, two approvers)
3. **Flow architecture** — 9 focused, single-purpose flows vs. monolithic process builders; clean separation of status changes, assignment, routing, and locking
4. **Permission granularity** — 9+ dedicated permission sets (Read Only, Approval, Cost Accessibility, Price Accessibility, MAS Integration, Lifecycle Management)
5. **Quick action palette** — 14 purpose-built actions (Approve, Decline, Escalate, Cancel, Assign to Me, Pending Information, Resync) provide a rich user experience
6. **CPQ platform leverage** — Proper use of SBQQ.TriggerControl, field sets, and CPQ calculation engine rather than reinventing pricing logic
7. **Higher LWC adoption ratio** — 27% LWC (vs. Case's 6.3%) with a smaller Aura migration burden (11 vs. 45 components)

---

## 9. Where Each Object is Doing Poorly

### Case Weaknesses
1. **Zero architectural layering** — No selectors, no services, no domain classes. Business logic, SOQL, and DML are mixed freely across controllers and helpers
2. **God class problem** — GetCaseInformation.cls (2,762 lines) has 15+ public methods mixing UI rendering, data retrieval, work order initiation, and file operations
3. **Untested controller** — CaseController.cls (569 lines with DML, dynamic SOQL, and business logic) has **no test class at all**
4. **5 triggers on one object** — CaseTrigger, CaseCommentTrigger, CaseAssetTrigger, CasetoQuoteAutomation, CaseHistoryTrackerTrigger violate single-trigger-per-object best practice
5. **Monolithic flow** — Case_Update_Process at 6,096 lines is a maintenance and debugging nightmare
6. **Static variable pollution** — CaseTriggerHandler exposes public static Maps that risk data leakage across transactions
7. **Dynamic SOQL** — CaseController uses Database.query() with string interpolation (lines 342, 461) instead of static SOQL
8. **LWC adoption** — Only 3 LWC components out of 48 total (6.3%); 45 Aura components represent a massive migration backlog
9. **No permission model** — Lacks dedicated permission sets; access control is likely managed through profiles alone
10. **Broad exception handling** — Catches generic Exception and returns raw stack traces to the UI

### Quote Weaknesses
1. **Largest God class in the org** — QuoteProcurementController.cls at 5,642 lines with 50+ public methods is the single biggest monolith in the codebase
2. **Pervasive SOQL-in-loops** — Lines 107-118, 281, 436-450 of QuoteProcurementController execute queries inside loops; N+1 query problem
3. **50+ hard-coded magic strings** — Occurrence types ('SOC', 'SCH'), frequencies ('D', 'M', 'Y', 'W'), cost models ('STP', 'REB'), and more scattered without constants
4. **Fragile approval engine** — QuoteApproval.cls has unsafe array access at line 1440 (`approvalLogs[0]` without size check), missing null checks at lines 60, 76, 80, and empty catch blocks
5. **Missing bulkification** — Multiple `SELECT ... WHERE Id = :single_id` patterns in QuoteProcurementController (lines 52-61, 149-153)
6. **Single record type** — Only "New_Service" record type limits the ability to create distinct page layouts, validation rules, and workflows for different quote scenarios
7. **Global static state in approvals** — QuoteApproval.cls (lines 13-37) maintains static Maps that persist across calls, risking state corruption in batch contexts
8. **Test volume masks quality gaps** — Despite 4.25:1 ratio, edge cases like empty approval logs, null business rules, and circular approver dependencies are untested
9. **Unbounded SOQL** — Multiple queries without LIMIT clauses on custom metadata and custom object tables (lines 281, 590, 619, 678, 749, 799, 834, 854, 889)

---

## 10. Recommendations

### Shared Priorities (Both Objects)
1. **Consolidate to single trigger per object** — Merge all trigger logic into CaseTrigger/QuoteTrigger dispatchers
2. **Break up God classes** — Extract domain-specific services from GetCaseInformation and QuoteProcurementController
3. **Centralize constants** — Create `CaseConstants.cls` and `QuoteConstants.cls` for all magic strings
4. **Eliminate SOQL in loops** — Batch-collect IDs, query once outside the loop, then map results

### Case-Specific
5. **Add architectural layers** — Introduce CaseSelector, CaseService, and CaseDomain classes
6. **Write tests for CaseController.cls** — 569 lines of untested DML and dynamic SOQL is a deployment risk
7. **Decompose Case_Update_Process flow** — Split the 6,096-line flow into focused sub-flows
8. **Accelerate LWC migration** — Prioritize the 10 most-used Aura components for conversion
9. **Implement permission sets** — Create granular access controls similar to Quote's model
10. **Replace dynamic SOQL** — Convert Database.query() calls to static SOQL with bind variables

### Quote-Specific
11. **Refactor QuoteProcurementController** — Extract vendor management, pricing, MAS integration, and validation into separate classes
12. **Fix QuoteApproval null safety** — Add size checks before array access, validate business rule matches, add null guards
13. **Add record types** — Consider types for Amendment, Exception, Correction, and Quote-Only to enable layout and rule segmentation
14. **Remove empty catch blocks** — Ensure all exceptions route through UTIL_LoggingService
15. **Add LIMIT clauses** — Cap unbounded metadata queries to prevent governor limit issues at scale

---

## Appendix: Volume Context

With **918,841 Cases** generated since January 1, 2025 (roughly **2,400/day**), every Case code path — trigger, flow, batch — executes at massive scale. Performance anti-patterns like SOQL-in-loops and dynamic queries carry proportionally higher risk on Case than on Quote.

With **111,528 Quotes** in the same period (~**305/day**), Quote's volume is 1/8th of Case. However, each Quote transaction is more computationally expensive due to CPQ calculation engine invocations, multi-level approval routing, and procurement workflows. The fragile approval edge cases in QuoteApproval.cls are therefore more likely to surface under load than raw volume alone would suggest.

| Metric | Case | SBQQ__Quote__c |
|--------|------|-----------------|
| Records since Jan 2025 | 918,841 | 111,528 |
| Estimated daily volume | ~2,400 | ~305 |
| Apex classes touched per transaction | 5-8 (trigger chain) | 8-12 (trigger + CPQ + approval) |
| Governor limit exposure | High (volume) | High (complexity per transaction) |
