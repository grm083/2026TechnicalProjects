# Feature Rationalization: Mapping Codebase Capabilities to Permission Sets

**Document Type:** Technical Analysis
**Version:** 1.0
**Date:** March 12, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT - Ready for Review
**Purpose:** Analyze the complete codebase (Apex, LWC, Aura, Flows, Triggers, Objects) and rationalize into discrete feature groupings that map to permission sets.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Methodology](#methodology)
3. [Codebase Inventory Summary](#codebase-inventory-summary)
4. [Rationalized Feature Groupings](#rationalized-feature-groupings)
5. [Feature-to-Permission-Set Mapping](#feature-to-permission-set-mapping)
6. [Feature-to-PSG Mapping: Which Roles Get Which Features](#feature-to-psg-mapping)
7. [Existing Permission Sets: Gap Analysis](#existing-permission-sets-gap-analysis)
8. [Appendix: Complete Component Inventory by Feature](#appendix)

---

## Executive Summary

A comprehensive review of the Salesforce codebase reveals **~850 discrete components** (405 Apex classes, 204 Aura components, 42 LWC components, 101 flows, 32 triggers, 65+ custom objects) that deliver the platform's functionality.

These components can be rationalized into **16 distinct business features**. Each feature represents a coherent set of capabilities that a user either needs access to or doesn't — making them natural boundaries for permission sets.

The existing 31 permission sets partially align to these features but have significant gaps in coverage and consistency. The proposed model replaces them with **21 feature-based permission sets** (16 core + 5 tiered variants for features that need User/Admin split access).

### Key Finding

The codebase is dominated by four interconnected features that together account for ~70% of all components:

| Feature | % of Codebase | Complexity |
|---------|--------------|------------|
| Case Management | ~25% | Very High — touches nearly every other feature |
| Quote/CPQ Management | ~20% | Very High — pricing engine, multi-vendor, approvals |
| Task Management | ~12% | High — Genesys integration, framework-driven |
| Business Rules & Approvals | ~12% | High — cross-cutting rules engine |

These four features form the operational core and must be permission-set-accessible to most user roles.

---

## Methodology

### Sources Analyzed

| Source | Count | Method |
|--------|-------|--------|
| Apex Classes (non-test) | 405 | Name analysis + code review of key classes |
| Aura Components | 204 | Component markup + controller/helper review |
| LWC Components | 42 | JS module + HTML template review |
| Flows | 101 | Flow metadata + element analysis |
| Triggers | 32 | Trigger body + handler pattern review |
| Custom Objects | 65+ | Object + field metadata review |
| Existing Permission Sets | 31 | Permission set metadata review |
| Custom Metadata Types | 40+ | MDT structure + record review |

### Grouping Criteria

Components were grouped into features based on:

1. **Object affinity** — Which SObjects does the component primarily operate on?
2. **UI surface** — Which page/tab/action does the component render on?
3. **Trigger chain** — Which trigger handler calls which helpers?
4. **Flow orchestration** — Which flows call which subflows?
5. **Business process** — What user-facing business process does this serve?
6. **Access pattern** — Who needs this? Does it make sense to grant/deny as a unit?

---

## Codebase Inventory Summary

### Component Distribution

```
Apex Classes (405)
├── Case Management .............. 52 classes
├── Quote/CPQ .................... 62 classes
├── Task Management .............. 28 classes
├── Work Order ................... 18 classes
├── Pricing Engine ............... 32 classes
├── Business Rules & Approvals ... 30 classes
├── Asset & Availability ......... 16 classes
├── Genesys/CTI Integration ...... 18 classes
├── Vendor Management ............ 12 classes
├── Communication & Email ........ 22 classes
├── Entitlement/SLA .............. 8 classes
├── Account/Contact .............. 20 classes
├── Integration/API .............. 24 classes
├── Reporting/Dashboard .......... 8 classes
├── User/Queue Management ........ 12 classes
├── Exception Logging ............ 12 classes
├── System Config & Utilities .... 31 classes
└── Framework (Trigger/Batch) .... 20 classes

Aura Components (204)
├── Case Management .............. 42 components
├── Quote/CPQ .................... 28 components
├── Task Management .............. 15 components
├── Work Order ................... 10 components
├── Pricing & Approval .......... 12 components
├── Asset Management ............. 10 components
├── Vendor Management ............ 8 components
├── Communication ................ 12 components
├── Dashboard/Reporting .......... 8 components
├── Account/Contact .............. 6 components
├── Location/Availability ........ 6 components
├── User/Queue ................... 6 components
├── Flow Integration ............. 6 components
├── Genesys/CTI .................. 4 components
├── Utilities & Events ........... 31 components

LWC Components (42)
├── Asset Availability (AAV) ..... 10 components
├── Quote/CPQ .................... 5 components
├── Pricing ...................... 4 components
├── Case/Business Rules .......... 8 components
├── Communication ................ 8 components
├── Vendor ...................... 3 components
├── Work Order ................... 1 component
├── Utilities .................... 3 components

Flows (101)
├── Case Management .............. 23 flows
├── Task Management .............. 17 flows
├── Work Order ................... 9 flows
├── Quote/CPQ .................... 11 flows
├── Account/Contact .............. 7 flows
├── Approval/Business Rules ...... 7 flows
├── Genesys Integration .......... 11 flows
├── Pricing ...................... 5 flows
├── Admin/Utility ................ 11 flows
```

---

## Rationalized Feature Groupings

After analyzing all ~850 components, they rationalize into **16 discrete features**. Each feature is a self-contained set of capabilities that makes sense to grant or deny as a unit.

### Feature 1: Case Lifecycle Management

**What it does:** Create, edit, track, close, and clone customer service cases. Includes case status/substatus workflows, SLA date management, case highlight panels, case-to-case navigation, duplicate detection, and case reassignment.

**Objects:**
- Case (Standard — heavily customized)
- Case_History_Tracker__c
- Case_Asset_Header__c
- Case_Process_Manager__c
- Case_Task_Tracker__c
- SBS_Case_Asset__c
- Intake_Process__c

**Key Apex Classes (52):**
CaseTriggerHandler, CaseTriggerHelper, CaseController, CaseCreation, CaseDetailHelper, CaseUpdateHandler, CaseEntitlement, CaseSLAEntitlementUTIL, CaseApprovalHandler, CaseAssetTriggerHandler, CaseAssetTriggerHelper, CaseAssetController, CaseAssetControllerPopUp, CaseAttachUploadCntrlr, CaseCommentsControllerExtension, CaseCustomLookUpController, CaseRulesModalCtrl, CaseHistoryTrackerTriggerHandler, CustomCaseCreationCntrlr, CustomCaseHighlightPanelCntrl, CloneApprovalRules, DuplicateCheckOnCaseController, MultipleCaseCreation (batch creation), ProgressCaseComponentController, CreateCaseHistory, AssetHeadersForCaseController, GetCaseInformation, GetChildCase, SetCaseCustomerInfo (via flows), ShowAllOpenCases, MyOpenCaseListController, IntakeProcessAuraHandler, changeRecordTypeController, subStatusPathController, caseService, BalePickupCaseService, ExtraPickupHandler, CreatePickupCaseAPI, UpdateCasePO, CloseAcornTicket, ReopenAcornTicket, ReassignAcornTicket, and supporting classes.

**Aura (42):** CaseCreationComponent, CaseActivityTimeline, CaseAssetComponent, CaseHighlightPanel, CaseEditComponent, CaseNavigation, CaseReassignment, CloseCasePop, CloneCaseCreation, MultipleCaseCreation, MyOpenCases, ShowAllOpenCases, ProgressCaseComponent, DuplicateCheckOnCase, FillCaseSubType, AddComment, CustomCommentContainer, and more.

**LWC (8):** allRulesModal, caseRulesModal, changeRecordTypeCard, changeRTCard, populateCaseSubType, multiAssetCaseCard, customCaseComment, viewComments

**Flows (23):** Case_Update_Process, Validate_Case, Case_Sub_Status, Email_to_Case, Master_Intake_Flow, createNewServiceCase, and 17 more.

**Triggers (3):** CaseTrigger, CaseCommentTrigger, CaseHistoryTrackerTrigger, CaseAssetTrigger

---

### Feature 2: Task Management & Framework

**What it does:** Create, assign, escalate, complete, and delete tasks. Includes the Task Framework (metadata-driven task creation), task bundling dashboard, personal queue management, out-of-office reassignment, and multi-case task operations.

**Objects:**
- Task (Standard — extended)
- Complete_Task__c
- Task_Genesys_Routing_Control__c
- Personal_Queue_Info__c
- Out_of_Office__c
- Task_Framework__mdt
- Task_Subject_Description_Mapping__mdt

**Key Apex Classes (28):**
TaskTriggerHandler, TaskTriggerHelper, MyTaskListController, GenTaskController, AsyncCompleteTask, ChangeTaskAssignmentcntrl, CreatePendingInformationTask, ValidateTaskToPopMessage, TaskPopUpMessageController, PersonalQueueTriggerHandler, PersonalQueueTriggerHelper, PersonalQueueRecDelete, PersonalQueueTaskClosureBatch, PersonalQueueTicketAssignmentTaskBatch, OutofOfficeTriggerHandler, OutofOfficeTriggerHelper, MultiCaseTaskPopuCntrl, ConcatenateTaskDetailForAcorn, TaskAndGenesysPETriggerHelper, GetTaskRecursionCheck, PutTaskRecursionCheck, TaskRelatedListAura, SupervisorDashboardCls, and supporting classes.

**Aura (15):** ManualTaskCreation, MyOpenTasks, TaskModalDialog, CreatePendingInformationTask, OpenTaskQueue, OpenTaskQueueAll, ShowAllOpenTasks, TaskBundlingDashboard, multiCaseTaskPopUp, and more.

**Flows (17):** Task_Assignment, Creation_of_Task, Create_Task_Genesys_Routing, Process_on_Task_Completion, Task_Delete, Followup_Task_Creation, Change_Task_Assignment, and 10 more.

**Triggers (2):** TaskTrigger, TaskAndGenesysPETrigger

---

### Feature 3: Quote/CPQ Lifecycle Management

**What it does:** Create, configure, assign, lock/unlock, approve, and fulfill CPQ quotes. Includes quote line management, quote summary, quote team assignment, quote favorites, quote cloning, and quote-to-order conversion.

**Objects:**
- SBQQ__Quote__c
- SBQQ__QuoteLine__c
- SBQQ__ConfigurationAttribute__c
- SBQQ__ProductFeature__c
- SBQQ__ProductOption__c
- Quote_Order__c
- QuoteApproval__c
- Quote_Line_History_Tracking__c
- Quote_Action_Framework__mdt
- Quote_Teams_Framework__mdt

**Key Apex Classes (62):**
QuoteTriggerHandler, QuoteTriggerHelper, QuoteCreationHandler, QuoteSelector, QuoteLineCreationHandler, QuoteLineTriggerHandler, QuoteLineTriggerHelper, QuoteLineSelector, QuoteLineService, QuoteLineServices, QuoteLineScheduleAOverride, QuoteActionsController, QuoteApproval, QuoteApprovalHandler, QuoteDecline, QuoteEmailHandler, QuoteFavoritesController, QuoteOnlyController, QuoteOrderTriggerHandler, QuoteOrderTriggerHelper, QuoteProcurementController, QuotePriorityChangeBatch, GetQuoteSummary, ShowQuoteLineHistoryController, CalculateQuotePriority, AsyncUpdateQuoteFlag, QuoteLineClassificationChanges, RemovalQuoteLineHandler, SBQQConfigurationRuleSelector, SBQQConfigurationRuleService, SBQQProductOptionSelector, SBQQQuoteService, ProductRulesExecutor, ProductServices, AssetQuoteProcurementController, QouteValiationHandler, validateProductQuoteOrder, and supporting classes.

**Aura (28):** QuoteCreationWrapper, QuoteOverview, QuoteProducts, QuoteProductDetails, QuoteOrderDetails, QuoteSummaryConfirmation, QuoteFavorites, CentralizedQuoteActions, ExistingQuoteModal, QuoteResyncAction, GetQuotePricing, GetQuoteSTP, ShowPricingOnQuote, showQuoteLineHistory, TeamQuoteAll, TeamUserQuotes, and more.

**LWC (5):** quoteDetailsComp, quoteOrderComp, quoteSummaryComp, quotelineDetailsComp, multiVendorPricingResponse

**Flows (11):** Quote_Assignment_Flow, Quote_Status_Change_Flow, Quote_Genesys_Routing_Autoflow, Flow_to_Lock_and_UnLock_Quote, and 7 more.

**Triggers (3):** QuoteTrigger, QuoteLineTrigger, QuoteOrderTrigger

---

### Feature 4: Pricing Engine

**What it does:** Create and process pricing requests, execute STP (Straight-Through Processing) pricing rules, handle multi-vendor pricing, calculate costs, and integrate with external pricing APIs.

**Objects:**
- Pricing_Request__c
- PricingJsonSetting__mdt
- PricingRequestOutputField__mdt
- PricingSTP__mdt
- Pricing_Threshold_Settings__mdt
- Pricing_Response_Process_Quote_Line__mdt

**Key Apex Classes (32):**
PricingRequest, PricingRequestHandler, PricingRequestHelper, PricingRequestAPIIntegration, PricingJSONRequest, PricingRequestJsonDeserialize, PricingRequestSelector, PricingRequestMultiVendorSTPProcess, PricingRequestSTPProcess, PricingRequestResponseBatch, PricingResponseProcessor, PricingReportingFieldsMetadata, PricingRequestFieldsMetadata, PricingChangeRequest, PriceOnlyRequestSTPProcess, ProcessQLIPricingRequest, CreatePricingRequest, Pricing_Constant_Util, ExhibitPriceServices, UpdateQuantityClientPrice, and supporting classes.

**Aura (3):** NewPricingRequest, GetQuotePricing, ShowPricingOnQuote

**LWC (4):** pricingRequestInput, pricingOutputScreen, pricingMultiVendorOutputScreen, pubsub (shared messaging)

**Flows (5):** Pricing-related subflows integrated into quote and case flows.

**Triggers (1):** PricingRequestTrigger

---

### Feature 5: Work Order Management

**What it does:** Create, process, and track work orders and work order line items. Includes service date management, ETA tracking, work order PDF generation, Acorn ERP integration, and service scheduling.

**Objects:**
- WorkOrder (Standard — 50+ custom fields)
- WorkOrderLineItem
- ServiceAppointment
- WOCreation__mdt

**Key Apex Classes (18):**
WorkOrderTriggerHandler, WorkOrderTriggerHelper, WorkOrderTriggerAction, WorkOrderController, WorkOrderLineItemTriggerHandler, WorkOrderLineItemTriggerHelper, MultipleWorkorderController, UpdateWorkOrder, WorkOrderWebservices, WorkOrderReportCtrl, GetWorkOrderPDFCntrlr, ETAWindowController, BatchUpdateWorkOrderLineItem, NewServiceFlowClass, and supporting classes.

**Aura (10):** WorkOrderPDFComp, WorkOrderReportLink, ETAOnWorkOrder, ETAWindowComponent, ETAWindowComponentWO, NotificationRecordsCmpWO, ServiceDateContainer, WMCapacity, ServiceScheduler, ServiceApprovers

**LWC (1):** acornWODetails

**Flows (9):** Work_Order_Creation, Work_Order_Process, Actions_for_the_Work_Order, Recreate_Work_Order, New_Service_Flow, Update_Service_date, and 3 more.

**Triggers (2):** WorkOrderTrigger, WorkOrderLineItemTrigger

---

### Feature 6: Asset Management & Availability (AAV)

**What it does:** Track customer assets, view asset availability, search assets by location, manage asset-case relationships, and integrate with the Asset Availability View (AAV) API for delivery date calculations and container alternatives.

**Objects:**
- Asset (Standard — extended)
- AAV_Asset_Availability__c
- SBS_Case_Asset__c
- Asset_Quoteline_Mapping__mdt
- Notification_Asset__c

**Key Apex Classes (16):**
AssetTriggerHandler, AssetTriggerHelper, AAV_APIIntegration, AAV_AvailabilityUtility, AAV_AvailbilityAppHelper, AvailabilityAPIJsonDeserialize, AssetQuerySelector, assetCustomTreeGridController, AssetHeadersForCaseController, DisplayCaseAssetController, AlternateServiceController, LocationContainerController, updateAcornAssetLocation, PotentialDeliveryDate, PotentialPickupDateAPI, and supporting classes.

**Aura (10):** AssetDetailsTreeGrid, DisplayCaseAssets, LocationAssetSearch, aavNewAvailabilityButton, AccountTeamsTable, ContactByRoleComponent, FinancialDetailComponent, and more.

**LWC (10):** aavAlternateContainers, aavAppInputPanel, aavAppOutputDeliverySection, aavAppOutputOutageSection, aavAppOutputPanel, aavAppOutputServiceSection, aavCustomDatePicker, aavDeliveryDatesUI, aavReusablePagination, aavUtilityMethods

---

### Feature 7: Business Rules Engine

**What it does:** Evaluate, select, and apply configurable business rules to cases, quotes, and approvals. Includes NTE (Not-to-Exceed) rules, company category rules, business rule cloning, rule-driven field updates, and rule notification display.

**Objects:**
- Business_Rule__c
- Business_Rule_Field_Mapping__mdt
- STP_Criteria__c
- Categorization__c
- Category__c
- Disposition__c

**Key Apex Classes (18):**
BusinessRuleTriggerHandler, BusinessRuleTriggerHelper, BusinessRuleHelper, BusinessRuleUtility, BusinessRuleCtrl, BusinessRuleNSCHelper, BR_RelatedListController, NTEApprovalRuleHelper, CloneApprovalRules, STPCriteriaSelector, STPCriteriaService, STPRuleExecution, STPExceptionUtil, STPProcessEventTriggerHandler, STPProcessTriggerHelper, BooleanExpression, BooleanStringConverter, OperatorExpression

**Aura (6):** BR_RelatedList, caseBusinessRuleTab, locationBusinessRuleTab, OpenBusinessRulesReport, GetBusinessRulesforApprovers, DynamicQuestions

**LWC (3):** allRulesModal, caseRulesModal, ntebRulesModal

**Flows (7):** Business_Rule_Selection, Approval_Business_Rule, Business_Rules_Automation_Flow, CustomCloningBusinessRule, Business_Rule_Company_Category, Field_Update_On_Business_Rule, Business_Rule_Chatter_Feed_Flow

**Triggers (2):** BusinessRuleTrigger, STPProcessEventTrigger

---

### Feature 8: Approval Workflows

**What it does:** Manage multi-level approval workflows for quotes, services, and NTE thresholds. Includes approval log tracking, service approver routing, approval images/documentation, and automated approval email notifications.

**Objects:**
- Approval_Log__c
- Service_Approver__c
- ApprovalImages__c
- Quote_Approval_Priority_Setting__mdt

**Key Apex Classes (12):**
QuoteApproval, QuoteApprovalHandler, CaseApprovalHandler, ServiceApproverHandler, ServiceApproverHelper, ServiceApproverFuzzyMatch, GetServiceApprover, GetDeclinedApproverLogData, ReqInfoServiceApprovers, AutoSendEmailToServiceApprovers, SendEmailToServiceApproversCntrlr, ToActivateServiceApprovers, AddNTERulesCtrl, NTEBRRulesModalCtrl, GetBRQuotePriorityNTECtrl, showApprovalLogs

**Aura (5):** GetApproverDetails, ServiceApprovers, showApprovalLogs, GetBusinessRulesforApprovers, FetchServiceApproverEvent

**LWC (1):** addNTERulesSA

**Flows (4):** Approval_Business_Rule, Approval_Log, Approval_Log_Task_Creation, Business_Rules_Automation_Flow

**Triggers (2):** ApprovalLogTrigger, ServiceApproverTrigger

---

### Feature 9: Genesys/CTI Integration

**What it does:** Integrate with Genesys contact center for inbound/outbound call routing, screen pops, IVR service status, email-to-quote routing, and task-Genesys synchronization. Drives which users receive routed work based on UCC.

**Objects:**
- Genesys_Routing__c
- Genesys_Reporting__c
- Task_Genesys_Routing_Control__c
- Task_and_Genesys_Platform_Event__e
- QuoteGenesysEmailToQuote__mdt

**Key Apex Classes (18):**
Screenpop, ScreenpopController, IVRExitController, IVRUtility, IVRContainerServices, IVRServiceStatusWebService, IVRServiceStatusWebService_V1, IVRServiceStatusETA, IVRServiceStatusETA_V1, GetSFDCServiceFlag, GetIVRCasePrompt, TaskAndGenesysPETriggerHelper, CreateGenesysForQuoteBatch, CreateGenesysRecordBatch, BatchToCreateGenesysForPITasks, ScheduleCreateGenesysForQuoteBatch, ScheduleCreateGenesysForTask, and supporting classes.

**Aura (4):** IVRExitPoint, TwoWayCommunication, PortalMessages, closeEmailTaskComponent

**LWC (1):** chatNowTranscript (transcript retrieval)

**Flows (11):** Create_Genesys_Routing, Integration_Task_and_Genesys_Routing, Quote_Genesys_Routing_Autoflow, Outbound_Message_to_Genesys, Modify_the_Last_Agent, Determine_and_Return_Last_Agent_Id, and 5 more.

**Triggers (1):** TaskAndGenesysPETrigger

---

### Feature 10: Communication & Email Management

**What it does:** Manage customer communications including email-to-case, two-way messaging, chat transcripts, case comments, portal messages, email template rendering, and notification preference management.

**Objects:**
- EmailMessage (Standard)
- SFDCEmailMessage__c
- Comment__c
- Account_Notification_Preference__c
- Contact_Notification_Preference__c
- Communication_Channel__c
- Notification_Contact__c
- Two_way_communication__mdt
- Email_Alias__mdt

**Key Apex Classes (22):**
EmailMessageTriggerHandler, EmailMessageTriggerHelper, EmailMessageHelper, EmailMessageCreation, EmailMessageContactMapping, EmailMessageProcessorExtension, EmailService, FetchEmailMessages, CommentController, CustomCommentController, InvocableFlowEmail, GetToAddress, getDetailsForEmail, TwoWayService, TwoWayServiceRevision, ContactTextOptInInvokableAPI, ContactTextOptOutInvokableAPI, NotifTrackingWrapper, NotificationTrackingController, SendAlert, NotifyCustomerOfDelayEmailController, ChatNowTranscriptResponse, ChatTranscriptPdfCtrl

**Aura (12):** TwoWayCommunication, EmailDetailViewApp, EmailDetailViewComponent, EmailMessageList, EmailRelatedListComponent, EmailViewWithCaseEditComp, FetchEmailMessagesComponent, CopyEmailToComment, PortalMessages, ShowExternalComments, ExternalComments, HoverOverCards

**LWC (6):** chatNowTranscript, customCaseComment, emailMessageInput, sendAlert, updatePortal, viewComments

**Triggers (2):** EmailMessageTrigger, CommentTrigger

**Flows (3):** EMailMessageUpdate, Email_Notification_for_Vendor_and_Customer, Process_for_update_Case_Comment

---

### Feature 11: Vendor & Supplier Management

**What it does:** Search, select, and manage vendors. Includes vendor escalation contacts, vendor scorecarding, vendor service location codes, local vendor lookup, and vendor communication channels.

**Objects:**
- Account (Vendor record types)
- SBS_Supplier_Scorecard__c
- Vendor_Contact_Role_Map__mdt
- Vendor_Service_Location_Code__c (referenced)

**Key Apex Classes (12):**
VendorEscalationContactController, GetVendorContact, getLocalVendorController, VCRCodeController, SendEmailToWMVendorCtrl, MapSortService, ContactSearchandCreate, FetchAccountContactByRole, and supporting classes.

**Aura (8):** VendorContainer, VendorSearch, VendorLookupComponent, ShowLocalVendors, maintainVendorEscalationConOverrideButton, MASLookupComponent, SearchExistingContact, ContactByRoleComponent

**LWC (3):** maintainVendorEscalationCom, maintainVendorEscalationContact, assetHoverCard

**Flows (3):** Get_Contact_And_Vendor_Details, Delete_Vendor_Service_Location_Code, Supplier_Score_Trending

---

### Feature 12: Entitlement & SLA Management

**What it does:** Manage service entitlements, SLA calculations, SLA tracking on cases, and service contract management. Includes internal/external SLA dashboards and entitlement assignment on account activation.

**Objects:**
- Entitlement (Standard)
- ServiceContract (Standard)
- sla_calculation__c
- Industry_Standard_SLA__mdt

**Key Apex Classes (8):**
EntitlementTriggerHelper, CaseEntitlement, CaseSLAEntitlementUTIL, GetSLAInformation, BusinessDays, GetBusinessDelayTime, InvocableBusinessHours, StartDateManagement

**Aura (2):** ExternalSLA, InternalSLA

**Flows (2):** Update_Entitlement, Create_SLA_upon_activating_Account

**Triggers (1):** EntitlementTrigger

---

### Feature 13: Account & Contact Management

**What it does:** Manage customer accounts, contacts, account team members, contact notification preferences, account titles, and account-contact relationships.

**Objects:**
- Account (Standard)
- Contact (Standard)
- AccountContactRelation (Standard)
- AccountTeamMember (Standard)
- Account_Position__c
- Account_Title__c
- Client_Account_Numbers__c
- Account_Group_Role_Map__mdt

**Key Apex Classes (20):**
AccountContactRelationHandler, AccountContactRelationHelper, AccountContactRelationTriggerHandler, AccountContactRelationTriggerHelper, AccountTeamMemberQueryAction, AccountTeamMemberUIController, AccountTitleTriggerHandler, AccountTitleTriggerHelper, ContactTriggerHandler, ContactTriggerHelper, ContactNotifyPrefTriggerHandler, ContactNotifyPrefTriggerHelper, ContactSearchandCreate, ContactMaintenanceBatch, DuplicateContactMergeBatch, BatchCreateUnspecifiedContacts, AcornCompanyController, AcornCompanyDetails, FetchAccountContactByRole, and supporting classes.

**Aura (6):** AccountTeamsTable, ContactByRoleComponent, CreateContactWithNewTitle, createNewAccountTitle, SearchExistingContact, CompanyCategoryComponent

**Flows (7):** Account_Team_Task_Creation, Add_Account_Team_Member, Delete_Account_Team_Member, Add_Self_Service_Eligible_on_Account_Creation, Populate_Common_Name, Populate_Preferred_Language, Get_Contact_And_Vendor_Details

**Triggers (3):** AccountContactRelationTrigger, ContactTrigger, ContactNotificationPreferenceTrigger, AccountTitleTrigger

---

### Feature 14: Market Area Alerts (MAA)

**What it does:** Configure, display, and manage geographic market area alerts with filtering by type, line of business, and date ranges.

**Objects:**
- MAA_Admin_Settings__c
- MAS_Setup_Detail__c
- Market_Area_Alerts_Settings__c

**Key Apex Classes (2):**
MarketAreaAlertController, MarketAreaAlertMockResponse

**LWC (1):** alertCard

**Aura (2):** MASLookupComponent (shared)

---

### Feature 15: Exception Logging & System Monitoring

**What it does:** Log, track, and manage system exceptions, errors, and debug information. Includes logging framework configuration, exception purging, error notification emails, and system log platform events.

**Objects:**
- ExceptionLog__c
- ExceptionLog_Settings__c
- System_Log__c
- System_Log_Event__e
- Logging_Framework_Control__c
- FAST_Activity_Log__c

**Key Apex Classes (12):**
Logger, UTIL_LoggingService, UTIL_UnhandledLoggingService, ExceptionDetailsServices, ExceptionModifier, ExceptionLogEmailSend, ExceptionHandlingScheduler, PopulateNewExceptionsEffectiveDate, BATCH_PurgeOldExcption, SCH_PurgeOldExcptionScheduler, SendErrorNotificationOnJobFailure, PlatformEventProcessor

---

### Feature 16: Reporting & Dashboards

**What it does:** Provide custom reporting views, supervisor dashboards, task bundling analytics, and report links. Includes the supervisor workflow grouping dashboard.

**Objects:**
- Report (Standard)
- Dashboard (Standard)
- Dashboard_Component_Data__mdt
- Digital_Transformation_Time_Tracking__c
- Project_Code__c

**Key Apex Classes (8):**
ReportController, SupervisorDashboardCls, LightningTableController, TableListCmpCls, ProjectCodeTriggerHandler, ProjectCodeTriggerHelper, ProjectCodeActiveChecker, and supporting classes.

**Aura (8):** DashboardDataTable, SupervisorDashboardHeaderRegion, SupervisorWorkflowGroupingDashboard, TaskBundlingDashboard, ChartToggleBar, ReportLinks, CustomAppPageTemplate, CustomHomePageTemplate

---

### Cross-Cutting: System Configuration & Utilities

**Not a permission set feature** — these are framework-level classes and configuration objects that support all features. Access is controlled indirectly through the features they support.

**Objects:**
- Code_Switch__c (feature toggles)
- Config_PO__c
- Data_Store__c
- Max_RecursiveCall__c
- Object_Save_Mode__c
- Origin__c
- Generic_Values__mdt

**Key Apex Classes (31):**
TriggerDispatcher, TriggerHandler, TriggerActionBase, TriggerParameters, IHandler, iTriggerAction, RecurrsiveTriggerHandler, RecursionCheck, Constant_Util, ConstantClass, Pricing_Constant_Util, CodeSwitchUtility, FieldDescribeUtil, FieldSetReader, Date_Utility, Compactor_Utility, ValidationUtility, GetSobjectRecordTypeId, GetRecordLockedStatus, RESTHelper, IntegrationHandlerUtil, APICallUtility, DataStoreProcessor, MetadataSelector, SystemObjectSelector, OrgWideEmailSelector, GetUsername, ToolingAPIUtility, AvoidProcessBuilder, UTIL_ErrorConstants, UTIL_Picklist, SplitStringToListCntrlr, DependentPickListValueController, RecordComparator, WorkFlowMigration

---

## Feature-to-Permission-Set Mapping

### Proposed Permission Sets (21)

Based on the 16 features above, plus tiered access for features that need User vs. Admin separation:

| # | Permission Set API Name | Feature | Access Level | Key Object Permissions |
|---|---|---|---|---|
| 1 | `PS_Case_Management` | Case Lifecycle | Create/Edit cases, view case history | Case (CRUD), Case_History_Tracker__c (R), Case_Asset_Header__c (R), SBS_Case_Asset__c (RU), Intake_Process__c (RU) |
| 2 | `PS_Task_Management` | Task Management | Create/edit/complete tasks, manage personal queue | Task (CRUD), Complete_Task__c (RU), Personal_Queue_Info__c (CRUD own), Out_of_Office__c (CRUD own) |
| 3 | `PS_Quote_Management` | Quote/CPQ Lifecycle | Create/edit quotes and quote lines | SBQQ__Quote__c (CRUD), SBQQ__QuoteLine__c (CRUD), Quote_Order__c (RU), Quote_Line_History_Tracking__c (R) |
| 4 | `PS_Quote_Approval` | Quote/CPQ Approval | Approve/decline quotes | QuoteApproval__c (CRUD), SBQQ__Quote__c (RU), Approval_Log__c (CRUD) |
| 5 | `PS_Quote_Read_Only` | Quote/CPQ View-only | View quotes without editing | SBQQ__Quote__c (R), SBQQ__QuoteLine__c (R), QuoteApproval__c (R) |
| 6 | `PS_Pricing_Access` | Pricing Engine | Create/process pricing requests | Pricing_Request__c (CRUD), Quote_Line_History_Tracking__c (R) |
| 7 | `PS_Multi_Vendor_Pricing` | Pricing — Multi-Vendor | Multi-vendor pricing workflows | Pricing_Request__c (RU), vendor-related fields |
| 8 | `PS_Work_Order_Management` | Work Orders | Create/edit work orders and line items | WorkOrder (CRUD), WorkOrderLineItem (CRUD), ServiceAppointment (RU) |
| 9 | `PS_Asset_Management` | Asset & Availability | View/edit assets, use AAV tool | Asset (RU), AAV_Asset_Availability__c (R), SBS_Case_Asset__c (RU) |
| 10 | `PS_Business_Rules_User` | Business Rules (view) | View business rules, see applied rules on cases | Business_Rule__c (R), STP_Criteria__c (R), Categorization__c (R) |
| 11 | `PS_Business_Rules_Admin` | Business Rules (admin) | Configure business rules and STP criteria | Business_Rule__c (CRUD), STP_Criteria__c (CRUD), Categorization__c (CRUD), Disposition__c (CRUD) |
| 12 | `PS_Approval_Management` | Approval Workflows | View and participate in approvals | Approval_Log__c (RU), ApprovalImages__c (R), Service_Approver__c (R) |
| 13 | `PS_Approval_Administration` | Approval Admin | Configure approvers and routing | Approval_Log__c (CRUD), Service_Approver__c (CRUD), ApprovalImages__c (CRUD) |
| 14 | `PS_Genesys_CTI` | Genesys Integration | Receive routed work, screen pops | Genesys_Routing__c (R), Genesys_Reporting__c (R), Task_Genesys_Routing_Control__c (R) |
| 15 | `PS_Communication_Management` | Communication & Email | Manage notifications, two-way comms | Account_Notification_Preference__c (CRUD), Contact_Notification_Preference__c (CRUD), Communication_Channel__c (R), Comment__c (CRUD), SFDCEmailMessage__c (R) |
| 16 | `PS_Vendor_Management` | Vendor & Supplier | Manage vendors, scorecards, contacts | Account-Vendor RT (CRUD), SBS_Supplier_Scorecard__c (CRUD), Contact (CRUD) |
| 17 | `PS_Entitlement_Management` | Entitlement & SLA | Manage entitlements and SLA | Entitlement (CRUD), ServiceContract (RU), sla_calculation__c (CRUD) |
| 18 | `PS_Account_Contact_Management` | Account & Contact | Manage accounts, contacts, teams | Account (RU), Contact (CRUD), AccountTeamMember (via std), Account_Title__c (CRUD) |
| 19 | `PS_Market_Area_Alerts` | MAA (view) | View and receive alerts | MAA objects (R) |
| 20 | `PS_Exception_Log_User` | Exception Logging (view) | View error logs for troubleshooting | ExceptionLog__c (R), System_Log__c (R), FAST_Activity_Log__c (R) |
| 21 | `PS_Reporting_User` | Reporting (view/run) | View and run reports | Report (R), Dashboard (R), Run Reports |

**Additional Admin-tier permission sets (from existing analysis, unchanged):**
- `PS_Exception_Log_Admin` — Configure logging framework
- `PS_Integration_Admin` — Configure integrations
- `PS_Market_Area_Alerts_Admin` — Configure MAA
- `PS_Reporting_Creator` — Create reports/dashboards
- `PS_Reporting_Admin` — Full reporting admin
- `PS_System_Configuration` — System config objects (Code_Switch, etc.)
- `PS_Knowledge_Author` — Knowledge articles (create/edit)
- `PS_Knowledge_Publisher` — Knowledge articles (publish)
- `PS_Project_Time_Tracking` — Time tracking
- `PS_Organizational_Management` — Personal settings (Out_of_Office, Department)

**Total: ~31 permission sets** (21 core feature + 10 admin/specialized)

---

## Feature-to-PSG Mapping: Which Roles Get Which Features

This table shows which permission sets belong in each PSG, based on what each department actually uses in the codebase.

### PSG_Customer_Service (the largest — this is the operational core)

| Permission Set | Why |
|---|---|
| PS_Case_Management | Primary function — CSRs create and manage cases |
| PS_Task_Management | CSRs receive and complete tasks via Genesys |
| PS_Quote_Management | CSRs create standard quotes |
| PS_Pricing_Access | CSRs initiate pricing requests |
| PS_Work_Order_Management | CSRs create work orders from cases |
| PS_Asset_Management | CSRs view assets and use AAV tool |
| PS_Business_Rules_User | CSRs see applicable business rules on cases |
| PS_Approval_Management | CSRs view approval status |
| PS_Genesys_CTI | CSRs receive Genesys-routed work |
| PS_Communication_Management | CSRs manage customer notifications and comments |
| PS_Account_Contact_Management | CSRs view account/contact info |
| PS_Market_Area_Alerts | CSRs receive market area alerts |
| PS_Reporting_User | CSRs run reports |
| PS_Organizational_Management | Personal queue, out-of-office |
| **Total: 14 permission sets** | |

### PSG_Sales

| Permission Set | Why |
|---|---|
| PS_Case_Management | Sales handles escalated cases |
| PS_Task_Management | Sales receives and manages tasks |
| PS_Quote_Management | Sales creates complex quotes |
| PS_Quote_Approval | Sales approves/declines quotes |
| PS_Pricing_Access | Sales initiates pricing requests |
| PS_Asset_Management | Sales views asset information |
| PS_Business_Rules_User | Sales sees business rules |
| PS_Approval_Management | Sales participates in approvals |
| PS_Communication_Management | Sales manages customer communications |
| PS_Account_Contact_Management | Sales manages accounts and contacts |
| PS_Market_Area_Alerts | Sales receives alerts |
| PS_Reporting_User | Sales runs reports |
| PS_Organizational_Management | Personal settings |
| **Total: 13 permission sets** | |

### PSG_Fulfillment

| Permission Set | Why |
|---|---|
| PS_Quote_Management | Fulfillment works with quote fulfillment |
| PS_Pricing_Access | Fulfillment accesses pricing |
| PS_Multi_Vendor_Pricing | Fulfillment coordinates multi-vendor pricing |
| PS_Vendor_Management | Fulfillment manages vendors and scorecards |
| PS_Task_Management | Fulfillment receives and completes tasks |
| PS_Asset_Management | Fulfillment views asset information |
| PS_Work_Order_Management | Fulfillment coordinates work orders |
| PS_Business_Rules_User | Fulfillment views business rules |
| PS_Communication_Management | Fulfillment manages vendor/customer comms |
| PS_Account_Contact_Management | Fulfillment manages vendor accounts |
| PS_Reporting_User | Fulfillment runs reports |
| PS_Organizational_Management | Personal settings |
| **Total: 12 permission sets** | |

### PSG_Compliance

| Permission Set | Why |
|---|---|
| PS_Entitlement_Management | Primary function — SLA governance |
| PS_Quote_Read_Only | Compliance reviews quotes (read-only) |
| PS_Approval_Management | Compliance reviews approval workflows |
| PS_Business_Rules_User | Compliance reviews business rules |
| PS_Reporting_Creator | Compliance creates compliance reports |
| PS_Organizational_Management | Personal settings |
| **Total: 6 permission sets** | |

### PSG_IT_Support

| Permission Set | Why |
|---|---|
| PS_Exception_Log_User | Primary function — troubleshooting |
| PS_Quote_Read_Only | View quotes for troubleshooting |
| PS_Reporting_User | Run diagnostic reports |
| PS_Project_Time_Tracking | Track time (if applicable) |
| PS_Organizational_Management | Personal settings |
| **Total: 5 permission sets** | |

### PSG_System_Administrator

All permission sets at the Admin tier:
- PS_System_Configuration, PS_Business_Rules_Admin, PS_Approval_Administration, PS_Exception_Log_Admin, PS_Integration_Admin, PS_Market_Area_Alerts_Admin, PS_Knowledge_Publisher, PS_Reporting_Admin
- Plus all user-level permission sets as needed
- **Total: 20+ permission sets**

---

## Existing Permission Sets: Gap Analysis

### What Exists vs. What's Needed

| Existing Permission Set | Maps To Proposed | Status |
|---|---|---|
| CPQReadOnly | PS_Quote_Read_Only | Rename/align |
| Pricing_Access | PS_Pricing_Access | Rename/align |
| Pricing_Read_Only | (merge into PS_Quote_Read_Only) | Consolidate |
| QuoteOrdersUser | (merge into PS_Quote_Management) | Consolidate |
| Price_Accessibility_Permission_Set | (merge into PS_Pricing_Access) | Consolidate |
| Cost_Accessibility_Permission_Set | (merge into PS_Multi_Vendor_Pricing) | Consolidate |
| Task_Genesys_Routing_Permission | PS_Genesys_CTI | Rename/align |
| Escalation_Maintenance_Permissions | (merge into PS_Case_Management) | Consolidate |
| Business_Rule_Notification | (merge into PS_Business_Rules_User) | Consolidate |
| Governance_Team | (merge into PS_Approval_Management) | Consolidate |
| Account_Notification_Maintenance | (merge into PS_Communication_Management) | Consolidate |
| Contact_Notification_Maintenance | (merge into PS_Communication_Management) | Consolidate |
| AAV_Availability_Stand_Alone_Tool | (merge into PS_Asset_Management) | Consolidate |
| Asset_Availability_User_Permission_Set | (merge into PS_Asset_Management) | Consolidate |
| Reports_and_Dashboards_Administrator | PS_Reporting_Admin | Rename/align |
| Reports_and_Dashboards_Super_User | PS_Reporting_Creator | Rename/align |
| Customer_Service_Reporting_User | PS_Reporting_User | Rename/align |
| STP_Administration | (merge into PS_Business_Rules_Admin) | Consolidate |
| MAA_Admin_Panel_Team | PS_Market_Area_Alerts_Admin | Rename/align |
| MAS_Permissionset | (merge into PS_Market_Area_Alerts) | Consolidate |
| Knowledge_Manager_User | PS_Knowledge_Publisher | Rename/align |
| Digital_Transformation_Time_Tacking | PS_Project_Time_Tracking | Rename/align |
| SBS_Account_Management | (merge into PS_Account_Contact_Management) | Consolidate |
| Manage_Premium_Deliveries | (merge into PS_Work_Order_Management) | Consolidate |
| Launch_Fast | (evaluate — may be obsolete) | Review |
| Project_Services_Project_Management | (merge into PS_Work_Order_Management or PS_Project_Time_Tracking) | Consolidate |
| View_Setup_and_Configuration | (keep as PS_System_Configuration prereq) | Keep |
| Manage_Flows | (admin only — merge into PS_System_Configuration) | Consolidate |
| Modify_All_Data | (admin only — keep or retire) | Review |
| Merge_Access_for_Non_Admin_Users | (merge into PS_Account_Contact_Management) | Consolidate |
| Password_Never_Expires | (keep as standalone — security policy) | Keep |

### Summary

| Status | Count |
|--------|-------|
| Direct rename/align | 8 |
| Consolidate into proposed PS | 18 |
| Keep as-is | 2 |
| Review for retirement | 2 |
| **New permission sets needed** | **~10** |

### Missing Permission Sets (need to create)

These features have no existing permission set coverage:

| Proposed PS | Feature | No Existing Coverage Because |
|---|---|---|
| PS_Case_Management | Case Lifecycle | Permissions were embedded in profiles |
| PS_Task_Management | Task Management | Permissions were embedded in profiles |
| PS_Quote_Management | Quote/CPQ (edit) | Only read-only PS existed |
| PS_Work_Order_Management | Work Orders | Permissions were embedded in profiles |
| PS_Business_Rules_User | Business Rules (view) | Only notification PS existed |
| PS_Approval_Management | Approval Workflows (view) | No PS existed |
| PS_Approval_Administration | Approval Config | No PS existed |
| PS_Genesys_CTI | Genesys Integration | Only routing control PS existed |
| PS_Vendor_Management | Vendor/Supplier | No PS existed |
| PS_Entitlement_Management | Entitlement/SLA | No PS existed |

This confirms the gap identified in the Permission Strategy Analysis — the 4 highest-volume features (Case, Task, Quote edit, Work Order) had **no permission sets at all** because all access was embedded in profiles. This is the strongest argument for the migration.

---

## Appendix: Apex Class Access Requirements by Permission Set

Each permission set must include Apex Class Access for the classes that power its UI components and API endpoints. This is critical — without class access, Lightning components will fail even if object permissions are correct.

### PS_Case_Management — Required Apex Class Access

CaseController, CaseCreation, CaseDetailHelper, CaseAssetController, CaseAssetControllerPopUp, CaseAttachUploadCntrlr, CaseCommentsControllerExtension, CaseCustomLookUpController, CaseRulesModalCtrl, CustomCaseCreationCntrlr, CustomCaseHighlightPanelCntrl, DuplicateCheckOnCaseController, ProgressCaseComponentController, AssetHeadersForCaseController, GetCaseInformation, GetChildCase, MyOpenCaseListController, IntakeProcessAuraHandler, changeRecordTypeController, subStatusPathController, caseService, CreatePickupCaseAPI, BalePickupCaseService, CloseAcornTicket, ReopenAcornTicket, ReassignAcornTicket, CommentController, CustomCommentController, HoverCardController, HoverOverCardsCntrl

### PS_Task_Management — Required Apex Class Access

MyTaskListController, GenTaskController, AsyncCompleteTask, ChangeTaskAssignmentcntrl, CreatePendingInformationTask, ValidateTaskToPopMessage, TaskPopUpMessageController, MultiCaseTaskPopuCntrl, TaskRelatedListAura, PersonalQueueTriggerHandler (indirect), SupervisorDashboardCls

### PS_Quote_Management — Required Apex Class Access

QuoteActionsController, QuoteCreationHandler, QuoteFavoritesController, QuoteOnlyController, QuoteProcurementController, GetQuoteSummary, ShowQuoteLineHistoryController, QuoteLineClassificationChanges, AssetQuoteProcurementController, CalculateQuotePriority, SBQQQuoteService, ProductServices, ProductRulesExecutor

### PS_Pricing_Access — Required Apex Class Access

PricingRequest, PricingRequestHandler, PricingRequestHelper, PricingRequestAPIIntegration, PricingJSONRequest, PricingRequestJsonDeserialize, CreatePricingRequest, PricingResponseProcessor, PricingReportingFieldsMetadata, PricingRequestFieldsMetadata, ExhibitPriceServices

### PS_Work_Order_Management — Required Apex Class Access

WorkOrderController, MultipleWorkorderController, UpdateWorkOrder, GetWorkOrderPDFCntrlr, WorkOrderReportCtrl, ETAWindowController, WorkOrderWebservices, ServiceDateContainerController, ServiceSchedulerCtrl, NewServiceFlowClass

### PS_Asset_Management — Required Apex Class Access

AAV_APIIntegration, AAV_AvailabilityUtility, AAV_AvailbilityAppHelper, AvailabilityAPIJsonDeserialize, assetCustomTreeGridController, DisplayCaseAssetController, AlternateServiceController, LocationContainerController, PotentialDeliveryDate, PotentialPickupDateAPI

### PS_Business_Rules_User — Required Apex Class Access

BusinessRuleCtrl, BR_RelatedListController, AllRulesModalController, NTEBRRulesModalCtrl, GetBRQuotePriorityNTECtrl, SendBusinessRuleData

### PS_Genesys_CTI — Required Apex Class Access

Screenpop, ScreenpopController, IVRExitController, IVRUtility, IVRContainerServices, GetSFDCServiceFlag, GetIVRCasePrompt

### PS_Communication_Management — Required Apex Class Access

EmailService, FetchEmailMessages, CommentController, CustomCommentController, TwoWayService, TwoWayServiceRevision, NotificationTrackingController, SendAlert, NotifyCustomerOfDelayEmailController, GetChatNowTranscriptCtrl, ChatTranscriptPdfCtrl, CommunicationChannelViewController, UpdatePortal, viewComments

### PS_Vendor_Management — Required Apex Class Access

VendorEscalationContactController, GetVendorContact, getLocalVendorController, VCRCodeController, SendEmailToWMVendorCtrl, FetchAccountContactByRole, ContactSearchandCreate

### PS_Approval_Management — Required Apex Class Access

GetServiceApprover, GetDeclinedApproverLogData, ReqInfoServiceApprovers, showApprovalLogs (via Aura), AddNTERulesCtrl, NTEBRRulesModalCtrl

### PS_Market_Area_Alerts — Required Apex Class Access

MarketAreaAlertController

### PS_Exception_Log_User — Required Apex Class Access

ExceptionDetailsServices

### PS_Reporting_User — Required Apex Class Access

ReportController, SupervisorDashboardCls, LightningTableController, TableListCmpCls

---

**Document Status:** DRAFT
**Next Steps:**
1. Validate feature groupings with business stakeholders
2. Confirm Apex Class Access lists are complete (cross-reference with profile class access)
3. Build permission sets in sandbox
4. Map to PSGs and test with representative users from each UCC/role
**Document Owner:** George Martin, Salesforce Technical Architect

---

**END OF FEATURE RATIONALIZATION DOCUMENT**
