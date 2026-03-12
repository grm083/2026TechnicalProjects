# Segregation of Duties: Granular Permission Set Specification

**Document Type:** Technical Specification
**Version:** 1.0
**Date:** March 12, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT — Ready for Review
**Purpose:** Break down feature-based permission sets into granular, SoD-compliant access points. Each permission set is defined by the specific fields, objects, Apex classes, and user permissions it controls.

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [SoD Framework](#sod-framework)
3. [Permission Set Inventory](#permission-set-inventory)
4. [Feature Area Breakdown](#feature-area-breakdown)
   - [A. Quote / CPQ](#a-quote--cpq)
   - [B. Case Management](#b-case-management)
   - [C. Task Management](#c-task-management)
   - [D. Work Order Management](#d-work-order-management)
   - [E. Asset Management](#e-asset-management)
   - [F. Pricing Engine](#f-pricing-engine)
   - [G. Business Rules & Approvals](#g-business-rules--approvals)
   - [H. Account & Contact](#h-account--contact)
   - [I. Genesys / CTI Integration](#i-genesys--cti-integration)
   - [J. Communication & Email](#j-communication--email)
   - [K. Reporting & Dashboards](#k-reporting--dashboards)
   - [L. Administration & Configuration](#l-administration--configuration)
5. [SoD Conflict Matrix](#sod-conflict-matrix)
6. [PSG Composition](#psg-composition)
7. [Migration Path from Existing Permission Sets](#migration-path)

---

## Design Principles

1. **Segregation of Duties governs the split.** If two access points must not be held by the same person (e.g., Price vs Cost), they must be separate permission sets — even if they operate on the same object.
2. **Read vs Write is a boundary.** Every feature area with write access has a corresponding read-only permission set. Users who need visibility but not modification get the read-only variant.
3. **Object access ≠ field access.** The base profile provides Read on all objects. Permission sets grant Create/Edit/Delete at the object level AND field-level edit access. A user with Case Read-only from the profile can see cases but cannot modify any field until a permission set grants field-level edit.
4. **Apex Class Access is explicit.** Lightning components fail silently without class access. Every permission set lists the classes it requires.
5. **Permission sets are additive.** No permission set removes access. Conflicts are prevented by never assigning mutually exclusive permission sets to the same PSG.
6. **Existing permission sets are preserved where they align.** The 33 existing permission sets are mapped into this new structure. Where they already enforce SoD (Price vs Cost), they are retained.

---

## SoD Framework

The following access points represent duties that must be segregated:

| Duty A | Duty B | Rationale |
|--------|--------|-----------|
| **Price Modification** | **Cost Modification** | A user who controls both price and cost can manipulate margins without oversight |
| **Quote Creation/Edit** | **Quote Approval** | The person who creates a quote should not approve it |
| **Pricing Request Execution** | **Pricing Request Read-Only** | Users who execute pricing workflows have different authority than those who only view results |
| **Case Financial Fields** | **Case Lifecycle Management** | Billing/PO/charge fields must be restricted from general case agents |
| **Business Rule Administration** | **Approval Decision-Making** | The person who configures approval rules should not also be the approver |
| **STP Criteria Administration** | **STP Execution** | Those who set eligibility criteria should not also process STP transactions |
| **Work Order Cost Fields** | **Work Order Scheduling** | Vendor cost management is a different duty than service scheduling |
| **Contact Merge/Delete** | **Contact Create/Edit** | Destructive operations require separate authorization |
| **Report Administration** | **Report Execution** | Creating/managing report folders and types is an admin function |
| **Account Financial Config** | **Account General Management** | Billing model, PO requirements, and payment terms are financial controls |

---

## Permission Set Inventory

### Summary: 47 Permission Sets across 12 Feature Areas

| # | Feature Area | Permission Sets | SoD Split Rationale |
|---|-------------|----------------|---------------------|
| **A** | **Quote / CPQ** | 6 | Price vs Cost vs Lifecycle vs Approval vs Read-Only vs MAS |
| **B** | **Case Management** | 5 | Intake vs Lifecycle vs Financial vs SLA Override vs Read-Only |
| **C** | **Task Management** | 3 | Assignment vs Completion vs Read-Only |
| **D** | **Work Order** | 4 | Creation vs Cost/Financial vs Scheduling vs Read-Only |
| **E** | **Asset Management** | 4 | View vs Financial vs Availability Tool vs Configuration |
| **F** | **Pricing Engine** | 3 | Request Execution vs Read-Only vs STP Admin |
| **G** | **Business Rules & Approvals** | 5 | Rule Admin vs Approver Config vs Approval Decision vs NTE Approval vs Read-Only |
| **H** | **Account & Contact** | 5 | Account Mgmt vs Account Financial vs Contact Mgmt vs Contact Merge vs Notification Prefs |
| **I** | **Genesys / CTI** | 2 | Routing View vs Routing Control |
| **J** | **Communication & Email** | 2 | Send Email vs Read-Only |
| **K** | **Reporting & Dashboards** | 3 | Viewer vs Creator vs Administrator |
| **L** | **Administration** | 5 | Knowledge Mgmt vs Project Services vs Governance vs Flow Mgmt vs Market Area Alerts |
|  | **TOTAL** | **47** | |

---

## Feature Area Breakdown

### A. Quote / CPQ

The CPQ subsystem has 154 fields on Quote, 334 fields on QuoteLine, and ~134 Apex classes driving quote creation, line configuration, pricing, and approval workflows. This is the highest-complexity area and requires the most granular SoD.

---

#### A1. PS_Quote_Price_Accessibility

**Duty:** Modify price-related fields on Quotes and Quote Lines.
**SoD Conflict:** Cannot be combined with A2 (Cost Accessibility) in the same PSG.
**Existing PS:** `Price_Accessibility_Permission_Set` — **RETAIN AS-IS**

**Object Permissions:**
- SBQQ__Quote__c: Read (from profile) — no additional object-level grants
- SBQQ__QuoteLine__c: Read (from profile) — no additional object-level grants

**Field Permissions (Edit):**

| Object | Field | Description |
|--------|-------|-------------|
| SBQQ__QuoteLine__c | PriceIncrement1__c through PriceIncrement4__c | Tiered price increment values |
| SBQQ__QuoteLine__c | PricePrice1__c through PricePrice4__c | Tiered price amounts |
| SBQQ__QuoteLine__c | PriceUpTo1__c through PriceUpTo4__c | Tiered price thresholds |
| SBQQ__QuoteLine__c | PriceMinQuantity__c | Minimum quantity for pricing |
| SBQQ__QuoteLine__c | PriceUOM__c | Price unit of measure |
| SBQQ__QuoteLine__c | SBQQ__ListPrice__c | List price |
| SBQQ__QuoteLine__c | SBQQ__PricingMethod__c | Pricing method (list, cost-plus, etc.) |
| SBQQ__QuoteLine__c | Price_Override_Description__c | Justification for price override |
| SBQQ__QuoteLine__c | Price_Override_Reason__c | Reason code for price override |
| SBQQ__QuoteLine__c | HoldUntilPosted__c | Hold flag for price posting |
| SBQQ__QuoteLine__c | Pricing_API_Method__c | API pricing method |
| SBQQ__Quote__c | Cost_Price_Override_Description__c | Quote-level override justification |
| SBQQ__Quote__c | Cost_Price_Override_Reason__c | Quote-level override reason |
| SBQQ__ProductOption__c | PriceUOM__c | Product option price UOM |

**Apex Class Access:** None required (field-level access only).

---

#### A2. PS_Quote_Cost_Accessibility

**Duty:** Modify cost-related fields on Quotes and Quote Lines.
**SoD Conflict:** Cannot be combined with A1 (Price Accessibility) in the same PSG.
**Existing PS:** `Cost_Accessibility_Permission_Set` — **RETAIN AS-IS**

**Object Permissions:**
- SBQQ__Quote__c: Read — no additional object-level grants
- SBQQ__QuoteLine__c: Read — no additional object-level grants

**Field Permissions (Edit):**

| Object | Field | Description |
|--------|-------|-------------|
| SBQQ__QuoteLine__c | CostIncrement1__c through CostIncrement4__c | Tiered cost increment values |
| SBQQ__QuoteLine__c | CostPrice1__c through CostPrice4__c | Tiered cost amounts |
| SBQQ__QuoteLine__c | CostUpTo1__c through CostUpTo4__c | Tiered cost thresholds |
| SBQQ__QuoteLine__c | CostMinQuantity__c | Minimum quantity for costing |
| SBQQ__QuoteLine__c | CostModelType__c | Cost model type |
| SBQQ__QuoteLine__c | SBQQ__UnitCost__c | Unit cost |
| SBQQ__QuoteLine__c | Cost_Override_Description__c | Justification for cost override |
| SBQQ__QuoteLine__c | Cost_Override_Reason__c | Reason code for cost override |
| SBQQ__QuoteLine__c | Cost_Unit_of_Measure__c | Cost unit of measure |
| SBQQ__QuoteLine__c | Cost_Compare_Message__c | Cost comparison message (Read-only) |
| SBQQ__QuoteLine__c | Vendor__c | Vendor assignment |
| SBQQ__QuoteLine__c | Vendor_Commit_Date__c | Vendor commitment date |
| SBQQ__QuoteLine__c | Vendor_Service_Location_Code__c | Vendor service location |
| SBQQ__QuoteLine__c | VendorAccountNumber__c | Vendor account number |
| SBQQ__Quote__c | Cost_Price_Override_Description__c | Quote-level override justification |
| SBQQ__Quote__c | Cost_Price_Override_Reason__c | Quote-level override reason |
| SBQQ__Quote__c | Alternate_Description__c | Alternate service description |
| SBQQ__Quote__c | Alternate_Service_Provided__c | Alternate service flag |
| SBQQ__Quote__c | Quote_SLA_Date__c | SLA date on quote |
| SBQQ__Quote__c | ContractNotes__c | Contract notes |

**Apex Class Access:** None required (field-level access only).

---

#### A3. PS_Quote_Lifecycle_Management

**Duty:** Create, edit, and manage quote records through their lifecycle. Covers quote creation, line configuration, status progression, and assignment — but explicitly excludes price fields, cost fields, and approval authority.
**SoD Conflict:** Cannot be combined with A5 (Quote Approval) in the same user context.
**Existing PS:** `QuoteOrdersUser` — **REPLACE** (too broad; grants all CPQ access without SoD)

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| SBQQ__Quote__c | Yes | Yes | Yes | No |
| SBQQ__QuoteLine__c | Yes | Yes | Yes | No |
| SBQQ__ConfigurationAttribute__c | Yes | Yes | Yes | Yes |
| SBQQ__ProductFeature__c | Yes | Yes | Yes | Yes |
| SBQQ__ProductOption__c | Yes | Yes | Yes | Yes |
| Quote_Line_History_Tracking__c | Yes | Yes | Yes | No |

**Field Permissions (Edit) — Quote Status/Lifecycle fields:**
- SBQQ__Status__c, SBQQ__DocumentStatus__c, Integration_Status__c, QuoteProcuredStatus__c
- STP__c, STP_Success_Report__c, Resubmit_Flag__c, DoResyncOutBoundcall__c
- AAV_Asset_Availability_Flag__c, GR_Service_Flag__c
- Quote_Only__c, Emergency_Request__c

**Field Permissions (Edit) — Quote Routing/Assignment fields:**
- Assigned_To__c, Assing_To_Me_Action__c, SFDC_Team__c, SFDC_Team_User__c
- Is_Genesys_Required__c, Genesys_Record_Created__c

**Field Permissions (Edit) — Quote General Data fields:**
- Customer_Request_Date__c, Duration__c, Schedule_or_On_Call__c
- Onsite_Contact__c, Location_Customer_Name__c, Primary_Segment__c
- Priority__c, Project__c, ErrorComments__c
- Next_Action_Date__c, Next_Action_Description__c

**Field Permissions (Excluded — belong to A1/A2):**
- All PriceIncrement/PricePrice/PriceUpTo fields
- All CostIncrement/CostPrice/CostUpTo fields
- SBQQ__ListPrice__c, SBQQ__UnitCost__c, Markup_Percentage__c

**Apex Class Access (25+ classes):**
- QuoteCreationHandler, QuoteLineCreationHandler, QuoteLineService, QuoteLineServices
- QuoteTriggerHandler, QuoteTriggerHelper, QuoteLineTriggerHandler, QuoteLineTriggerHelper
- QuoteSelector, QuoteLineSelector, QuoteLineClassificationChanges
- QuoteActionsController, QuoteOnlyController, QuoteProcurementController
- QuoteFavoritesController, GetQuoteSummary, ShowQuoteLineHistoryController
- AssetQuoteProcurementController, AlternateServiceController
- QuoteOrderTriggerHandler, RemovalQuoteLineHandler, QouteValiationHandler
- SBQQConfigurationRuleSelector, SBQQConfigurationRuleService, SBQQProductOptionSelector
- SBQQQuoteService, AsyncUpdateQuoteFlag, CalculateQuotePriority

**User Permissions:** None additional (profile provides base).

---

#### A4. PS_Quote_Read_Only

**Duty:** View-only access to all quote and quote line data, including price and cost fields.
**SoD Conflict:** None — read-only access does not create SoD risk.
**Existing PS:** `CPQReadOnly` — **RETAIN AS-IS**

**Object Permissions:**
- SBQQ__Quote__c: Read only
- SBQQ__QuoteLine__c: Read only
- Quote_Line_History_Tracking__c: Read only

**Field Permissions:** All fields readable, none editable.

**Apex Class Access:** Same as CPQReadOnly (40+ classes for view operations, navigation, and display).

---

#### A5. PS_Quote_Approval

**Duty:** Authority to approve or decline quotes. Covers the approval workflow fields.
**SoD Conflict:** Cannot be combined with A3 (Quote Lifecycle) — the person who creates/edits a quote should not approve it.

**Object Permissions:**
- SBQQ__Quote__c: Edit
- Approval_Log__c: Create, Edit

**Field Permissions (Edit):**
- SBQQ__Quote__c: Action_Type__c, Action_Reason__c, Manual_Approval_Action__c, Approve_NTE_Amount__c, Pending_Information__c, Special_Handling__c, Special_Handling_Reason__c
- Approval_Log__c: Status__c, Approval_Comments__c, Decision_Date_Time__c, Actual_Approver__c

**Apex Class Access:**
- QuoteApproval, QuoteApprovalHandler, QuoteDecline

---

#### A6. PS_Quote_MAS_Integration

**Duty:** Manage MAS (Material Automated Services) integration fields on quote lines.
**SoD Conflict:** None — operational integration, not financial.
**Existing PS:** `MAS_Permissionset` — **RETAIN AS-IS**

**Object Permissions:**
- SBQQ__QuoteLine__c: Edit

**Field Permissions (Edit):** 21 MAS-specific fields including ByPassMASServiceChange__c, MASAccount__c, MASBox__c, MASDelivery__c, MASNewTicket__c, MASOpsRouting__c, MASRemoval__c, MAS_Swapout__c, VCRCode__c, and related comment fields.

---

### B. Case Management

The Case object has 321 fields and is the primary operational object. Cases involve financial fields (billing, PO, charges), SLA management (with override authority), intake/creation, general lifecycle, and assignment/routing. These are distinct duties.

---

#### B1. PS_Case_Intake

**Duty:** Create new cases and populate initial intake data. This is the entry-point permission for any case-handling role.

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Case | Yes | Yes | Yes | No |
| SBS_Case_Asset__c | Yes | Yes | Yes | No |

**Field Permissions (Edit) — Intake fields:**
- Case_Type__c, Case_Sub_Type__c, Case_Reason__c, Subject, Description
- ContactId, Site_Contact__c, Site_Contact_Phone__c, Email_Address__c
- Location__c, Client__c, Supplier__c, AssetId
- Emergency__c, Emergency_Reason__c, Quote_Only__c
- Source_System__c, Is_From_ScreenPop__c, FlowToRun__c
- Service_Date__c, Delivery_Date__c, Service_Start_Date__c, Service_End_Date__c
- Equipment_Size_Code__c, Equipment_Type_Code__c, Material_Type__c, Material__c
- Monday__c through Sunday__c, Frequency__c, Occurrence__c
- Offsite_Address__c, Offsite_Street_Address__c, Offsite_City__c, Offsite_State__c, Offsite_Postal_Code__c
- All haul-away intake fields, portable/compactor questionnaire fields, site survey fields

**Apex Class Access:**
- CaseController, CustomCaseCreationCntrlr, CaseCreation, CaseUpdateHandler
- CaseTriggerHandler, CaseTriggerHelper, CaseDetailHelper, CustomCaseHighlightPanelCntrl
- CaseCustomLookUpController, DuplicateCheckOnCaseController, GetCaseInformation
- ContactSearchandCreate, ScreenpopController, Screenpop
- HaulAwayService, BalePickupCaseService, ETAWindowController
- IntakeProcessAuraHandler, ProgressCaseComponentController

**User Permissions:**
- ActivitiesAccess (required to create tasks from case context)

---

#### B2. PS_Case_Lifecycle_Management

**Duty:** Progress cases through status changes, milestone updates, approval workflows, and closure. Does NOT include financial fields or SLA override authority.
**SoD Conflict:** Cannot be combined with B3 (Case Financial).

**Object Permissions:**
- Case: Edit
- Comment__c: Create, Edit

**Field Permissions (Edit) — Status/Lifecycle fields:**
- Status, Case_Sub_Status__c, Approval_Status__c, Authorization_Status__c
- Current_Milestone__c, Milestone_Entry_Time__c, Milestone_Warning_1__c
- Close_Case_Reason__c, Close_Irrelevant_Case__c, Close_Pickup_Case__c, Case_Close_Reason__c
- isApproved__c, isRejected__c, isWorkOrderCreated__c
- Master_Intake_Complete__c, VCC_Complete__c, BackOffice_Case__c
- PSI_Override_Reason__c, Availability_Checked__c, Availability_Confirmed__c
- CheckReassignment__c, Last_Agent_ID__c, Last_Agent_Id_ForTaskAssignment__c

**Field Permissions (Edit) — Communication fields:**
- Case_Comments__c, PSI_Comments__c, EmailTemplateAdditionalComments__c
- Authorization_Notes__c, Authorization_Channel__c

**Field Permissions (Excluded — belong to B3):**
- PurchaseOrder_Number__c, Invoice_Number__c, Disputed_Amount__c, Chargeable__c
- SalesMeet_Price__c, No_Price__c, Price_Quote_Identifier__c

**Field Permissions (Excluded — belong to B4):**
- SLA_Service_Date__c, SLA_Service_Date_Time__c, SLA_Override_Reason__c, SLA_Override_Comment__c

**Apex Class Access:**
- CaseUpdateHandler, CaseApprovalHandler, CaseHistoryTrackerTriggerHandler
- CommentController, CustomCommentController, CaseCommentsControllerExtension
- CreateCaseHistory, CloseAcornTicket, ReopenAcornTicket, ReassignAcornTicket
- ConcatenateTaskDetailForAcorn, AcornController, AcornCaseDetailsResource
- ValidateTaskToPopMessage, MultiCaseTaskPopuCntrlr, CaseDetailCardController
- CommunicationChannelViewController, GetChildCase

---

#### B3. PS_Case_Financial

**Duty:** Modify billing, pricing, PO, and charge-related fields on cases.
**SoD Conflict:** Cannot be combined with B2 (Case Lifecycle) in roles where financial segregation is required.

**Object Permissions:**
- Case: Edit (field-level restriction)

**Field Permissions (Edit):**
- PurchaseOrder_Number__c, PurchaseOrder_Required__c, PurchaseOrder_Override_Reason__c, Override_PO_Create_Task__c
- Invoice_Number__c, Disputed_Amount__c
- Chargeable__c, Is_Haul_Away_Service__c, Haul_Away_Service_Booked__c
- SalesMeet_Price__c, No_Price__c, Price_Quote_Identifier__c
- Quote_Eligibility_Result__c, CPQ_New_Service__c
- Cost_of_bale_wire_per_unit__c, Quantity_of_bale_wire_needed_per_cost__c, Documentation_of_cost__c
- IsOpportunity_Created__c
- Locally_Billed__c

**Apex Class Access:**
- BillingService (calculates billing for cases)

---

#### B4. PS_Case_SLA_Override

**Duty:** Override SLA dates and service date calculations. This is a privileged action — most agents should NOT have this.
**SoD Conflict:** Should be restricted to supervisors/leads who are not the case owner.

**Object Permissions:**
- Case: Edit (field-level restriction)

**Field Permissions (Edit):**
- SLA_Service_Date__c, SLA_Service_Date_Time__c, SLA_Date_Text__c
- SLA_Override_Reason__c, SLA_Override_Comment__c, SLA_Violation__c
- Service_Date_from_Local_Time__c
- WO_Original_Service_Date__c (typically formula — but override scenarios exist)
- Proposed_Service_Date__c

**Apex Class Access:**
- CaseSLAEntitlementUTIL, CaseEntitlement, StartDateManagement, EndDateHandler
- GetSLAInformation

---

#### B5. PS_Case_Read_Only

**Duty:** View-only access to all case data including financial and SLA fields.
**SoD Conflict:** None.

**Object Permissions:**
- Case: Read only
- SBS_Case_Asset__c: Read only
- Comment__c: Read only

**Field Permissions:** All fields readable, none editable.

**Apex Class Access:**
- CaseDetailHelper, CustomCaseHighlightPanelCntrl, CaseDetailCardController
- GetCaseInformation, CommunicationChannelViewController

---

### C. Task Management

The Task object has 22 standard fields but is heavily governed by 29 validation rules that enforce outcome-based restrictions, UCC-based access control, and date validations. The SoD boundary is between assignment authority and completion authority.

---

#### C1. PS_Task_Assignment

**Duty:** Create, assign, and reassign tasks. Includes setting the task owner, team assignment, and initial scheduling.

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Task | Yes | Yes | Yes | No |

**Field Permissions (Edit):**
- OwnerId, Subject, Description, Priority, ActivityDate
- WhatId (related Case), WhoId (related Contact)
- Status (limited to assignment-related statuses)
- Type, CallType, IsReminderSet, ReminderDateTime

**User Permissions:**
- EditTask, EditEvent, ActivitiesAccess

**Apex Class Access:**
- TaskTriggerHandler, TaskTriggerHelper, AssignToMeCntrl, ChangeTaskAssignmentcntrl
- TaskRelatedListAura, TaskTableWrapper, TaskPopUpMessageController
- MultiCaseTaskPopuCntrlr, CreatePendingInformationTask, GenTaskController
- MyTaskListController, ServiceIssueTaskController
- GetTaskRecursionCheck, PutTaskRecursionCheck

**Note:** Validation rule `Restrict_Next_Task_Date_to_SSMGEN_users` enforces that only SSM team users (UCC = SSMGEN) can edit Next_Task_Due_Date_Time__c. This is an additional UCC-based SoD control layered on top of permission sets.

---

#### C2. PS_Task_Completion

**Duty:** Complete tasks by setting outcomes, updating result fields, and closing. This is separated from assignment because in some workflows the person who assigns a task should not be the one who records its outcome.
**SoD Conflict:** In audit-sensitive workflows, should not overlap with C1 for the same user.

**Object Permissions:**
- Task: Edit

**Field Permissions (Edit):**
- Status (set to Completed/Closed)
- CompletedDateTime, CallDisposition, CallDurationInSeconds
- Outcome fields (these are typically controlled via Task validation rules per Outcome__c picklist value)

**Apex Class Access:**
- AsyncCompleteTask, AttemptTasksCreationBatch, SendEmailForNotifyCustomerDelayTask

---

#### C3. PS_Task_Read_Only

**Duty:** View-only access to all task data.

**Object Permissions:**
- Task: Read only

**Field Permissions:** All fields readable, none editable.

**Apex Class Access:**
- TaskRelatedListAura, TaskTableWrapper, MyTaskListController

---

### D. Work Order Management

Work Orders have 137 fields with significant financial, scheduling, and vendor management dimensions. The SoD boundary separates cost management from scheduling from creation.

---

#### D1. PS_WorkOrder_Creation

**Duty:** Create and edit work orders and line items. Covers general work order data but excludes financial/cost fields.

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| WorkOrder | Yes | Yes | Yes | No |
| WorkOrderLineItem | Yes | Yes | Yes | No |

**Field Permissions (Edit) — General WO fields:**
- Subject, Description, Status, Priority, StartDate, EndDate
- Service_Date__c, Original_Expected_Date__c, Proposed_Service_Date__c
- Account (AccountId), Contact (ContactId), Asset (AssetId), Case (CaseId)
- Acorn integration fields: Acorn_Issue_Id__c, Acorn_Work_Order_Number__c, Acorn_Status__c
- Work_Order_Instructions__c, User_Input_Work_Order_Instructions__c, System_Gen_WO_Instructions__c
- Location fields, equipment fields, material fields

**Field Permissions (Excluded — belong to D2):**
- All cost/financial fields on WorkOrder and WorkOrderLineItem

**Apex Class Access:**
- WorkOrderController, WorkOrderTriggerHandler, WorkOrderTriggerHelper
- WorkOrderLineItemTriggerHandler, WorkOrderLineItemTriggerHelper
- MultipleWorkorderController, UpdateWorkOrder, GetWorkOrderPDFCntrlr
- AcornWODetailsController, WODataWrapper

---

#### D2. PS_WorkOrder_Cost_Management

**Duty:** Modify cost and financial fields on Work Orders and Line Items.
**SoD Conflict:** Should be restricted to vendor relations / financial roles. Cannot be held alongside D3 (Scheduling) in roles where vendor financial and scheduling duties must be separated.

**Object Permissions:**
- WorkOrder: Edit (field-level restriction)
- WorkOrderLineItem: Edit (field-level restriction)

**Field Permissions (Edit):**
- WorkOrder: Vendor cost fields, service charge fields, billing fields
- WorkOrderLineItem: Unit cost fields, total cost fields, charge type fields
- Service_Status__c related: Charge_Type__c, Charge_Amount__c

**Apex Class Access:**
- WorkOrderWebservices, BillingService

---

#### D3. PS_WorkOrder_Scheduling

**Duty:** Manage service dates, scheduling, and vendor assignment on Work Orders.
**SoD Conflict:** In vendor management scenarios, may need to be separated from D2.

**Object Permissions:**
- WorkOrder: Edit (field-level restriction)

**Field Permissions (Edit):**
- Service_Date__c, Original_Expected_Date__c, Proposed_Service_Date__c
- StartDate, EndDate, ETA fields
- Vendor assignment fields, Service_Classification__c
- Schedule_or_On_Call__c, Recurrence fields

**Apex Class Access:**
- ServiceSchedulerCtrl, WorkOrderReportCtrl, ETAWindowController

---

#### D4. PS_WorkOrder_Read_Only

**Duty:** View-only access to all work order data.

**Object Permissions:**
- WorkOrder: Read only
- WorkOrderLineItem: Read only

**Field Permissions:** All fields readable, none editable.

**Apex Class Access:**
- AcornWODetailsController, WODataWrapper, GetWorkOrderPDFCntrlr

---

### E. Asset Management

Assets have 288 fields — the most complex object. Dominated by financial/cost fields (69), equipment configuration, and Acorn ERP integration.

---

#### E1. PS_Asset_View

**Duty:** Read-only access to asset records with display capabilities.

**Object Permissions:**
- Asset: Read only
- SBS_Case_Asset__c: Read only

**Field Permissions:** All fields readable, none editable.

**Apex Class Access:**
- AssetHeadersForCaseController, DisplayCaseAssetController, CaseAssetController
- assetCustomTreeGridController, LocationContainerController
- AssetQuerySelector

---

#### E2. PS_Asset_Financial

**Duty:** Modify financial fields on assets — cost, discount, pricing model fields.
**SoD Conflict:** Should not overlap with E4 (Configuration) in roles where financial and operational duties are separated.

**Object Permissions:**
- Asset: Edit (field-level restriction)

**Field Permissions (Edit):**
- All SBQQ discount/pricing fields on Asset
- Cost-related fields, billing model fields
- Contract pricing fields, markup fields

---

#### E3. PS_Asset_Availability_Tool

**Duty:** Execute the Asset Availability (AAV) stand-alone tool.
**Existing PS:** `AAV_Availability_Stand_Alone_Tool` + `Asset_Availability_User_Permission_Set` — **CONSOLIDATE into one**

**Object Permissions:**
- AAV_Asset_Availability__c: Create, Read, Edit, Delete, ViewAll, ModifyAll

**Field Permissions (Edit):** All 15 AAV fields.

**Custom Permissions:** AAV_Asset_Availability_User

**Apex Class Access:**
- AAV_APIIntegration, AAV_AvailabilityUtility, AAV_AvailbilityAppHelper
- QuoteFavoritesController

---

#### E4. PS_Asset_Configuration

**Duty:** Modify equipment type, container details, material codes, and service configuration on assets.

**Object Permissions:**
- Asset: Edit (field-level restriction)

**Field Permissions (Edit):**
- Equipment type/size/style fields, Container fields
- Material type/code fields, Product family fields
- Service day fields, recurrence/frequency fields
- Location/site fields

**Apex Class Access:**
- AssetTriggerHandler, AssetTriggerHelper, updateAcornAssetLocation
- ProjectCodeTriggerHandler, ProjectCodeTriggerHelper, ProjectCodeActiveChecker

---

### F. Pricing Engine

The Pricing Request object (76 fields) drives vendor pricing through API integrations. This is already well-segregated in the existing permission sets.

---

#### F1. PS_Pricing_Request_Execution

**Duty:** Create and process pricing requests through the full workflow including API integration.
**Existing PS:** `Pricing_Access` — **RETAIN AS-IS**

**Object Permissions:**
- Pricing_Request__c: Create, Read, Edit (no Delete), ViewAll

**Field Permissions (Edit):** 70+ fields including all cost/price pairs (Haul_Cost__c/Haul_Price__c, Pickup_Cost__c/Pickup_Price__c, Disposal_Cost__c/Disposal_Price__c, Extra_Pickup_Cost__c/Extra_Pickup_Price__c), service configuration, vendor info.

**Apex Class Access (25+ classes):**
- PricingRequest, PricingChangeRequest, CreatePricingRequest, PricingRequestHandler
- PricingRequestAPIIntegration, PricingResponseProcessor, ProcessQLIPricingRequest
- PricingRequestSelector, PricingRequestHelper, PricingRequestFieldsMetadata
- PricingRequestSTPProcess, PriceOnlyRequestSTPProcess, PricingRequestMultiVendorSTPProcess
- PricingRequestJsonDeserialize, PricingRequestResponseBatch, ExhibitPriceServices

---

#### F2. PS_Pricing_Request_Read_Only

**Duty:** View-only access to pricing request data.
**Existing PS:** `Pricing_Read_Only` — **RETAIN AS-IS**

**Object Permissions:**
- Pricing_Request__c: Read only, ViewAll

**Field Permissions:** 12 key fields readable, none editable.

**Apex Class Access:** Limited set for view operations.

---

#### F3. PS_STP_Administration

**Duty:** Configure STP eligibility criteria and manage exception logs.
**SoD Conflict:** Users with STP admin access should not also execute STP pricing workflows (F1).
**Existing PS:** `STP_Administration` — **RETAIN AS-IS**

**Object Permissions:**
- STP_Criteria__c: Create, Read, Edit, Delete, ViewAll, ModifyAll
- ExceptionLog__c: Read only, ViewAll

**Field Permissions (Edit):** 22 STP criteria fields — vendor eligibility, customer eligibility, equipment rules, market type, frequency, duration.

---

### G. Business Rules & Approvals

Business Rules (43 fields), Service Approvers (31 fields), Approval Logs (24 fields), and Out of Office (11 fields) form the approval ecosystem. SoD requires separating rule authoring from approver configuration from approval decision-making.

---

#### G1. PS_Business_Rule_Administration

**Duty:** Create and manage business rules, including NTE rules, notification rules, and approval routing configuration.
**SoD Conflict:** Cannot be combined with G3 (Approval Decision) — the person who writes the rules should not be the one making approval decisions under those rules.
**Existing PS:** `Business_Rule_Notification` — **REFACTOR** (currently too broad; includes approver config)

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Business_Rule__c | Yes | Yes | Yes | Yes |
| Categorization__c | Yes | Yes | Yes | Yes |
| Department__c | Yes | Yes | Yes | Yes |
| Entitlement | Yes | Yes | Yes | Yes |

**Field Permissions (Edit):** All 43 Business_Rule__c fields, all Categorization__c and Department__c fields.

**Custom Permissions:** BR_Notification, Clone_Button_Visibility

**Apex Class Access:**
- BusinessRuleCtrl, BusinessRuleHelper, BusinessRuleNSCHelper
- BusinessRuleTriggerHandler, BusinessRuleTriggerHelper, BusinessRuleUtility
- AllRulesModalController, CaseRulesModalCtrl, NTEApprovalRuleHelper, NTEBRRulesModalCtrl
- AddNTERulesCtrl, CloneApprovalRules

---

#### G2. PS_Service_Approver_Configuration

**Duty:** Configure who the approvers are for each business rule, including NTE amounts, fuzzy matching, and contact/email settings.
**SoD Conflict:** Cannot be combined with G3 (Approval Decision) — configuring approvers and being an approver creates a self-approval risk.

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Service_Approver__c | Yes | Yes | Yes | Yes |
| Out_of_Office__c | Yes | Yes | Yes | Yes |

**Field Permissions (Edit):** All 31 Service_Approver__c fields, all 11 Out_of_Office__c fields.

**Apex Class Access:**
- ServiceApproverHandler, ServiceApproverHelper, ServiceApproverFuzzyMatch
- GetServiceApprover, ToActivateServiceApprovers, ReqInfoServiceApprovers
- SendEmailToServiceApproversCntrlr, SendEmailToServiceApproversCntrlrURule

---

#### G3. PS_Approval_Decision

**Duty:** Make approval decisions — approve, reject, request info. Record the decision in the Approval Log.
**SoD Conflict:** Cannot be combined with G1 (Rule Admin) or G2 (Approver Config).

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Approval_Log__c | Yes | Yes | Yes | No |

**Field Permissions (Edit):**
- Status__c, Approval_Comments__c, Decision_Date_Time__c
- Actual_Approver__c, Actual_Approver_Contact__c, Actual_Approver_Email__c
- Actual_External_Approver_Name__c, Actual_Approver_Origin__c, Actual_Approver_Title__c

**Apex Class Access:**
- CaseApprovalHandler, QuoteApprovalHandler, QuoteApproval, QuoteDecline
- UpdateBrApprovalBatch

---

#### G4. PS_NTE_Approval

**Duty:** Approve Not-To-Exceed (NTE) amounts on quotes. This is a financial approval that must be held by a separate authority from general approval decision-making in high-value scenarios.

**Object Permissions:**
- SBQQ__Quote__c: Edit (field-level restriction)

**Field Permissions (Edit):**
- Approve_NTE_Amount__c, is_NTE_Quote__c

**Apex Class Access:**
- NTEApprovalRuleHelper, NTEBRRulesModalCtrl, GetBRQuotePriorityNTECtrl

---

#### G5. PS_Business_Rule_Read_Only

**Duty:** View-only access to business rules, approvers, and approval logs.

**Object Permissions:**
- Business_Rule__c: Read only
- Service_Approver__c: Read only
- Approval_Log__c: Read only
- Out_of_Office__c: Read only

**Apex Class Access:**
- AllRulesModalController, CaseRulesModalCtrl (view-mode only)

---

### H. Account & Contact

Account (215 fields) and Contact (73 fields) have financial configuration fields that must be separated from general management.

---

#### H1. PS_Account_Management

**Duty:** Edit general account data — names, addresses, location codes, market areas, operational configuration.

**Object Permissions:**
- Account: Edit
- Account_Title__c: Create, Edit

**Field Permissions (Edit):** General account fields — Customer_ID__c, Customer_Code__c, Company_Category__c, Business_Type__c, Status__c, Market_Area__c, Location_Type__c, Division__c, Category__c, DBA_Names__c, address fields, Acorn integration fields, phone/email fields, timezone fields.

**Field Permissions (Excluded — belong to H2):**
- Billing_Model__c, Billing_Schedule__c, Billing_Window__c, Invoice_Method__c
- PO_Required__c, Federal_Tax_Id__c, payment terms fields

**Apex Class Access:**
- AccountContactRelationHandler, AccountContactRelationHelper
- AccountTitleTriggerHandler, AccountTitleTriggerHelper
- AcornCompanyController, AcornCompanyDetails
- AccountTeamMemberUIController, AccountTeamMemberQueryAction, HoverOverCardsCntrl

---

#### H2. PS_Account_Financial_Configuration

**Duty:** Modify billing model, PO requirements, payment terms, and other financial configuration on accounts.
**SoD Conflict:** Cannot be combined with H1 in roles where financial configuration must be authorized separately.

**Object Permissions:**
- Account: Edit (field-level restriction)

**Field Permissions (Edit):**
- Billing_Model__c, Billing_Schedule__c, Billing_Window__c
- Invoice_Method__c, PO_Required__c
- Federal_Tax_Id__c, Payment_Terms__c
- Enrolled_in_Premium_Delivery_Service__c (from Manage_Premium_Deliveries PS)

---

#### H3. PS_Contact_Management

**Duty:** Create and edit contacts, manage contact-to-account relationships.

**Object Permissions:**

| Object | Create | Read | Edit | Delete |
|--------|--------|------|------|--------|
| Contact | Yes | Yes | Yes | No |
| Contact_Notification_Preference__c | Yes | Yes | Yes | No |

**Field Permissions (Edit):** All standard and custom contact fields — ANI__c, Contact_Status__c, phone/email fields, Preferred_Language__c, Preferred_Method__c, Text_Notifications_Opt_In__c, Account_Title__c, Account_Department__c, Location__c.

**Existing PS:** `Contact_Notification_Maintenance` — **ABSORB** into this PS.

**Apex Class Access:**
- ContactTriggerHandler, ContactTriggerHelper, ContactSearchandCreate
- ContactByRoleHelper, FetchAccountContactByRole
- ContactNotifyPrefTriggerHandler, ContactNotifyPrefTriggerHelper
- ContactTextOptInInvokableAPI, ContactTextOptOutInvokableAPI

---

#### H4. PS_Contact_Merge

**Duty:** Delete and merge duplicate contact records. This is a destructive operation requiring separate authorization.
**SoD Conflict:** Must be separate from H3 (Contact Management) — creating contacts and merging/deleting them should require different authority.
**Existing PS:** `Merge_Access_for_Non_Admin_Users` — **RETAIN AS-IS**

**Object Permissions:**
- Contact: Edit, Delete, ModifyAll, ViewAll
- DuplicateRecordSet: Read, ViewAll

**Apex Class Access:**
- DuplicateContactMergeBatch, BatchToInactivateContact

---

#### H5. PS_Notification_Preferences

**Duty:** Manage account-level notification preferences.
**Existing PS:** `Account_Notification_Maintenance` — **RETAIN AS-IS**

**Object Permissions:**
- Account_Notification_Preference__c: Create, Read, Edit

---

### I. Genesys / CTI Integration

Genesys Routing (42 fields) and Task Routing Control are operational integration points.

---

#### I1. PS_Genesys_Routing_View

**Duty:** View Genesys routing records and integration status.

**Object Permissions:**
- Genesys_Routing__c: Read only

**Field Permissions:** All 42 fields readable, none editable.

**Apex Class Access:**
- IVRServiceStatusWebService, IVRServiceStatusWebService_V1
- IVRServiceStatusETA, IVRServiceStatusETA_V1, IVRUtility
- GetIVRCasePrompt, IVRContainerServices, IVRExitController

---

#### I2. PS_Genesys_Routing_Control

**Duty:** Create and manage Genesys routing records and task routing configuration.
**Existing PS:** `Task_Genesys_Routing_Permission` — **RETAIN** and extend.

**Object Permissions:**
- Genesys_Routing__c: Create, Read, Edit
- Task_Genesys_Routing_Control__c: Create, Read, Edit, Delete, ViewAll, ModifyAll

**Field Permissions (Edit):** All Genesys_Routing__c fields, all Task_Genesys_Routing_Control__c fields (Primary_Segment__c, Service_Flag__c, Stop_Routing__c, Task_Type__c).

**Apex Class Access:**
- CreateGenesysRecordBatch, CreateGenesysForQuoteBatch, BatchToCreateGenesysForPITasks
- DeleteGenesysReportingBatch, TaskAndGenesysPETriggerHelper
- ScheduleCreateGenesysForQuoteBatch, ScheduleCreateGenesysForTask

---

### J. Communication & Email

---

#### J1. PS_Communication_Send

**Duty:** Send emails, manage email messages, and create communication records.

**Object Permissions:**
- Communication_Channel__c: Create, Read, Edit
- EmailMessage: Create, Read, Edit

**Field Permissions (Edit):** All Communication_Channel__c fields (9), email message fields.

**User Permissions:**
- EmailSingle, DistributeFromPersWksp

**Apex Class Access:**
- EmailService, EmailMessageCreation, EmailMessageHelper
- EmailMessageTriggerHandler, EmailMessageTriggerHelper, FetchEmailMessages
- InvocableFlowEmail, NotifyCustomerOfDelayEmailController
- NotificationTrackingController, NotifTrackingWrapper
- SendAlert, SendBusinessRuleData, SendEmailToWMVendorCtrl
- AutoSendEmailToServiceApprovers, SendErrorNotificationOnJobFailure
- ChatTranscriptPdfCtrl

---

#### J2. PS_Communication_Read_Only

**Duty:** View communication history, email messages, and channel records.

**Object Permissions:**
- Communication_Channel__c: Read only
- EmailMessage: Read only

**Apex Class Access:**
- CommunicationChannelViewController, FetchEmailMessages, NotificationTrackingController

---

### K. Reporting & Dashboards

Three tiers of reporting access, each building on the previous.

---

#### K1. PS_Report_Viewer

**Duty:** Run existing reports and view dashboards. (Note: RunReports and ViewPublicReports/ViewPublicDashboards are already on the base profile.)
**Existing PS:** Not needed as separate PS — base profile covers this.

---

#### K2. PS_Report_Creator

**Duty:** Create and customize reports and dashboards.
**Existing PS:** `Reports_and_Dashboards_Super_User` — **RETAIN AS-IS**

**User Permissions:**
- CreateCustomizeDashboards, CreateCustomizeReports
- RunReports, ViewPublicDashboards, ViewPublicReports

---

#### K3. PS_Report_Administrator

**Duty:** Full report and dashboard administration including folder management and publishing.
**SoD Conflict:** Cannot be combined with K2 in roles where report publishing must be authorized separately.
**Existing PS:** `Reports_and_Dashboards_Administrator` — **RETAIN AS-IS**

**User Permissions:**
- CreateCustomizeDashboards, CreateCustomizeReports, CreateDashboardFolders, CreateReportFolders
- EditMyDashboards, EditMyReports
- ManageDashbdsInPubFolders, ManageReportsInPubFolders
- RunReports, ViewPublicDashboards, ViewPublicReports

---

### L. Administration & Configuration

---

#### L1. PS_Knowledge_Management

**Duty:** Create, edit, and publish knowledge articles.
**Existing PS:** `Knowledge_Manager_User` — **RETAIN AS-IS**

**Object Permissions:**
- Knowledge__kav: Create, Read, Edit, Delete

**User Permissions:** ArchiveArticles, EditKnowledge, PublishArticles, ViewArchivedArticles, ViewDraftArticles

---

#### L2. PS_Project_Services

**Duty:** Manage project codes and project-level business rules.
**Existing PS:** `Project_Services_Project_Management` — **RETAIN AS-IS**

**Object Permissions:**
- Project_Code__c: Create, Read, Edit
- Business_Rule__c: Create, Read, Edit

**Field Permissions:** All Project_Code__c and business rule fields.

---

#### L3. PS_Governance_Team

**Duty:** Override read-only restrictions for governance updates and manage unspecified contacts.
**Existing PS:** `Governance_Team` — **RETAIN AS-IS**

**Custom Permissions:** Goverance_Team_Access, Unspecified_Contact_Edit

---

#### L4. PS_Flow_Management

**Duty:** Manage and execute flows with elevated permissions.
**Existing PS:** `Manage_Flows` — **RETAIN AS-IS**

**User Permissions:** ManageInteraction, RunFlow, ViewRoles, ViewSetup

---

#### L5. PS_Market_Area_Alerts_Admin

**Duty:** Configure market area alert settings.
**Existing PS:** `MAA_Admin_Panel_Team` — **RETAIN AS-IS**

**Object Permissions:**
- MAA_Admin_Settings__c: Read, Edit

**Custom Permissions:** MAA_Admin_Panel

**Apex Class Access:** MarketAreaAlertController

---

#### L6. PS_Customer_Service_Reporting

**Duty:** Customer service supervisor reporting and dashboard access.
**Existing PS:** `Customer_Service_Reporting_User` — **RETAIN AS-IS**

**User Permissions:** CreateCustomizeReports, CreateReportFolders, CreateReportInLightning, EditMyReports, ManageCustomReportTypes, ManagePvtRptsAndDashbds, ManageReportsInPubFolders, NewReportBuilder, ScheduleReports

**Apex Class Access:** SupervisorDashboardCls

---

#### L7. PS_Escalation_Maintenance

**Duty:** Manage vendor escalation contacts and categories.
**Existing PS:** `Escalation_Maintenance_Permissions` — **RETAIN AS-IS**

**Object Permissions:**
- Category__c: Create, Read

**Apex Class Access:** VendorEscalationContactController

---

#### L8. PS_Launch_FAST

**Duty:** LAUNCH/FAST activity log and project tracking.
**Existing PS:** `Launch_Fast` — **RETAIN AS-IS**

**Object Permissions:**
- FAST_Activity_Log__c: Create, Read, Edit, Delete, ViewAll, ModifyAll

---

#### L9. PS_Digital_Transformation_Tracking

**Duty:** Time tracking for digital transformation projects.
**Existing PS:** `Digital_Transformation_Time_Tacking` — **RETAIN AS-IS**

**Object Permissions:**
- Digital_Transformation_Time_Tracking__c: Create, Read, Edit

---

#### L10. PS_Premium_Delivery_Management

**Duty:** Manage premium delivery service enrollment on accounts.
**Existing PS:** `Manage_Premium_Deliveries` — **RETAIN AS-IS**

---

#### L11. PS_View_Setup

**Duty:** View-only access to org setup and configuration.
**Existing PS:** `View_Setup_and_Configuration` — **RETAIN AS-IS**

**User Permissions:** ViewRoles, ViewSetup

---

#### L12. PS_Modify_All_Data

**Duty:** Full administrative data modification. System admin only.
**Existing PS:** `Modify_All_Data` — **RETAIN AS-IS**

---

#### L13. PS_Password_Never_Expires

**Duty:** Integration/API user password policy.
**Existing PS:** `Password_Never_Expires` — **RETAIN AS-IS**

---

## SoD Conflict Matrix

The following permission set combinations MUST NEVER appear in the same PSG:

| PS A | PS B | Risk |
|------|------|------|
| A1 (Price Accessibility) | A2 (Cost Accessibility) | Margin manipulation |
| A3 (Quote Lifecycle) | A5 (Quote Approval) | Self-approval of quotes |
| B2 (Case Lifecycle) | B3 (Case Financial) | Unauthorized financial changes |
| B1/B2 (Case Intake/Lifecycle) | B4 (Case SLA Override) | SLA manipulation by case agent |
| D2 (WO Cost Management) | D3 (WO Scheduling) | Vendor cost/schedule collusion |
| G1 (Rule Administration) | G3 (Approval Decision) | Self-approval rule authoring |
| G2 (Approver Configuration) | G3 (Approval Decision) | Self-appointment as approver |
| F1 (Pricing Execution) | F3 (STP Administration) | STP criteria manipulation for self-benefit |
| H1 (Account Management) | H2 (Account Financial Config) | Unauthorized billing configuration |
| H3 (Contact Management) | H4 (Contact Merge) | Uncontrolled data destruction |

---

## PSG Composition

Below shows how permission sets compose into persona-based PSGs. Each PSG enforces SoD by design — conflicting permission sets never appear in the same group.

### PSG_Customer_Service_Agent
| Permission Set | Rationale |
|---------------|-----------|
| B1 — Case Intake | Core duty: create cases |
| B2 — Case Lifecycle | Core duty: manage case progress |
| C1 — Task Assignment | Core duty: manage tasks |
| C2 — Task Completion | Core duty: complete tasks |
| A4 — Quote Read-Only | View quotes but not edit |
| D4 — WorkOrder Read-Only | View work orders |
| E1 — Asset View | View assets |
| G5 — Business Rule Read-Only | View rules |
| I1 — Genesys View | View routing |
| J1 — Communication Send | Send emails to customers |
| H3 — Contact Management | Manage contacts on cases |

### PSG_Customer_Service_Lead
Inherits all of PSG_Customer_Service_Agent PLUS:
| Permission Set | Rationale |
|---------------|-----------|
| B4 — Case SLA Override | Supervisor authority to override SLA |
| G3 — Approval Decision | Authority to approve |
| K2 — Report Creator | Create team reports |

### PSG_SSM_Agent
| Permission Set | Rationale |
|---------------|-----------|
| B1 — Case Intake | Create cases |
| B2 — Case Lifecycle | Manage cases |
| B3 — Case Financial | SSM handles financial fields |
| C1 — Task Assignment | Manage tasks |
| C2 — Task Completion | Complete tasks |
| A3 — Quote Lifecycle | Create and manage quotes |
| A2 — Cost Accessibility | SSM manages cost (NOT price) |
| D1 — WorkOrder Creation | Create work orders |
| E1 — Asset View | View assets |
| F1 — Pricing Execution | Execute pricing requests |
| G5 — Business Rule Read-Only | View rules |
| I2 — Genesys Control | Manage routing |
| J1 — Communication Send | Send emails |
| H3 — Contact Management | Manage contacts |

### PSG_Sales_Agent
| Permission Set | Rationale |
|---------------|-----------|
| A3 — Quote Lifecycle | Create and manage quotes |
| A1 — Price Accessibility | Sales manages price (NOT cost) |
| A4 — Quote Read-Only | View all quote data |
| B5 — Case Read-Only | View cases |
| E1 — Asset View | View assets |
| F2 — Pricing Read-Only | View pricing requests |
| H1 — Account Management | Manage accounts |

### PSG_Vendor_Relations
| Permission Set | Rationale |
|---------------|-----------|
| D1 — WorkOrder Creation | Create work orders |
| D2 — WorkOrder Cost Management | Manage vendor costs |
| D3 — WorkOrder Scheduling | Schedule vendor services |
| A2 — Cost Accessibility | Manage cost side of quotes |
| B5 — Case Read-Only | View cases |
| E4 — Asset Configuration | Configure assets |
| F1 — Pricing Execution | Execute pricing |
| L7 — Escalation Maintenance | Manage vendor escalations |
| J1 — Communication Send | Communicate with vendors |

### PSG_Compliance
| Permission Set | Rationale |
|---------------|-----------|
| B5 — Case Read-Only | Audit cases |
| A4 — Quote Read-Only | Audit quotes |
| D4 — WorkOrder Read-Only | Audit work orders |
| G5 — Business Rule Read-Only | Audit rules |
| F2 — Pricing Read-Only | Audit pricing |
| K2 — Report Creator | Create compliance reports |
| L11 — View Setup | View configuration |

### PSG_Business_Rule_Administrator
| Permission Set | Rationale |
|---------------|-----------|
| G1 — Business Rule Admin | Configure rules |
| G2 — Service Approver Config | Configure approvers |
| L2 — Project Services | Manage project codes |
| B5 — Case Read-Only | Context for rule creation |
| A4 — Quote Read-Only | Context for rule creation |

**Note:** PSG_Business_Rule_Administrator deliberately EXCLUDES G3 (Approval Decision) to enforce SoD.

### PSG_IT_Support
| Permission Set | Rationale |
|---------------|-----------|
| F3 — STP Administration | Configure STP criteria |
| I2 — Genesys Control | Manage routing config |
| L1 — Knowledge Management | Manage knowledge base |
| L4 — Flow Management | Manage flows |
| L5 — Market Area Alerts Admin | Configure alerts |
| L11 — View Setup | View configuration |
| K3 — Report Administrator | Manage reporting infrastructure |

---

## Migration Path from Existing Permission Sets

| Existing Permission Set | Action | New PS |
|------------------------|--------|--------|
| Price_Accessibility_Permission_Set | **RETAIN** | A1 — PS_Quote_Price_Accessibility |
| Cost_Accessibility_Permission_Set | **RETAIN** | A2 — PS_Quote_Cost_Accessibility |
| CPQReadOnly | **RETAIN** | A4 — PS_Quote_Read_Only |
| QuoteOrdersUser | **REPLACE** | A3 — PS_Quote_Lifecycle (split out financial fields) |
| MAS_Permissionset | **RETAIN** | A6 — PS_Quote_MAS_Integration |
| Pricing_Access | **RETAIN** | F1 — PS_Pricing_Request_Execution |
| Pricing_Read_Only | **RETAIN** | F2 — PS_Pricing_Request_Read_Only |
| STP_Administration | **RETAIN** | F3 — PS_STP_Administration |
| Business_Rule_Notification | **REFACTOR** | G1 + G2 (split rule admin from approver config) |
| SBS_Account_Management | **REFACTOR** | G1 + G2 (absorb into rule admin/approver config) |
| Project_Services_Project_Management | **RETAIN** | L2 — PS_Project_Services |
| Governance_Team | **RETAIN** | L3 — PS_Governance_Team |
| Task_Genesys_Routing_Permission | **RETAIN** | I2 — PS_Genesys_Routing_Control |
| AAV_Availability_Stand_Alone_Tool | **CONSOLIDATE** | E3 — PS_Asset_Availability_Tool |
| Asset_Availability_User_Permission_Set | **CONSOLIDATE** | E3 — PS_Asset_Availability_Tool |
| Reports_and_Dashboards_Administrator | **RETAIN** | K3 — PS_Report_Administrator |
| Reports_and_Dashboards_Super_User | **RETAIN** | K2 — PS_Report_Creator |
| Customer_Service_Reporting_User | **RETAIN** | L6 — PS_Customer_Service_Reporting |
| Contact_Notification_Maintenance | **ABSORB** | H3 — PS_Contact_Management |
| Account_Notification_Maintenance | **RETAIN** | H5 — PS_Notification_Preferences |
| Merge_Access_for_Non_Admin_Users | **RETAIN** | H4 — PS_Contact_Merge |
| Manage_Premium_Deliveries | **RETAIN** | L10 — PS_Premium_Delivery_Management |
| Knowledge_Manager_User | **RETAIN** | L1 — PS_Knowledge_Management |
| Manage_Flows | **RETAIN** | L4 — PS_Flow_Management |
| MAA_Admin_Panel_Team | **RETAIN** | L5 — PS_Market_Area_Alerts_Admin |
| Escalation_Maintenance_Permissions | **RETAIN** | L7 — PS_Escalation_Maintenance |
| Launch_Fast | **RETAIN** | L8 — PS_Launch_FAST |
| Digital_Transformation_Time_Tacking | **RETAIN** | L9 — PS_Digital_Transformation_Tracking |
| View_Setup_and_Configuration | **RETAIN** | L11 — PS_View_Setup |
| Modify_All_Data | **RETAIN** | L12 — PS_Modify_All_Data |
| Password_Never_Expires | **RETAIN** | L13 — PS_Password_Never_Expires |
| **NEW** | **CREATE** | B1 — PS_Case_Intake |
| **NEW** | **CREATE** | B2 — PS_Case_Lifecycle_Management |
| **NEW** | **CREATE** | B3 — PS_Case_Financial |
| **NEW** | **CREATE** | B4 — PS_Case_SLA_Override |
| **NEW** | **CREATE** | B5 — PS_Case_Read_Only |
| **NEW** | **CREATE** | C1 — PS_Task_Assignment |
| **NEW** | **CREATE** | C2 — PS_Task_Completion |
| **NEW** | **CREATE** | C3 — PS_Task_Read_Only |
| **NEW** | **CREATE** | D1 — PS_WorkOrder_Creation |
| **NEW** | **CREATE** | D2 — PS_WorkOrder_Cost_Management |
| **NEW** | **CREATE** | D3 — PS_WorkOrder_Scheduling |
| **NEW** | **CREATE** | D4 — PS_WorkOrder_Read_Only |
| **NEW** | **CREATE** | A3 — PS_Quote_Lifecycle_Management |
| **NEW** | **CREATE** | A5 — PS_Quote_Approval |
| **NEW** | **CREATE** | E1 — PS_Asset_View |
| **NEW** | **CREATE** | E2 — PS_Asset_Financial |
| **NEW** | **CREATE** | E4 — PS_Asset_Configuration |
| **NEW** | **CREATE** | G3 — PS_Approval_Decision |
| **NEW** | **CREATE** | G4 — PS_NTE_Approval |
| **NEW** | **CREATE** | G5 — PS_Business_Rule_Read_Only |
| **NEW** | **CREATE** | H1 — PS_Account_Management |
| **NEW** | **CREATE** | H2 — PS_Account_Financial_Configuration |
| **NEW** | **CREATE** | J1 — PS_Communication_Send |
| **NEW** | **CREATE** | J2 — PS_Communication_Read_Only |

**Summary:** 20 permission sets retained as-is, 3 refactored/replaced, 2 consolidated, 1 absorbed, and 24 net-new permission sets created. Total: **47 permission sets**.
