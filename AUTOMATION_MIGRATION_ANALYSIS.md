# Salesforce Automation Migration Analysis
## Process Builders & Workflow Rules Assessment

**Analysis Date:** January 15, 2026
**Total Process Builders:** 11
**Total Workflow Rules:** 15 files (containing multiple rules)

---

## Executive Summary

This analysis identifies **26 automation items** requiring migration or deactivation:
- **11 Process Builders** (4 Active, 7 Draft/Inactive)
- **15 Workflow Rule files** containing approximately 50+ individual rules

**Critical Finding:** Multiple objects already have Apex triggers deployed (Case, Task, WorkOrder, Contact, EmailMessage, etc.). This significantly impacts migration strategy recommendations.

**Recommended Migration Priority:**
1. **HIGH**: Active Process Builders & Workflow Rules on objects with existing triggers
2. **MEDIUM**: Active automations on objects without triggers
3. **LOW**: Draft/Inactive Process Builders

---

## PROCESS BUILDERS ANALYSIS

### 1. CASE OBJECT

#### Case_Update_Process.flow-meta.xml
- **Status:** DRAFT (Inactive)
- **Object:** Case (Comment__c object reference found in code)
- **Complexity:** COMPLEX
  - 20+ decision nodes
  - Multiple field update actions
  - Complex formulas with ISCHANGED, ISPICKVAL
  - Evaluates Status, Case_Sub_Status__c changes
  - Multiple conditions with nested AND/OR logic
- **What It Does:**
  - Updates case fields based on status and sub-status changes
  - Monitors Case_Sub_Status__c transitions (Pending Service Integration, Request Not Approved, Pending Manual Dispatch, etc.)
  - Handles Work Order status synchronization
  - Manages various case lifecycle transitions
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** CaseTrigger already exists; consolidate logic into existing trigger framework for better performance and maintainability
- **Dependencies:**
  - Work_Order__c relationship
  - Vendor_Service_Status__c field
  - Case_Sub_Status__c picklist values
- **Risks:**
  - Draft status means it may be incomplete or abandoned
  - Complex nested conditions may have undocumented business logic
  - Need to verify if logic overlaps with existing CaseTrigger
- **Effort Estimate:** LARGE (20-30 hours)
  - Deactivate/archive since Draft
  - If needed, migrate 20+ criteria nodes to Apex
  - Extensive testing required for all status transitions

---

### 2. ACCOUNT OBJECT

#### Create_SLA_upon_activating_Account.flow-meta.xml
- **Status:** ACTIVE
- **Object:** Account
- **Complexity:** MEDIUM
  - 3 decision nodes
  - Multiple record lookups and creates
  - Creates Entitlement records (SLA)
  - Cross-object operations
- **What It Does:**
  - Creates SLA (Entitlement) records when an Account is activated
  - Performs lookup operations to check for existing Entitlements
  - Creates multiple Entitlement records based on account status
- **Migration Path:** RECORD-TRIGGERED FLOW (Recommended)
  - **Reason:** Clean migration path; modern Flow can handle record creation efficiently; no existing Account trigger for Entitlement creation
- **Dependencies:**
  - Entitlement object
  - Account Status field
  - Entitlement creation logic
- **Risks:**
  - Need to ensure no duplicate Entitlement creation
  - Verify EntitlementTrigger doesn't conflict
  - Test bulk scenarios (200+ accounts)
- **Effort Estimate:** MEDIUM (8-12 hours)
  - Straightforward conversion to Record-Triggered Flow
  - Test entitlement creation logic
  - Validate bulk operations

---

### 3. VENDOR/LOCATION OBJECT

#### Delete_Vendor_Service_Location_Code.flow-meta.xml
- **Status:** DRAFT (Inactive)
- **Object:** Custom object (Vendor_Service_Location__c or similar)
- **Complexity:** SIMPLE
  - Single decision node
  - Delete record action
  - Simple criteria evaluation
- **What It Does:**
  - Deletes Vendor Service Location Code records based on specific criteria
- **Migration Path:** DEACTIVATE/ARCHIVE
  - **Reason:** Draft status indicates incomplete or abandoned; assess if functionality is still needed before migrating
- **Dependencies:**
  - Vendor Service Location object
- **Risks:**
  - Low risk - already inactive
- **Effort Estimate:** SMALL (1-2 hours)
  - Archive or delete if not needed
  - If needed, simple conversion to Record-Triggered Flow

---

### 4. EMAIL MESSAGE OBJECT

#### Email_to_Case.flow-meta.xml
- **Status:** ACTIVE
- **Object:** EmailMessage
- **Complexity:** COMPLEX
  - 14+ decision nodes
  - Multiple Apex class invocations (EmailMessageHelper, EmailMessageContactMapping)
  - Multiple subflow calls (1:1 match flow, Genesys Routing flow)
  - Monitors To_Be_Processed__c, IndicoStatus__c fields
  - Complex routing logic
- **What It Does:**
  - Processes incoming email messages for Case creation
  - Invokes Apex methods for email processing and contact mapping
  - Calls Genesys Routing flow for case routing
  - Implements 1:1 contact-to-case matching
  - Integrates with Indico email processing
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** EmailMessageTrigger already exists; complex Apex integrations; performance-critical; better suited for trigger framework
- **Dependencies:**
  - EmailMessageHelper Apex class (Invocable)
  - EmailMessageContactMapping Apex class (Invocable)
  - Genesys Routing flow
  - 1:1 match flow
  - Indico integration
- **Risks:**
  - HIGH - Email processing is critical business functionality
  - Complex dependencies on multiple Apex classes and flows
  - Must maintain email-to-case routing accuracy
  - Performance critical - high volume email processing
- **Effort Estimate:** X-LARGE (40-60 hours)
  - Complex integration with existing EmailMessageTrigger
  - Multiple Apex class dependencies to refactor
  - Extensive testing of email routing scenarios
  - Integration testing with Genesys and Indico

---

### 5. CONTACT OBJECT

#### Populate_Preferred_Language_from_Contact_to.flow-meta.xml
- **Status:** ACTIVE
- **Object:** Contact (unclear target - likely Case or related object)
- **Complexity:** SIMPLE
  - 1-2 decision nodes
  - Simple field copy operation
  - Basic criteria evaluation
- **What It Does:**
  - Copies Preferred Language field from Contact to a related object
  - Likely updates Case or Account with Contact's language preference
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** ContactTrigger already exists; simple field update is more efficient in Apex; consolidate with existing trigger logic
- **Dependencies:**
  - Contact.Preferred_Language__c field
  - Target object relationship
- **Risks:**
  - LOW - Simple field update
  - Need to identify exact target object
- **Effort Estimate:** SMALL (2-4 hours)
  - Add to existing ContactTrigger handler
  - Simple field mapping logic
  - Test contact updates

#### Update_Text_Notification_Opt_In.flow-meta.xml
- **Status:** ACTIVE
- **Object:** Contact
- **Complexity:** MEDIUM
  - 3-4 decision nodes
  - Apex integration (ContactTextOptInInvokableAPI)
  - External API call for opt-in/opt-out
  - Multiple field evaluations
- **What It Does:**
  - Manages text notification opt-in/opt-out preferences
  - Calls external API for SMS preference management
  - Updates Contact.Text_Notifications_Opt_In__c
  - Monitors mobile phone changes
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** ContactTrigger already exists; API callout better handled in Apex with proper error handling; can be async
- **Dependencies:**
  - ContactTextOptInInvokableAPI Apex class
  - External SMS opt-in service
  - Contact.MobilePhone field
  - Contact.Text_Notifications_Opt_In__c field
- **Risks:**
  - MEDIUM - External API dependency
  - Must handle API failures gracefully
  - Need proper error logging
  - Consider async processing for API calls
- **Effort Estimate:** MEDIUM (8-12 hours)
  - Integrate with existing ContactTrigger
  - Refactor to use async Apex for API calls
  - Add error handling and retry logic
  - Test API integration

---

### 6. SUPPLIER OBJECT

#### Supplier_Score_Trending.flow-meta.xml
- **Status:** ACTIVE
- **Object:** Custom object (Supplier__c or similar)
- **Complexity:** MEDIUM
  - Multiple calculations
  - Trend analysis logic
  - Field updates based on scoring
- **What It Does:**
  - Calculates and tracks supplier performance scores over time
  - Updates trending indicators
  - Likely performs date-based calculations
- **Migration Path:** RECORD-TRIGGERED FLOW (Recommended)
  - **Reason:** Calculation logic can be cleanly expressed in Flow; no existing trigger on Supplier object
- **Dependencies:**
  - Supplier scoring fields
  - Historical data tracking
- **Risks:**
  - MEDIUM - Need to validate calculation accuracy
  - Verify bulk operation performance
- **Effort Estimate:** MEDIUM (10-14 hours)
  - Convert calculations to Record-Triggered Flow
  - Extensive testing of scoring logic
  - Validate historical trending accuracy

---

### 7. TASK OBJECT

#### Update_Case_for_Task_Process.flow-meta.xml
- **Status:** DRAFT (Inactive)
- **Object:** Task → Case (updates Case from Task)
- **Complexity:** MEDIUM
  - Multiple decision nodes
  - Calls Task_Subject_Description_Mapping flow
  - Updates related Case records
  - Multiple field evaluations
- **What It Does:**
  - Updates Case fields when Task is created/updated
  - Maps Task Subject and Description using subflow
  - Handles Task framework logic for non-pickup tasks
  - Updates Case based on Task completion or changes
- **Migration Path:** APEX TRIGGER (Recommended if activated)
  - **Reason:** TaskTrigger already exists; Draft status suggests deactivation is better option
- **Dependencies:**
  - Task_Subject_Description_Mapping flow
  - Task.Subject field
  - Case relationship
- **Risks:**
  - LOW - Draft status means not in use
  - If activated, could conflict with existing TaskTrigger
- **Effort Estimate:** SMALL (2-4 hours)
  - Archive/deactivate since Draft
  - If needed, integrate with existing TaskTrigger (8-12 hours)

---

### 8. QUOTE OBJECT

#### Update_To_Chatter_From_Quote.flow-meta.xml
- **Status:** ACTIVE
- **Object:** SBQQ__Quote__c (Salesforce CPQ)
- **Complexity:** SIMPLE
  - 1-2 decision nodes
  - Creates Chatter posts
  - Simple notification logic
- **What It Does:**
  - Posts to Chatter when Quote status/fields change
  - Notifies stakeholders of Quote updates
  - Likely creates FeedItem records
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** QuoteTrigger already exists; Chatter posts more efficient in Apex; better error handling
- **Dependencies:**
  - FeedItem object
  - Quote status fields
  - User/Group mentions in Chatter
- **Risks:**
  - LOW - Simple Chatter notification
  - Verify Chatter is enabled in org
- **Effort Estimate:** SMALL (4-6 hours)
  - Add to existing QuoteTrigger
  - Simple Chatter post logic
  - Test notifications

---

### 9. WORK ORDER OBJECT

#### Work_Order_Process.flow-meta.xml
- **Status:** DRAFT (Inactive)
- **Object:** WorkOrder
- **Complexity:** MEDIUM
  - Launches Work_Order_Creation flow
  - Creates task framework records
  - Multiple decision points
  - Field validation logic
- **What It Does:**
  - Orchestrates Work Order creation process
  - Calls Work_Order_Creation flow
  - Creates related tasks via Create_Task_FrameWork_Process
  - Handles declined work order follow-ups
- **Migration Path:** APEX TRIGGER (Recommended if activated)
  - **Reason:** WorkOrderTrigger already exists; Draft status suggests it's superseded by existing trigger
- **Dependencies:**
  - Work_Order_Creation flow
  - Create_Task_FrameWork_Process flow
  - Case relationship
- **Risks:**
  - LOW - Draft status, likely obsolete
  - Verify existing WorkOrderTrigger handles this functionality
- **Effort Estimate:** SMALL (2-4 hours)
  - Archive since Draft
  - Verify existing trigger coverage (4-8 hours if migration needed)

---

### 10. INVOCABLE PROCESS

#### EMailMessageUpdate.flow-meta.xml
- **Status:** ACTIVE
- **Object:** EmailMessage (Invocable Process - called by other automation)
- **Complexity:** SIMPLE
  - Invocable process (not trigger-based)
  - Simple field updates
  - Called by other flows/processes
- **What It Does:**
  - Updates EmailMessage fields when invoked
  - Reusable process called by other automation
  - Performs field updates based on passed parameters
- **Migration Path:** CONVERT TO INVOCABLE ACTION (Apex)
  - **Reason:** Invocable Apex more performant and flexible; easier to maintain
- **Dependencies:**
  - Calling flows/processes (likely Email_to_Case process)
  - EmailMessage fields
- **Risks:**
  - LOW - Simple update logic
  - Must update all calling automation
- **Effort Estimate:** SMALL (4-6 hours)
  - Create Invocable Apex method
  - Update calling automation references
  - Test invocation scenarios

---

## WORKFLOW RULES ANALYSIS

### 1. CASE OBJECT (Case.workflow-meta.xml)

**Total Rules:** 17 rules defined
**Active Rules:** 2
**Inactive Rules:** 15

#### ACTIVE RULES:

##### Send Acorn New Case Information
- **Status:** ACTIVE
- **Complexity:** COMPLEX
- **What It Does:**
  - Sends outbound message to Acorn system when Case status changes
  - Handles multiple record types (New_Service_Case, Modify_Existing_Service_Case, Pickup_Case)
  - Complex formula with 100+ lines evaluating status transitions
  - Integration with legacy Acorn system
- **Actions:**
  - Outbound Message: Case_Payload → https://qa.sf.wmsbs.wm.com/SalesforceOutboundMessage/Services/CaseService.svc
- **Migration Path:** APEX TRIGGER (Required)
  - **Reason:** CaseTrigger exists; complex integration logic; outbound messages should be Platform Events or Apex HTTP callouts
- **Dependencies:**
  - Acorn_Issue_Id__c field
  - Integrate_with_Acorn__c field
  - Multiple Case record types
  - Case_Type__c, Case_Sub_Type__c picklists
- **Risks:**
  - CRITICAL - Integration with external Acorn system
  - Complex formula may have hidden edge cases
  - Outbound message failures need monitoring
  - Consider Platform Events instead of Outbound Messages
- **Effort Estimate:** LARGE (20-30 hours)
  - Migrate outbound message to Apex HTTP callout or Platform Event
  - Extensive integration testing with Acorn
  - Implement proper error handling and retry logic
  - Document all status transition scenarios

##### Set Reference Number
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Sets Case.Reference_Number__c to CaseNumber on creation
  - Only when ParentId is null
- **Actions:**
  - Field Update: Reference_Number__c = CaseNumber
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** CaseTrigger exists; simple field update in before insert
- **Dependencies:**
  - None
- **Risks:**
  - LOW - Simple field copy
- **Effort Estimate:** SMALL (1-2 hours)
  - Add to CaseTrigger handler
  - Before insert context

#### INACTIVE RULES (Draft/Inactive - 15 rules):

The following rules are all inactive and should be evaluated for archival:

1. **Acorn W/O Is Populated** - Updates Acorn WorkOrder Number
2. **Close Case** - Closes cases based on Close_Irrelevant_Case__c flag
3. **Close Pickup Case** - Closes pickup cases
4. **GENESYS Email2Case Workflow Rule** - Email to case routing (likely replaced by Email_to_Case process)
5. **Override_SLA_Option** - SLA date matching
6. **PO Mandatory or Not** - Sets status to Pending if PO required
7. **Recreated Work Order Successful** - Removes recreation flag
8. **SendBaleCaseToAcorn** - Routes Bale cases to queue
9. **Uncheck Ignore Duplicate on change** - Resets duplicate flag
10. **Update BackOffice Checkbox Workflow** - Sets BackOffice flag
11. **Update Service Date with Local Time** - Time zone handling
12. **UpdateCaseSla** - Updates SLA Service Date Time
13. **WorkOrderCreated** - Sets Work Order creation flag
14. **isByPassDuplicateCase** - Handles duplicate bypass logic

**Migration Path:** DEACTIVATE/ARCHIVE
- **Effort Estimate:** SMALL (2-4 hours total)
  - Document inactive rules
  - Verify functionality not needed
  - Delete from metadata

---

### 2. TASK OBJECT (Task.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Update Attempt for Notify Customer Of Service Update task
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Updates Task.Attempt__c from 1 to 2
  - Only for tasks with Process__c = "Notify Customer Of Service Update"
  - Tracks customer notification attempts
- **Actions:**
  - Field Update: Attempt__c = 2
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** TaskTrigger already exists; simple field update
- **Dependencies:**
  - Task.Process__c field
  - Task.Attempt__c field
- **Risks:**
  - LOW - Simple field update
- **Effort Estimate:** SMALL (2-3 hours)
  - Add to TaskTrigger handler
  - Before insert logic

---

### 3. WORK ORDER OBJECT (WorkOrder.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Integrate Work Order with Acorn
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Sends Work Order to Acorn system on creation
  - Only when Acorn_WorkOrder_Id__c is blank
  - Bypassed if user has Bypass_Validation__c = true
- **Actions:**
  - Outbound Message: Send_Work_Order → https://qa.sf.wmsbs.wm.com/SalesforceOutboundMessage/Services/WorkOrderService.svc
- **Migration Path:** APEX TRIGGER (Required)
  - **Reason:** WorkOrderTrigger exists; outbound message should be Platform Event or Apex callout
- **Dependencies:**
  - Acorn_WorkOrder_Id__c field
  - User.Bypass_Validation__c field
  - Acorn integration endpoint
- **Risks:**
  - HIGH - Critical integration with Acorn
  - Outbound message reliability
  - Need proper error handling
- **Effort Estimate:** MEDIUM (12-16 hours)
  - Migrate to Apex HTTP callout or Platform Event
  - Add to WorkOrderTrigger handler
  - Integration testing with Acorn
  - Implement error handling and logging

---

### 4. BUSINESS RULE OBJECT (Business_Rule__c.workflow-meta.xml)

**Total Rules:** 4 rules
**Active Rules:** 4

##### Business Rule Expiration
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Time-based workflow: Deactivates Business Rule 1 day after End_Date__c
  - Only if Active__c = true and End_Date__c >= TODAY()
- **Actions:**
  - Field Update: Active__c = false (time-triggered)
- **Migration Path:** SCHEDULED FLOW or RECORD-TRIGGERED FLOW
  - **Reason:** Time-based automation; Record-Triggered Flow can handle scheduled paths
- **Dependencies:**
  - Business_Rule__c.End_Date__c
  - Business_Rule__c.Active__c
- **Risks:**
  - MEDIUM - Time-based workflows need careful migration
  - Need to handle pending scheduled actions
  - Test scheduled path thoroughly
- **Effort Estimate:** MEDIUM (6-8 hours)
  - Convert to Record-Triggered Flow with scheduled path
  - Test time-based deactivation
  - Migrate pending scheduled actions

##### BusinessRuleWorkFlowChannelReq
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Sets Is_Channel_Requirements__c = true when Channel_Req__c is populated
- **Actions:**
  - Field Update: Is_Channel_Requirements__c = true
- **Migration Path:** RECORD-TRIGGERED FLOW or APEX TRIGGER
  - **Reason:** BusinessRuleTrigger exists; simple field update
- **Dependencies:**
  - Channel_Req__c field
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-3 hours)
  - Add to BusinessRuleTrigger or convert to Flow

##### BusinessRuleWorkFlowSpecailInstructions
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Sets Is_Special_Instructions__c = true when Special_Ins__c is populated
- **Actions:**
  - Field Update: Is_Special_Instructions__c = true
- **Migration Path:** RECORD-TRIGGERED FLOW or APEX TRIGGER
  - **Reason:** BusinessRuleTrigger exists; consolidate with Channel Requirements logic
- **Dependencies:**
  - Special_Ins__c field
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-3 hours)
  - Add to BusinessRuleTrigger or convert to Flow

##### End Date in Past
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Immediately deactivates Business Rule if End_Date__c < TODAY()
- **Actions:**
  - Field Update: Active__c = false
- **Migration Path:** RECORD-TRIGGERED FLOW or APEX TRIGGER
  - **Reason:** Simple validation; can be combined with other Business Rule logic
- **Dependencies:**
  - Business_Rule__c.End_Date__c
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-3 hours)

##### Update_Alias_BusinessRuleName
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Updates Alias__c field with Name value when blank or on clone
- **Actions:**
  - Field Update: Alias__c = Name
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** BusinessRuleTrigger exists; before insert/update logic
- **Dependencies:**
  - None
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-3 hours)

**Combined Migration Recommendation for Business_Rule__c:**
- Consolidate all 4 rules into BusinessRuleTrigger
- Total Effort: SMALL-MEDIUM (8-12 hours)
  - Migrate all field updates to trigger
  - Convert time-based rule to scheduled flow or scheduled Apex
  - Test all scenarios

---

### 5. CONTACT OBJECT (Contact.workflow-meta.xml)

**Total Rules:** 2 rules
**Active Rules:** 0 (both inactive)

##### Contact status updated (INACTIVE)
- **Status:** INACTIVE
- **What It Does:**
  - Updates Contact_Status__c to "Active" for System Admins when Corporate_Contact_Status__c = "Approved"
- **Migration Path:** DEACTIVATE/ARCHIVE
- **Effort Estimate:** SMALL (1 hour)

##### Text notification opt-out on number change (INACTIVE)
- **Status:** INACTIVE
- **What It Does:**
  - Opts out text notifications when MobilePhone changes
  - NOTE: This functionality appears to be handled by Update_Text_Notification_Opt_In Process Builder
- **Migration Path:** DEACTIVATE/ARCHIVE
- **Effort Estimate:** SMALL (1 hour)
  - Already replaced by Process Builder

---

### 6. QUOTE OBJECT (SBQQ__Quote__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Send Quote to API Hub
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Sends Quote to Acorn/API Hub when status changes to "Approved"
  - Also triggers on manual resync (DoResyncOutBoundcall__c flag)
  - Updates DoResyncOutBoundcall__c to false
- **Actions:**
  - Outbound Message: Send_Quote_to_Acorn → https://qa.sf.wmsbs.wm.com/SalesforceOutboundmessage/Services/CreateNewAssetService.svc
  - Field Update: DoResyncOutBoundcall__c = false
- **Migration Path:** APEX TRIGGER (Required)
  - **Reason:** QuoteTrigger exists; outbound message should be Platform Event or Apex callout
- **Dependencies:**
  - SBQQ__Status__c field
  - Acorn_integration_required__c flag
  - Resubmit_Flag__c field
  - Acorn API endpoint
- **Risks:**
  - HIGH - Critical CPQ to Acorn integration
  - Affects order fulfillment process
  - Need robust error handling
- **Effort Estimate:** LARGE (16-20 hours)
  - Migrate to Apex HTTP callout or Platform Event
  - Add to QuoteTrigger handler
  - Extensive integration testing
  - Implement retry logic and monitoring

---

### 7. GENESYS ROUTING OBJECT (Genesys_Routing__c.workflow-meta.xml)

**Total Rules:** 2 rules
**Active Rules:** 2

##### Email to Case Genesys Routing
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Routes email-to-case records to Genesys system
  - Complex boolean filter for record type and media type
- **Actions:**
  - Outbound Message: Genesys_Routing_Payload (20+ fields)
- **Migration Path:** APEX TRIGGER or PLATFORM EVENT
  - **Reason:** Complex integration; outbound messages should be modernized
- **Dependencies:**
  - Genesys integration endpoint
  - 20+ routing fields
  - Record types (Email to Case)
- **Risks:**
  - HIGH - Critical routing functionality
  - Integration with Genesys CTI
- **Effort Estimate:** LARGE (16-24 hours)
  - Migrate to Platform Event or Apex callout
  - Extensive integration testing
  - Implement monitoring

##### Task Genesys Routing Payload
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Routes Task records to Genesys for agent assignment
- **Actions:**
  - Outbound Message: Task_Payload (25+ fields)
- **Migration Path:** APEX TRIGGER or PLATFORM EVENT
  - **Reason:** Complex integration; consolidate with email routing
- **Dependencies:**
  - Genesys integration endpoint
  - Task routing fields
- **Risks:**
  - HIGH - Critical routing functionality
- **Effort Estimate:** LARGE (16-24 hours)

**Combined Recommendation:**
- Consolidate both rules into unified Platform Event architecture
- Total Effort: X-LARGE (30-40 hours)

---

### 8. COMMENT OBJECT (Comment__c.workflow-meta.xml)

**Total Rules:** 2 rules
**Active Rules:** 2

##### Populate Acorn_SUser_ID__c
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Populates Acorn_SUser_ID__c from User when null
- **Actions:**
  - Field Update: Acorn_SUser_ID__c = $User.Acorn_SUser_ID__c
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** CommentTrigger exists; simple field default
- **Dependencies:**
  - User.Acorn_SUser_ID__c
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-3 hours)

##### Task Values to Acorn Invocation Rule
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Sends completed task comments to Acorn system
  - Triggers on create or when Acorn_Tracking_Number__c changes
- **Actions:**
  - Outbound Message: Task_Values_to_Acorn
- **Migration Path:** APEX TRIGGER (Required)
  - **Reason:** CommentTrigger exists; outbound message modernization needed
- **Dependencies:**
  - Acorn_Tracking_Number__c field
  - Acorn integration endpoint
- **Risks:**
  - MEDIUM - Integration with Acorn
- **Effort Estimate:** MEDIUM (10-12 hours)

---

### 9. QUOTE LINE OBJECT (SBQQ__QuoteLine__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 0

##### Update Exception Details (INACTIVE)
- **Status:** INACTIVE
- **What It Does:**
  - Updates exception fields from Quote to Quote Line
- **Migration Path:** DEACTIVATE/ARCHIVE
- **Effort Estimate:** SMALL (1 hour)

---

### 10. GENESYS REPORTING OBJECT (Genesys_Reporting__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Send to Genesys Reporting
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Sends reporting data to Genesys on record creation
- **Actions:**
  - Outbound Message: Genesys_Reporting_outbound
- **Migration Path:** PLATFORM EVENT (Recommended)
  - **Reason:** Reporting data; async processing; no trigger exists
- **Dependencies:**
  - Genesys reporting endpoint
- **Risks:**
  - MEDIUM - Reporting integration
- **Effort Estimate:** MEDIUM (8-12 hours)

---

### 11. NOTIFICATION CONTACT OBJECT (Notification_Contact__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Adding contact mobile phone
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Formats mobile phone number with +1 prefix from Contact
- **Actions:**
  - Field Update: ISD_Phone__c = "+1" & Contact_Name__r.MobilePhone
- **Migration Path:** RECORD-TRIGGERED FLOW (Recommended)
  - **Reason:** Simple field formula; no trigger exists
- **Dependencies:**
  - Contact.MobilePhone
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (2-4 hours)

---

### 12. ENTITLEMENT OBJECT (Entitlement.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Update Entitlement Name
- **Status:** ACTIVE
- **Complexity:** MEDIUM
- **What It Does:**
  - Auto-generates Entitlement Name using complex formula
  - Based on Account, Service, Service Guarantee Category, etc.
- **Actions:**
  - Field Update: Name = Complex formula
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** EntitlementTrigger exists; complex formula better in Apex for maintainability
- **Dependencies:**
  - Account.AccountNumber
  - Service__c, Service_Guarantee_Category__c fields
- **Risks:**
  - MEDIUM - Complex naming formula
  - Verify existing trigger doesn't conflict
- **Effort Estimate:** MEDIUM (6-8 hours)

---

### 13. ACCOUNT TITLE OBJECT (Account_Title__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Avoid duplicate account title
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Creates unique identifier combining Name and Account ID
- **Actions:**
  - Field Update: Duplicate_Title__c = Name + Account__r.Id
- **Migration Path:** APEX TRIGGER (Recommended)
  - **Reason:** AccountTitleTrigger exists; simple field formula
- **Dependencies:**
  - Account__c relationship
- **Risks:**
  - LOW
- **Effort Estimate:** SMALL (3-4 hours)

---

### 14. CASE COMMENT OBJECT (CaseComment.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 1

##### Update CaseComment Createddate on Case
- **Status:** ACTIVE
- **Complexity:** SIMPLE
- **What It Does:**
  - Copies CaseComment CreatedDate to Case.CaseComment_CreateDate__c
  - Cross-object update to parent Case
- **Actions:**
  - Field Update: Case.CaseComment_CreateDate__c = CreatedDate (cross-object)
- **Migration Path:** APEX TRIGGER (Required)
  - **Reason:** CaseCommentTrigger exists; cross-object field updates not supported in Flow; needs Apex
- **Dependencies:**
  - Case.CaseComment_CreateDate__c field
- **Risks:**
  - LOW - Simple timestamp copy
- **Effort Estimate:** SMALL (3-4 hours)
  - Add to CaseCommentTrigger handler
  - Update parent Case

---

### 15. EMAIL MESSAGE OBJECT (SFDCEmailMessage__c.workflow-meta.xml)

**Total Rules:** 1 rule
**Active Rules:** 0

##### Send to Indico (INACTIVE)
- **Status:** INACTIVE
- **What It Does:**
  - Sends email messages to Indico ML system for processing
- **Actions:**
  - Outbound Message: Send_Indico_Email_Message
- **Migration Path:** DEACTIVATE/ARCHIVE
  - **Reason:** Inactive; likely replaced by Email_to_Case Process Builder
- **Effort Estimate:** SMALL (1 hour)

---

## MIGRATION STRATEGY & ROADMAP

### Phase 1: High Priority - Active Integrations (Weeks 1-6)

**Critical Path Items - Must migrate first:**

1. **Case Acorn Integration** (LARGE - 20-30 hrs)
   - Case.workflow: "Send Acorn New Case Information"
   - Migrate to CaseTrigger with Apex HTTP callout or Platform Event

2. **WorkOrder Acorn Integration** (MEDIUM - 12-16 hrs)
   - WorkOrder.workflow: "Integrate Work Order with Acorn"
   - Migrate to WorkOrderTrigger with Apex callout

3. **Quote Acorn Integration** (LARGE - 16-20 hrs)
   - SBQQ__Quote__c.workflow: "Send Quote to API Hub"
   - Migrate to QuoteTrigger with Apex callout

4. **Email to Case Processing** (X-LARGE - 40-60 hrs)
   - Email_to_Case Process Builder
   - Migrate to EmailMessageTrigger with refactored Apex

5. **Genesys Routing** (X-LARGE - 30-40 hrs)
   - Genesys_Routing__c.workflow: Both email and task routing
   - Migrate to Platform Event architecture

**Phase 1 Total Effort:** 118-166 hours (15-21 business days)

---

### Phase 2: Medium Priority - Active Field Updates & Logic (Weeks 7-10)

1. **Contact Text Notification** (MEDIUM - 8-12 hrs)
   - Update_Text_Notification_Opt_In Process Builder
   - Migrate to ContactTrigger with async API callout

2. **Contact Preferred Language** (SMALL - 2-4 hrs)
   - Populate_Preferred_Language_from_Contact_to Process Builder
   - Add to ContactTrigger

3. **Business Rule Automation** (SMALL-MEDIUM - 8-12 hrs)
   - Business_Rule__c.workflow: All 4 active rules
   - Consolidate into BusinessRuleTrigger + scheduled flow

4. **Account SLA Creation** (MEDIUM - 8-12 hrs)
   - Create_SLA_upon_activating_Account Process Builder
   - Convert to Record-Triggered Flow

5. **Supplier Score Trending** (MEDIUM - 10-14 hrs)
   - Supplier_Score_Trending Process Builder
   - Convert to Record-Triggered Flow

6. **Quote Chatter Notification** (SMALL - 4-6 hrs)
   - Update_To_Chatter_From_Quote Process Builder
   - Add to QuoteTrigger

7. **Task Attempt Update** (SMALL - 2-3 hrs)
   - Task.workflow: "Update Attempt..."
   - Add to TaskTrigger

8. **Comment Acorn Integration** (MEDIUM - 10-12 hrs)
   - Comment__c.workflow: Both rules
   - Add to CommentTrigger

9. **Entitlement Naming** (MEDIUM - 6-8 hrs)
   - Entitlement.workflow: "Update Entitlement Name"
   - Add to EntitlementTrigger

10. **Account Title Deduplication** (SMALL - 3-4 hrs)
    - Account_Title__c.workflow: "Avoid duplicate account title"
    - Add to AccountTitleTrigger

11. **CaseComment Timestamp** (SMALL - 3-4 hrs)
    - CaseComment.workflow: "Update CaseComment Createddate on Case"
    - Add to CaseCommentTrigger

12. **Notification Contact Phone Formatting** (SMALL - 2-4 hrs)
    - Notification_Contact__c.workflow: "Adding contact mobile phone"
    - Convert to Record-Triggered Flow

13. **Genesys Reporting** (MEDIUM - 8-12 hrs)
    - Genesys_Reporting__c.workflow: "Send to Genesys Reporting"
    - Convert to Platform Event

14. **EmailMessageUpdate Invocable** (SMALL - 4-6 hrs)
    - EMailMessageUpdate Process Builder
    - Convert to Invocable Apex

**Phase 2 Total Effort:** 78-113 hours (10-15 business days)

---

### Phase 3: Low Priority - Cleanup & Archive (Week 11)

**Inactive/Draft Process Builders to Archive:**
1. Case_Update_Process (DRAFT)
2. Delete_Vendor_Service_Location_Code (DRAFT)
3. Update_Case_for_Task_Process (DRAFT)
4. Work_Order_Process (DRAFT)

**Inactive Workflow Rules to Archive:**
1. Case.workflow: 15 inactive rules
2. Contact.workflow: 2 inactive rules
3. SBQQ__QuoteLine__c.workflow: 1 inactive rule
4. SFDCEmailMessage__c.workflow: 1 inactive rule

**Phase 3 Total Effort:** 10-15 hours (2 business days)

---

## TOTAL MIGRATION EFFORT ESTIMATE

| Phase | Description | Effort Range | Timeline |
|-------|-------------|--------------|----------|
| Phase 1 | Critical Integrations | 118-166 hours | 15-21 days |
| Phase 2 | Field Updates & Logic | 78-113 hours | 10-15 days |
| Phase 3 | Cleanup & Archive | 10-15 hours | 2 days |
| **TOTAL** | **Complete Migration** | **206-294 hours** | **27-38 days** |

**Recommended Team Size:** 2-3 developers + 1 QA engineer

**Realistic Timeline:** 3-4 months (including testing, deployment, monitoring)

---

## RISK ASSESSMENT SUMMARY

### CRITICAL RISKS (Immediate Attention Required)

1. **Acorn Integration Dependencies** (Case, WorkOrder, Quote, Comment)
   - Multiple outbound messages to same system
   - Need coordinated migration strategy
   - Consider API Hub modernization
   - **Mitigation:** Migrate to Platform Events with proper error handling and monitoring

2. **Email-to-Case Processing** (Email_to_Case Process Builder)
   - Complex, high-volume automation
   - Multiple Apex class dependencies
   - Genesys integration
   - **Mitigation:** Extensive testing in sandbox; phased rollout; rollback plan

3. **Genesys CTI Integration** (Routing & Reporting)
   - Critical for call center operations
   - Real-time routing requirements
   - **Mitigation:** Work closely with Genesys team; parallel run testing

### HIGH RISKS

1. **Existing Trigger Framework**
   - Multiple objects already have triggers
   - Need to understand trigger handler patterns
   - Order of execution changes possible
   - **Mitigation:** Code review of all existing triggers; document order of execution

2. **Bulk Operations**
   - Process Builders handle bulk differently than Apex
   - Data loads may behave differently
   - **Mitigation:** Bulk testing with 200+ records; governor limit testing

3. **Time-Based Workflows**
   - Business Rule expiration has pending scheduled actions
   - Need to migrate pending actions
   - **Mitigation:** Export pending time-based workflow queue before migration

### MEDIUM RISKS

1. **CPQ Dependencies** (Quote, QuoteLine workflows)
   - Salesforce CPQ has specific requirements
   - Quote lifecycle must be maintained
   - **Mitigation:** Involve CPQ expert; test quote-to-order process

2. **User Change Management**
   - Users may rely on email notifications from workflows
   - Process timing may change
   - **Mitigation:** Communication plan; training; documentation

---

## TESTING STRATEGY

### Unit Testing (Per Migration)
- Apex test classes with 75%+ coverage (aim for 90%+)
- All decision branches covered
- Bulk testing (200+ records)
- Negative test cases

### Integration Testing
- End-to-end scenarios for:
  - Case creation → Acorn integration → Work Order creation
  - Email-to-Case → Genesys routing → Agent assignment
  - Quote approval → Acorn integration → Asset creation
- External system connectivity
- Error handling and retry logic

### User Acceptance Testing
- Business process validation
- Performance testing (compare before/after)
- User workflow verification

### Regression Testing
- Full regression suite after each phase
- Verify existing functionality not broken
- Monitor debug logs for unexpected errors

---

## SUCCESS CRITERIA

1. **All active automations migrated** with equivalent or better functionality
2. **Zero business disruption** during migration
3. **Improved performance** (measured by execution time)
4. **Reduced governor limit consumption** (especially SOQL queries)
5. **Better error handling and monitoring** for integrations
6. **Complete documentation** of new automation architecture
7. **All test cases passing** (100% pass rate)

---

## RECOMMENDATIONS

### Immediate Actions (This Week)
1. **Freeze all Process Builder and Workflow Rule changes**
   - Prevent moving target during migration
   - Communicate to all developers

2. **Set up monitoring for existing automations**
   - Capture baseline metrics (execution time, failure rate)
   - Monitor outbound message queues

3. **Review existing Apex trigger framework**
   - Understand handler patterns
   - Identify gaps in error handling
   - Plan trigger architecture updates if needed

### Strategic Recommendations

1. **Platform Events Instead of Outbound Messages**
   - All Acorn integrations should use Platform Events
   - Better error handling, monitoring, and retry logic
   - Decouples Salesforce from external system availability

2. **Trigger Handler Framework**
   - If not already in place, implement standard trigger handler pattern
   - Ensures consistent code structure
   - Easier to maintain and test

3. **Async Processing Where Possible**
   - External API calls should be @future or Queueable
   - Improves user experience
   - Better error handling

4. **Comprehensive Logging**
   - Implement custom logging for all integrations
   - Track errors, retries, and successes
   - Enable proactive monitoring

5. **Consider Flow Builder First**
   - For simple field updates without existing triggers
   - Easier for admins to maintain
   - Reserve Apex for complex logic

---

## APPENDIX: OBJECT TRIGGER INVENTORY

**Existing Apex Triggers:**
- CaseTrigger ✓
- TaskTrigger ✓
- WorkOrderTrigger ✓
- WorkOrderLineItemTrigger ✓
- QuoteTrigger (SBQQ__Quote__c) ✓
- QuoteLineTrigger (SBQQ__QuoteLine__c) ✓
- ContactTrigger ✓
- EmailMessageTrigger ✓
- BusinessRuleTrigger (Business_Rule__c) ✓
- CommentTrigger (Comment__c) ✓
- EntitlementTrigger ✓
- AccountTitleTrigger (Account_Title__c) ✓
- CaseCommentTrigger ✓

**Objects Without Triggers:**
- Account (SLA creation)
- Supplier (or similar custom object)
- Notification_Contact__c
- Genesys_Routing__c
- Genesys_Reporting__c
- SFDCEmailMessage__c

---

## NEXT STEPS

1. **Review this analysis** with technical leadership and business stakeholders
2. **Prioritize migration** based on business criticality and risk
3. **Set up development environment** (dedicated sandbox for migration)
4. **Kick off Phase 1** with Acorn integration migration
5. **Schedule weekly status meetings** to track progress
6. **Create rollback plan** for each migration phase

---

**Document Version:** 1.0
**Last Updated:** January 15, 2026
**Prepared By:** Claude Code Analysis Tool
**Review Status:** DRAFT - Pending Review

---

## QUICK REFERENCE: MIGRATION PATH DECISIONS

| Object | Automation Type | Status | Migration Path | Reason |
|--------|----------------|--------|----------------|---------|
| Case | Process Builder (Case_Update_Process) | DRAFT | Archive | Inactive/abandoned |
| Case | Workflow Rule (Send Acorn New Case Info) | ACTIVE | Apex Trigger | Existing trigger + integration |
| Case | Workflow Rule (Set Reference Number) | ACTIVE | Apex Trigger | Existing trigger + simple logic |
| Account | Process Builder (Create_SLA) | ACTIVE | Record-Triggered Flow | Clean logic, no trigger |
| Vendor Service Location | Process Builder (Delete_Vendor) | DRAFT | Archive | Inactive |
| EmailMessage | Process Builder (Email_to_Case) | ACTIVE | Apex Trigger | Existing trigger + complex logic |
| EmailMessage | Process Builder (EMailMessageUpdate) | ACTIVE | Invocable Apex | Better performance |
| Contact | Process Builder (Populate_Preferred_Language) | ACTIVE | Apex Trigger | Existing trigger |
| Contact | Process Builder (Update_Text_Notification) | ACTIVE | Apex Trigger | Existing trigger + API calls |
| Contact | Workflow Rule (2 rules) | INACTIVE | Archive | Not in use |
| Supplier | Process Builder (Supplier_Score_Trending) | ACTIVE | Record-Triggered Flow | Clean logic, no trigger |
| Task | Process Builder (Update_Case_for_Task) | DRAFT | Archive | Inactive |
| Task | Workflow Rule (Update Attempt) | ACTIVE | Apex Trigger | Existing trigger |
| Quote | Process Builder (Update_To_Chatter) | ACTIVE | Apex Trigger | Existing trigger |
| Quote | Workflow Rule (Send Quote to API Hub) | ACTIVE | Apex Trigger | Existing trigger + integration |
| WorkOrder | Process Builder (Work_Order_Process) | DRAFT | Archive | Inactive |
| WorkOrder | Workflow Rule (Integrate with Acorn) | ACTIVE | Apex Trigger | Existing trigger + integration |
| Business_Rule__c | Workflow Rules (4 active) | ACTIVE | Apex Trigger + Scheduled Flow | Existing trigger |
| Comment__c | Workflow Rules (2 active) | ACTIVE | Apex Trigger | Existing trigger + integration |
| SBQQ__QuoteLine__c | Workflow Rule | INACTIVE | Archive | Not in use |
| Genesys_Routing__c | Workflow Rules (2 active) | ACTIVE | Platform Event | Integration modernization |
| Genesys_Reporting__c | Workflow Rule | ACTIVE | Platform Event | Reporting integration |
| Notification_Contact__c | Workflow Rule | ACTIVE | Record-Triggered Flow | Simple logic, no trigger |
| Entitlement | Workflow Rule | ACTIVE | Apex Trigger | Existing trigger |
| Account_Title__c | Workflow Rule | ACTIVE | Apex Trigger | Existing trigger |
| CaseComment | Workflow Rule | ACTIVE | Apex Trigger | Existing trigger + cross-object |
| SFDCEmailMessage__c | Workflow Rule | INACTIVE | Archive | Replaced by process builder |

