# QUALITY ASSURANCE TESTING CHECKLIST
## Workflow Rules and Process Builder Modernization

**Project Name:** Process Builder and Workflow Rule Modernization Initiative
**Project Code:** PBWR-2026
**Document Type:** QA Testing Checklist
**Prepared by:** George Martin, Salesforce Technical Architect
**Document Version:** 1.0
**Date:** January 15, 2026
**Status:** READY FOR USE

---

## DOCUMENT PURPOSE

This comprehensive QA Testing Checklist provides Quality Assurance engineers with detailed test scenarios, expected results, and validation criteria for the Process Builder and Workflow Rule modernization project. All tests must pass before deployment to production.

---

## TABLE OF CONTENTS

1. [Testing Overview](#1-testing-overview)
2. [Test Environment Setup](#2-test-environment-setup)
3. [Unit Testing Checklist](#3-unit-testing-checklist)
4. [Integration Testing Checklist](#4-integration-testing-checklist)
5. [Functional Testing Checklist](#5-functional-testing-checklist)
6. [Performance Testing Checklist](#6-performance-testing-checklist)
7. [Security Testing Checklist](#7-security-testing-checklist)
8. [Regression Testing Checklist](#8-regression-testing-checklist)
9. [Bulk Processing Testing](#9-bulk-processing-testing)
10. [Error Handling Testing](#10-error-handling-testing)
11. [Monitoring and Logging Testing](#11-monitoring-and-logging-testing)
12. [Pre-Production Validation](#12-pre-production-validation)
13. [Production Smoke Testing](#13-production-smoke-testing)
14. [Sign-Off](#14-sign-off)

---

## 1. TESTING OVERVIEW

### 1.1 Testing Scope

**In Scope:**
- All migrated Process Builders (4 active)
- All migrated Workflow Rules (~22 active)
- All new Platform Events (7)
- All new/modified Apex Triggers (13+)
- All new Record-Triggered Flows (5+)
- All integration handlers (6+)
- Error logging and monitoring
- Performance validation

**Out of Scope:**
- Business logic changes (maintaining existing behavior only)
- UI/UX changes
- Report/dashboard functionality (except integration monitoring)
- Inactive/archived automation

### 1.2 Test Levels

| Test Level | Responsibility | Completion Criteria |
|-----------|---------------|---------------------|
| **Unit Testing** | Developers | 90%+ code coverage, all tests pass |
| **Integration Testing** | QA Team | All external system integrations validated |
| **Functional Testing** | QA Team | All business processes function identically |
| **Performance Testing** | QA Team | Performance targets met or exceeded |
| **Security Testing** | QA Team + Security Review | No security vulnerabilities |
| **Regression Testing** | QA Team | No existing functionality broken |
| **UAT** | Business Users | Business sign-off obtained |

### 1.3 Test Data Requirements

**Production Data Copy:**
The QA environment contains a full copy of Production data, providing realistic test scenarios with actual business records. This approach ensures:
- Testing against real-world data patterns and volumes
- Validation of data migration and integration accuracy
- Identification of edge cases present in production

**Important Considerations:**
- Production data may contain PII/sensitive information - follow data handling policies
- Data is a point-in-time snapshot - recent production changes may not be reflected
- Select appropriate production records for testing (various record types, statuses, configurations)
- Avoid modifying critical production data copies unless necessary for testing

**Test Users:**
- Standard User profile
- System Administrator profile
- Custom profiles (if applicable)
- Users with Bypass_Validation__c flag

**External System Access:**
- QA environment access to Acorn
- QA environment access to Genesys
- Test credentials for all integrations

### 1.4 Entry Criteria

Before testing begins:
- [ ] All code deployed to sandbox
- [ ] All Apex tests passing (90%+ coverage)
- [ ] Production data copy refreshed and validated (within last 7 days)
- [ ] External systems (Acorn, Genesys) available in QA
- [ ] Monitoring dashboards configured
- [ ] QA team trained on new automation
- [ ] Test environment stable

### 1.5 Exit Criteria

Before production deployment:
- [ ] All critical and high priority test cases passed
- [ ] Zero P1 (Critical) defects open
- [ ] All P2 (High) defects resolved or accepted by PM
- [ ] Performance targets met
- [ ] Security review completed
- [ ] UAT sign-off obtained
- [ ] Regression testing completed
- [ ] Rollback procedures tested

---

## 2. TEST ENVIRONMENT SETUP

### 2.1 Sandbox Configuration Checklist

**Sandbox Preparation:**
- [ ] Full sandbox refreshed from production within last 7 days
- [ ] All new code deployed successfully
- [ ] Old Process Builders deactivated
- [ ] Old Workflow Rules deactivated
- [ ] New Flows activated
- [ ] Platform Events visible and configured
- [ ] Named Credentials configured and tested
- [ ] Integration_Error_Log__c object accessible
- [ ] Monitoring dashboards deployed

**External System Configuration:**
- [ ] Acorn QA endpoint configured in Named Credential
- [ ] Acorn QA credentials validated
- [ ] Genesys QA endpoint configured in Named Credential
- [ ] Genesys QA credentials validated
- [ ] Test transactions successful to all external systems

**Production Data Validation:**
```sql
-- Run these SOQL queries to validate production data copy
SELECT COUNT() FROM Account WHERE IsDeleted = false
SELECT COUNT() FROM Contact WHERE IsDeleted = false
SELECT COUNT() FROM Case WHERE CreatedDate = LAST_N_DAYS:30
SELECT COUNT() FROM WorkOrder WHERE CreatedDate = LAST_N_DAYS:30
SELECT COUNT() FROM Quote WHERE CreatedDate = LAST_N_DAYS:30
SELECT COUNT() FROM Business_Rule__c WHERE IsActive__c = true
```

Expected Results:
- [ ] Production data successfully copied (record counts match expectations)
- [ ] Recent records visible (created within last 30 days prior to refresh)
- [ ] Active business records available for testing
- [ ] Data refresh date documented and communicated to QA team

**Identifying Test Records:**
Use existing production records with the following criteria:
- Select Accounts/Contacts from various business units and regions
- Choose records with different record types and statuses
- Identify records that represent common business scenarios
- Tag test transactions with "QA Test - [Date]" in Subject/Description fields for tracking

### 2.2 Test User Setup

**Test User 1: Standard User**
- Username: qatester1@company.com.sandbox
- Profile: Standard User
- Permissions: Standard Case, Work Order, Contact access
- Bypass_Validation__c: false

**Test User 2: Admin User**
- Username: qatester2@company.com.sandbox
- Profile: System Administrator
- Bypass_Validation__c: false

**Test User 3: Integration Bypass User**
- Username: qabypass@company.com.sandbox
- Profile: Integration User
- Bypass_Validation__c: true (to test bypass logic)

### 2.3 Monitoring Setup

**Dashboards:**
- [ ] Integration_Health_Monitor dashboard accessible
- [ ] Dashboard components displaying data
- [ ] Real-time refresh configured (if available)

**Debug Logs:**
- [ ] Debug logs enabled for test users
- [ ] Log level set to FINEST for Apex classes
- [ ] Log filters configured for key classes:
  - CaseTriggerHandler
  - AcornCaseIntegrationHandler
  - EmailMessageTriggerHandler
  - GenesysRoutingHandler

---

## 3. UNIT TESTING CHECKLIST

### 3.1 Apex Test Coverage Validation

**Run All Tests:**
```bash
sfdx force:apex:test:run --testlevel RunLocalTests --codecoverage --resultformat human
```

**Coverage Requirements:**
- [ ] Overall org coverage ≥ 90%
- [ ] Each new/modified class ≥ 90% coverage
- [ ] All test methods passing (0 failures)
- [ ] No test methods skipped

**Critical Classes to Verify:**

| Class Name | Expected Coverage | Result | Notes |
|-----------|------------------|--------|-------|
| CaseService | ≥ 90% | [ ] Pass / [ ] Fail | |
| CaseTriggerHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| AcornCaseIntegrationHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| EmailMessageTriggerHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| GenesysRoutingHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| WorkOrderService | ≥ 90% | [ ] Pass / [ ] Fail | |
| AcornWorkOrderHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| QuoteService | ≥ 90% | [ ] Pass / [ ] Fail | |
| AcornQuoteHandler | ≥ 90% | [ ] Pass / [ ] Fail | |
| ContactService | ≥ 90% | [ ] Pass / [ ] Fail | |
| BusinessRuleService | ≥ 90% | [ ] Pass / [ ] Fail | |
| CommentService | ≥ 90% | [ ] Pass / [ ] Fail | |
| Logger | ≥ 90% | [ ] Pass / [ ] Fail | |

### 3.2 Test Method Validation

**For Each Test Class:**
- [ ] Positive test cases exist (happy path)
- [ ] Negative test cases exist (error conditions)
- [ ] Bulk test cases exist (200 records)
- [ ] Edge cases tested (null values, boundaries)
- [ ] All assertions are meaningful (not just System.assert(true))

**Example Validation:**
```apex
// CaseService_Test should have:
@isTest static void testSetReferenceNumber_NewCase() // Positive
@isTest static void testSetReferenceNumber_WithParent() // Negative
@isTest static void testSetReferenceNumber_Bulk() // Bulk
@isTest static void testSetReferenceNumber_NullCaseNumber() // Edge case
```

---

## 4. INTEGRATION TESTING CHECKLIST

### 4.1 Acorn Case Integration Testing

**Test Case 4.1.1: New Case Creation - Acorn Sync**

**Preconditions:**
- User logged in with standard profile
- Test Account exists
- Acorn QA environment is up

**Test Steps:**
1. Navigate to Cases tab
2. Click "New Case"
3. Fill in required fields:
   - Account: [Test Account]
   - Subject: "QA Test - New Service Case"
   - Status: "New"
   - Record Type: "New_Service_Case"
   - Integrate_with_Acorn__c: Checked
4. Save Case

**Expected Results:**
- [ ] Case created successfully
- [ ] Case.Reference_Number__c = Case.CaseNumber
- [ ] Platform Event published (check Integration_Error_Log__c within 30 seconds)
- [ ] Acorn receives Case data (verify in Acorn QA)
- [ ] Case.Acorn_Issue_Id__c populated with Acorn ID
- [ ] Case.Last_Acorn_Sync__c = current timestamp
- [ ] Integration_Error_Log__c record shows Status = "Success"

**Actual Results:**
- [ ] Pass / [ ] Fail

**Defect ID (if failed):** _____________

---

**Test Case 4.1.2: Case Status Change - Acorn Update**

**Preconditions:**
- Case from Test 4.1.1 exists with Acorn_Issue_Id__c populated

**Test Steps:**
1. Open existing Case
2. Change Status from "New" to "In Progress"
3. Save Case

**Expected Results:**
- [ ] Case saved successfully
- [ ] Platform Event published for status change
- [ ] Acorn receives updated Case data
- [ ] Integration_Error_Log__c shows Status = "Success"
- [ ] Case.Last_Acorn_Sync__c updated

**Actual Results:**
- [ ] Pass / [ ] Fail

**Defect ID (if failed):** _____________

---

**Test Case 4.1.3: Case Without Acorn Integration Flag**

**Preconditions:**
- User logged in

**Test Steps:**
1. Create new Case
2. Set Integrate_with_Acorn__c = false
3. Save Case

**Expected Results:**
- [ ] Case created successfully
- [ ] NO Platform Event published
- [ ] NO entry in Integration_Error_Log__c for this Case
- [ ] Case.Acorn_Issue_Id__c remains blank

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.1.4: Acorn Integration with Invalid Record Type**

**Preconditions:**
- User logged in

**Test Steps:**
1. Create new Case
2. Set Record Type = "Support_Case" (not in valid list)
3. Set Integrate_with_Acorn__c = true
4. Save Case

**Expected Results:**
- [ ] Case created successfully
- [ ] NO Platform Event published (doesn't meet criteria)
- [ ] NO integration attempt
- [ ] No errors displayed to user

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.1.5: Acorn Integration Failure - Retry Logic**

**Preconditions:**
- Acorn QA environment is down or configured to return 500 error

**Test Steps:**
1. Create new Case with Acorn integration enabled
2. Save Case
3. Wait 30 seconds
4. Check Integration_Error_Log__c

**Expected Results:**
- [ ] Case created successfully
- [ ] Platform Event published
- [ ] Integration attempt fails (Acorn down)
- [ ] Integration_Error_Log__c shows Status = "Retry"
- [ ] Retry_Count__c = 1 (then 2, then 3)
- [ ] After 3 retries, Status = "Failed"
- [ ] Email notification sent to integrations@company.com
- [ ] Case.Acorn_Issue_Id__c remains blank

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.1.6: Bulk Case Creation (200 Records)**

**Preconditions:**
- Data Loader or API access available
- Acorn QA environment up

**Test Steps:**
1. Use Data Loader to insert 200 Cases
2. All Cases have:
   - Valid Account
   - Record Type = "New_Service_Case"
   - Integrate_with_Acorn__c = true
3. Wait 5 minutes for async processing

**Expected Results:**
- [ ] All 200 Cases created successfully
- [ ] 200 Platform Events published
- [ ] 200 integration attempts made
- [ ] ≥ 190 successful integrations (95% success rate)
- [ ] All failed integrations have retry entries in log
- [ ] No governor limit exceptions
- [ ] Processing completes within 5 minutes

**Actual Results:**
- Cases Created: _____
- Successful Integrations: _____
- Failed Integrations: _____
- Success Rate: _____%
- [ ] Pass / [ ] Fail

---

### 4.2 Work Order Acorn Integration Testing

**Test Case 4.2.1: New Work Order - Acorn Sync**

**Preconditions:**
- Case exists
- Acorn QA up

**Test Steps:**
1. Create new Work Order
2. Link to Case
3. Leave Acorn_WorkOrder_Id__c blank
4. Save Work Order

**Expected Results:**
- [ ] Work Order created successfully
- [ ] Platform Event published
- [ ] Acorn receives Work Order data
- [ ] Work Order.Acorn_WorkOrder_Id__c populated
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.2.2: Work Order with Existing Acorn ID**

**Preconditions:**
- Work Order exists with Acorn_WorkOrder_Id__c populated

**Test Steps:**
1. Update Work Order fields
2. Save Work Order

**Expected Results:**
- [ ] Work Order saved successfully
- [ ] NO Platform Event published (Acorn ID already exists)
- [ ] No duplicate in Acorn

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.2.3: Work Order with Bypass User**

**Preconditions:**
- Logged in as user with Bypass_Validation__c = true

**Test Steps:**
1. Create new Work Order
2. Save

**Expected Results:**
- [ ] Work Order created successfully
- [ ] NO Platform Event published (bypass flag honored)
- [ ] NO integration attempt

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 4.3 Quote Acorn Integration Testing

**Test Case 4.3.1: Quote Approval - Asset Creation in Acorn**

**Preconditions:**
- Quote exists with Status = "Draft"
- Acorn_integration_required__c = true
- Acorn QA up

**Test Steps:**
1. Open Quote
2. Change Status to "Approved"
3. Save Quote

**Expected Results:**
- [ ] Quote saved successfully
- [ ] Platform Event published
- [ ] Acorn receives Quote data
- [ ] Assets created in Acorn (verify in Acorn UI)
- [ ] Quote.DoResyncOutBoundcall__c set to false
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.3.2: Quote Manual Resync**

**Preconditions:**
- Quote exists with Status = "Approved"
- Previously synced to Acorn

**Test Steps:**
1. Open Quote
2. Set DoResyncOutBoundcall__c = true
3. Save Quote

**Expected Results:**
- [ ] Quote saved successfully
- [ ] Platform Event published for resync
- [ ] Acorn receives updated Quote data
- [ ] Quote.DoResyncOutBoundcall__c automatically set to false
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.3.3: Quote without Acorn Integration Flag**

**Preconditions:**
- Quote exists

**Test Steps:**
1. Set Acorn_integration_required__c = false
2. Change Status to "Approved"
3. Save

**Expected Results:**
- [ ] Quote saved successfully
- [ ] NO Platform Event published
- [ ] No Acorn integration attempt

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 4.4 Genesys Routing Integration Testing

**Test Case 4.4.1: Email-to-Case Genesys Routing**

**Preconditions:**
- Genesys QA environment up
- Email-to-Case configured

**Test Steps:**
1. Send test email to Email-to-Case address
2. Wait for Email Message to be created
3. Verify Case creation
4. Check Genesys_Routing__c record created

**Expected Results:**
- [ ] EmailMessage created
- [ ] Case created from email
- [ ] Genesys_Routing__c record created
- [ ] Platform Event published (EmailToGenesysEvent__e)
- [ ] Genesys receives routing request with all 20+ fields
- [ ] Agent assigned in Genesys (verify in Genesys UI)
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.4.2: Task Genesys Routing**

**Preconditions:**
- Genesys QA up
- Task with Process__c = "Notify Customer Of Service Update"

**Test Steps:**
1. Create Task record
2. Set required routing fields
3. Save Task

**Expected Results:**
- [ ] Task created successfully
- [ ] Genesys_Routing__c record created
- [ ] Platform Event published (TaskToGenesysEvent__e)
- [ ] Genesys receives routing request with all 25+ fields
- [ ] Task assigned to agent in Genesys
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.4.3: Genesys Routing Failure - Retry**

**Preconditions:**
- Genesys QA down or configured to return error

**Test Steps:**
1. Create qualifying Email or Task
2. Trigger routing
3. Monitor retry attempts

**Expected Results:**
- [ ] Initial routing attempt fails
- [ ] Retry attempt 1 after 2 seconds
- [ ] Retry attempt 2 after 4 seconds
- [ ] Retry attempt 3 after 8 seconds
- [ ] After 3 retries, permanent failure logged
- [ ] Email notification sent to admins
- [ ] Integration_Error_Log__c shows all retry attempts

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 4.5 SMS Opt-In Integration Testing (Contact)

**Test Case 4.5.1: Contact Mobile Phone Change - SMS API Call**

**Preconditions:**
- Contact exists with MobilePhone
- SMS API QA endpoint configured

**Test Steps:**
1. Open Contact
2. Change MobilePhone to new number
3. Save Contact

**Expected Results:**
- [ ] Contact saved successfully
- [ ] Async API call made to SMS provider (verify in logs)
- [ ] Text_Notifications_Opt_In__c status updated based on API response
- [ ] No blocking of user (async execution)
- [ ] Integration_Error_Log__c shows Success or Failure

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 4.5.2: SMS API Failure - Error Handling**

**Preconditions:**
- SMS API QA down

**Test Steps:**
1. Update Contact MobilePhone
2. Save

**Expected Results:**
- [ ] Contact saved successfully (not blocked by integration failure)
- [ ] API call attempted
- [ ] Error logged in Integration_Error_Log__c
- [ ] Retry logic executed (3 attempts)
- [ ] After retries, admin notification sent

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 4.6 Integration Performance Testing

**Test Case 4.6.1: Integration Response Time**

**Test Steps:**
1. Create 10 Cases with Acorn integration
2. Measure time from Case creation to Acorn sync completion
3. Calculate average response time

**Expected Results:**
- [ ] Average response time < 2 seconds
- [ ] Max response time < 5 seconds
- [ ] All integrations complete successfully

**Actual Results:**
- Average: _____ seconds
- Max: _____ seconds
- [ ] Pass / [ ] Fail

---

**Test Case 4.6.2: High Volume Integration**

**Test Steps:**
1. Create 500 Cases in rapid succession (via API)
2. Monitor Platform Event queue
3. Monitor integration completion

**Expected Results:**
- [ ] All 500 Cases created successfully
- [ ] All 500 Platform Events published
- [ ] All integrations process within 10 minutes
- [ ] ≥ 475 successful integrations (95% success rate)
- [ ] No system errors or timeouts
- [ ] Queue processes efficiently (no backlog)

**Actual Results:**
- Success Rate: _____%
- Processing Time: _____ minutes
- [ ] Pass / [ ] Fail

---

## 5. FUNCTIONAL TESTING CHECKLIST

### 5.1 Case Management Functional Testing

**Test Case 5.1.1: Case Reference Number Assignment**

**Test Steps:**
1. Create new Case without ParentId
2. Save Case

**Expected Results:**
- [ ] Case.Reference_Number__c = Case.CaseNumber
- [ ] Field populated before save (no additional DML)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.1.2: Child Case - No Reference Number**

**Test Steps:**
1. Create parent Case
2. Create child Case with ParentId = parent Case
3. Save child Case

**Expected Results:**
- [ ] Child Case created
- [ ] Child Case.Reference_Number__c remains blank (has parent)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.1.3: Case Status Transitions**

**Test Steps:**
1. Create Case with Status = "New"
2. Update Status to "In Progress"
3. Update Status to "Pending Customer"
4. Update Status to "Resolved"
5. Update Status to "Closed"

**Expected Results:**
- [ ] All status changes save successfully
- [ ] Acorn receives status updates for each change (if integration enabled)
- [ ] No errors or blocks

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.2 Email-to-Case Functional Testing

**Test Case 5.2.1: Email Message Processing - New Case Creation**

**Test Steps:**
1. Send email to Email-to-Case address
2. Email content: Subject = "Test Case from Email", Body = "This is a test"
3. Wait for processing (up to 5 minutes)

**Expected Results:**
- [ ] EmailMessage record created
- [ ] Case created from email
- [ ] Case.Subject matches email subject
- [ ] Case.Description contains email body
- [ ] Contact matched (if email matches existing Contact)
- [ ] Case.To_Be_Processed__c = false (processed)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.2.2: Email Message - Contact Matching (1:1 Match)**

**Test Steps:**
1. Create Contact with Email = "test@example.com"
2. Send email from "test@example.com" to Email-to-Case
3. Wait for processing

**Expected Results:**
- [ ] Case created
- [ ] Case.ContactId = matching Contact
- [ ] Case.AccountId = Contact's Account

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.2.3: Email Message - Genesys Routing Triggered**

**Test Steps:**
1. Send email to Email-to-Case (qualifying for routing)
2. Wait for Case creation and routing

**Expected Results:**
- [ ] Case created from email
- [ ] Genesys routing triggered
- [ ] Agent assigned in Genesys

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.2.4: Email Message - Indico ML Integration**

**Test Steps:**
1. Send email to Email-to-Case
2. Verify Indico processing

**Expected Results:**
- [ ] EmailMessage.IndicoStatus__c updated by Indico
- [ ] Case categorization based on Indico analysis
- [ ] Integration logs show Indico API call

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.3 Contact Management Functional Testing

**Test Case 5.3.1: Contact Preferred Language Sync**

**Test Steps:**
1. Create Contact
2. Set Preferred_Language__c = "Spanish"
3. Save Contact
4. Create Case for this Contact

**Expected Results:**
- [ ] Contact saved
- [ ] Related records (Case) have language preference synced
- [ ] Preferred language propagated correctly

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.3.2: Contact Text Notification Opt-In**

**Test Steps:**
1. Create Contact with MobilePhone
2. Set Text_Notifications_Opt_In__c = true
3. Change MobilePhone number
4. Save Contact

**Expected Results:**
- [ ] Contact saved
- [ ] SMS opt-in API called (async)
- [ ] Text_Notifications_Opt_In__c status updated based on new number
- [ ] User not blocked during save

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.4 Business Rule Functional Testing

**Test Case 5.4.1: Business Rule Channel Requirements Flag**

**Test Steps:**
1. Create Business_Rule__c record
2. Populate Channel_Req__c field with any value
3. Save Business Rule

**Expected Results:**
- [ ] Business Rule saved
- [ ] Is_Channel_Requirements__c automatically set to true

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.4.2: Business Rule Special Instructions Flag**

**Test Steps:**
1. Create Business_Rule__c record
2. Populate Special_Ins__c field with any value
3. Save Business Rule

**Expected Results:**
- [ ] Business Rule saved
- [ ] Is_Special_Instructions__c automatically set to true

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.4.3: Business Rule Alias Field Default**

**Test Steps:**
1. Create Business_Rule__c record
2. Leave Alias__c field blank
3. Set Name = "Test Rule 123"
4. Save Business Rule

**Expected Results:**
- [ ] Business Rule saved
- [ ] Alias__c automatically populated with Name value ("Test Rule 123")

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.4.4: Business Rule End Date Validation**

**Test Steps:**
1. Create Business_Rule__c record
2. Set End_Date__c = yesterday's date
3. Set Active__c = true
4. Save Business Rule

**Expected Results:**
- [ ] Business Rule saved
- [ ] Active__c automatically set to false (end date is past)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.4.5: Business Rule Expiration (Scheduled Flow)**

**Test Steps:**
1. Create Business_Rule__c record
2. Set End_Date__c = today's date
3. Set Active__c = true
4. Save Business Rule
5. Wait for scheduled flow to run next day (or run manually if possible)

**Expected Results:**
- [ ] Business Rule saved as Active
- [ ] After End_Date__c passes, scheduled flow runs
- [ ] Active__c set to false by scheduled flow
- [ ] Admin notification sent (if configured)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.5 Quote Management Functional Testing

**Test Case 5.5.1: Quote Chatter Notification**

**Test Steps:**
1. Create Quote
2. Change Quote status or key field
3. Save Quote

**Expected Results:**
- [ ] Quote saved
- [ ] Chatter post created on Quote record
- [ ] Stakeholders mentioned/notified in Chatter
- [ ] Post content describes the change

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.5.2: Quote Approval Process**

**Test Steps:**
1. Create Quote with Status = "Draft"
2. Submit for approval
3. Approve Quote (Status changes to "Approved")
4. Verify Acorn integration triggered

**Expected Results:**
- [ ] Quote approved
- [ ] Status = "Approved"
- [ ] Acorn integration triggered (if Acorn_integration_required__c = true)
- [ ] Assets created in Acorn

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.6 Task Management Functional Testing

**Test Case 5.6.1: Task Attempt Counter Update**

**Test Steps:**
1. Create Task
2. Set Process__c = "Notify Customer Of Service Update"
3. Set Attempt__c = 1
4. Save Task

**Expected Results:**
- [ ] Task saved
- [ ] Attempt__c automatically updated to 2

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.6.2: Task Genesys Routing**

**Test Steps:**
1. Create Task with routing criteria
2. Save Task

**Expected Results:**
- [ ] Task saved
- [ ] Genesys routing triggered
- [ ] Task assigned to agent

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.7 Additional Object Functional Testing

**Test Case 5.7.1: Entitlement Name Generation**

**Test Steps:**
1. Create Entitlement record
2. Link to Account and Service
3. Leave Name blank
4. Save Entitlement

**Expected Results:**
- [ ] Entitlement saved
- [ ] Name auto-generated using formula (Account + Service + Category)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.7.2: Account Title Duplicate Prevention**

**Test Steps:**
1. Create Account_Title__c record
2. Set Name = "Test Title"
3. Link to Account
4. Save Account Title

**Expected Results:**
- [ ] Account Title saved
- [ ] Duplicate_Title__c = Name + Account.Id (unique identifier)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.7.3: Case Comment Timestamp Sync**

**Test Steps:**
1. Create Case
2. Add CaseComment to Case
3. Save CaseComment

**Expected Results:**
- [ ] CaseComment created
- [ ] Case.CaseComment_CreateDate__c updated to CaseComment.CreatedDate

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.7.4: Notification Contact Phone Formatting**

**Test Steps:**
1. Create Contact with MobilePhone = "5551234567"
2. Create Notification_Contact__c record
3. Link to Contact
4. Save Notification Contact

**Expected Results:**
- [ ] Notification Contact saved
- [ ] ISD_Phone__c = "+15551234567" (formatted with +1 prefix)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.7.5: Comment Acorn User ID Population**

**Test Steps:**
1. Login as test user with Acorn_SUser_ID__c populated
2. Create Comment__c record
3. Leave Acorn_SUser_ID__c blank on Comment
4. Save Comment

**Expected Results:**
- [ ] Comment saved
- [ ] Comment.Acorn_SUser_ID__c = current User.Acorn_SUser_ID__c

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.7.6: Comment Task Values to Acorn**

**Test Steps:**
1. Create Comment__c with Task values
2. Set Acorn_Tracking_Number__c
3. Save Comment

**Expected Results:**
- [ ] Comment saved
- [ ] Platform Event published (CommentToAcornEvent__e)
- [ ] Acorn receives comment data
- [ ] Integration_Error_Log__c shows Success

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.8 Account SLA Creation Flow Testing

**Test Case 5.8.1: Account Activation - SLA Creation**

**Test Steps:**
1. Create Account
2. Set Status = "Inactive"
3. Save Account
4. Update Status to "Active"
5. Save Account

**Expected Results:**
- [ ] Account saved
- [ ] Record-Triggered Flow executes
- [ ] Entitlement record(s) created for Account
- [ ] Entitlement.AccountId = Account.Id
- [ ] No duplicate Entitlements created (check logic)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 5.8.2: Account Activation - Existing SLA**

**Test Steps:**
1. Create Account with existing Entitlement
2. Activate Account

**Expected Results:**
- [ ] Account saved
- [ ] Flow checks for existing Entitlement
- [ ] No duplicate Entitlement created
- [ ] Existing Entitlement retained

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 5.9 Supplier Score Trending Flow Testing

**Test Case 5.9.1: Supplier Score Update**

**Test Steps:**
1. Create or update Supplier record
2. Update score-related fields
3. Save Supplier

**Expected Results:**
- [ ] Supplier saved
- [ ] Record-Triggered Flow executes
- [ ] Trend calculations performed
- [ ] Trend indicator fields updated
- [ ] Historical data preserved

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 6. PERFORMANCE TESTING CHECKLIST

### 6.1 Baseline Performance Comparison

**Test Case 6.1.1: Single Case Creation - Performance**

**Test Steps:**
1. Enable debug logs
2. Create single Case with Acorn integration
3. Capture execution time from debug logs

**Expected Results:**
- [ ] Total execution time ≤ 200ms (target)
- [ ] Trigger execution time ≤ 100ms
- [ ] Platform Event publish time ≤ 50ms
- [ ] Performance improved or equal to baseline

**Actual Results:**
- Total Time: _____ ms
- Trigger Time: _____ ms
- Event Publish Time: _____ ms
- [ ] Pass / [ ] Fail

---

**Test Case 6.1.2: Bulk Case Creation - Performance**

**Test Steps:**
1. Use Data Loader to create 200 Cases
2. Measure total processing time

**Expected Results:**
- [ ] All 200 Cases created successfully
- [ ] Total processing time ≤ 5 seconds
- [ ] No governor limit exceptions
- [ ] Memory usage acceptable

**Actual Results:**
- Processing Time: _____ seconds
- [ ] Pass / [ ] Fail

---

**Test Case 6.1.3: Email-to-Case Processing - Performance**

**Test Steps:**
1. Send 10 emails to Email-to-Case
2. Measure average processing time per email

**Expected Results:**
- [ ] All emails processed successfully
- [ ] Average processing time ≤ 1000ms (improved from 1500ms baseline)
- [ ] All Cases created within 5 minutes

**Actual Results:**
- Average Time: _____ ms
- [ ] Pass / [ ] Fail

---

**Test Case 6.1.4: Platform Event Delivery Time**

**Test Steps:**
1. Publish 100 Platform Events
2. Measure time from publish to subscriber execution

**Expected Results:**
- [ ] All events delivered successfully
- [ ] Average delivery time ≤ 50ms
- [ ] Max delivery time ≤ 100ms

**Actual Results:**
- Average: _____ ms
- Max: _____ ms
- [ ] Pass / [ ] Fail

---

**Test Case 6.1.5: Integration Response Time**

**Test Steps:**
1. Trigger 50 Acorn integrations
2. Measure HTTP callout response time

**Expected Results:**
- [ ] Average response time < 2 seconds
- [ ] Max response time < 5 seconds
- [ ] 95th percentile < 3 seconds

**Actual Results:**
- Average: _____ seconds
- Max: _____ seconds
- 95th percentile: _____ seconds
- [ ] Pass / [ ] Fail

---

### 6.2 Load Testing

**Test Case 6.2.1: High Volume Transaction Processing**

**Test Steps:**
1. Use API to create 1000 Cases rapidly
2. Monitor system performance
3. Monitor Platform Event queue
4. Wait for all integrations to complete

**Expected Results:**
- [ ] All 1000 Cases created successfully
- [ ] No system errors or timeouts
- [ ] Platform Event queue processes efficiently
- [ ] All integrations complete within 15 minutes
- [ ] Success rate ≥ 95%
- [ ] System remains responsive to other users

**Actual Results:**
- Cases Created: _____
- Integrations Successful: _____
- Processing Time: _____ minutes
- Success Rate: _____%
- [ ] Pass / [ ] Fail

---

**Test Case 6.2.2: Concurrent User Load**

**Test Steps:**
1. Simulate 20 users creating Cases simultaneously
2. Each user creates 10 Cases
3. Monitor system performance

**Expected Results:**
- [ ] All 200 Cases created successfully
- [ ] No locking or concurrency issues
- [ ] Response time acceptable for all users (<3 seconds per save)
- [ ] No errors displayed to users

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 6.3 Governor Limit Testing

**Test Case 6.3.1: SOQL Query Limit Test**

**Test Steps:**
1. Create 200 Cases with complex related data
2. Monitor SOQL query usage in debug logs

**Expected Results:**
- [ ] SOQL queries used < 50 (out of 100 limit)
- [ ] No "Too many SOQL queries" errors
- [ ] Queries are bulkified (not in loops)

**Actual Results:**
- SOQL Queries Used: _____ / 100
- [ ] Pass / [ ] Fail

---

**Test Case 6.3.2: DML Statement Limit Test**

**Test Steps:**
1. Create 200 Cases that trigger multiple updates
2. Monitor DML usage

**Expected Results:**
- [ ] DML statements < 75 (out of 150 limit)
- [ ] No "Too many DML statements" errors
- [ ] DMLs are bulkified

**Actual Results:**
- DML Statements Used: _____ / 150
- [ ] Pass / [ ] Fail

---

**Test Case 6.3.3: CPU Time Limit Test**

**Test Steps:**
1. Create 200 Cases with complex processing
2. Monitor CPU time in debug logs

**Expected Results:**
- [ ] CPU time < 5000ms (out of 10000ms limit)
- [ ] No CPU time limit exceptions

**Actual Results:**
- CPU Time Used: _____ ms / 10000 ms
- [ ] Pass / [ ] Fail

---

**Test Case 6.3.4: Heap Size Limit Test**

**Test Steps:**
1. Create 200 Cases with large payloads
2. Monitor heap size usage

**Expected Results:**
- [ ] Heap size < 3 MB (out of 6 MB limit)
- [ ] No heap size limit exceeded errors
- [ ] Collections cleared when no longer needed

**Actual Results:**
- Heap Size Used: _____ MB / 6 MB
- [ ] Pass / [ ] Fail

---

## 7. SECURITY TESTING CHECKLIST

### 7.1 Access Control Testing

**Test Case 7.1.1: Standard User - Object Access**

**Test Steps:**
1. Login as Standard User (no admin rights)
2. Attempt to view Integration_Error_Log__c records
3. Attempt to create Integration_Error_Log__c record

**Expected Results:**
- [ ] User can view Integration_Error_Log__c records (Public Read Only)
- [ ] User CANNOT create Integration_Error_Log__c manually
- [ ] User CANNOT edit Integration_Error_Log__c records
- [ ] User CANNOT delete Integration_Error_Log__c records

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 7.1.2: Admin User - Full Access**

**Test Steps:**
1. Login as System Administrator
2. Access Integration_Error_Log__c
3. View all fields including sensitive fields

**Expected Results:**
- [ ] Admin can view all records
- [ ] Admin can view Stack_Trace__c and Payload__c fields
- [ ] Admin can manually create records (if needed for testing)
- [ ] Admin can delete records

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 7.1.3: Sharing Rules Respected**

**Test Steps:**
1. Login as Standard User
2. Create Case owned by User
3. Login as different Standard User
4. Attempt to view the Case

**Expected Results:**
- [ ] Sharing rules respected (Case visible/not visible based on OWD)
- [ ] Automation runs in appropriate context (system or user mode)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 7.2 Data Privacy Testing

**Test Case 7.2.1: PII Masking in Logs**

**Test Steps:**
1. Create Case with customer email and phone
2. Trigger integration that logs payload
3. View Integration_Error_Log__c.Payload__c field

**Expected Results:**
- [ ] Email addresses masked (show first 3 chars + @domain)
- [ ] Phone numbers masked (show last 4 digits only)
- [ ] No SSN or credit card numbers logged
- [ ] Customer names hashed or masked

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 7.2.2: Sensitive Field Encryption**

**Test Steps:**
1. Query Integration_Error_Log__c with sensitive data
2. Verify encryption at rest (if configured)

**Expected Results:**
- [ ] Payload__c field encrypted (if platform encryption enabled)
- [ ] Sensitive data not accessible without proper decryption keys

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 7.3 Integration Security Testing

**Test Case 7.3.1: Named Credential Authentication**

**Test Steps:**
1. Verify Acorn_API Named Credential
2. Test authentication

**Expected Results:**
- [ ] Named Credential uses secure authentication (OAuth or encrypted password)
- [ ] No hardcoded credentials in code
- [ ] Credentials stored securely in Salesforce

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 7.3.2: API Endpoint Security**

**Test Steps:**
1. Verify all HTTP callouts use HTTPS
2. Review callout endpoints in code

**Expected Results:**
- [ ] All endpoints use HTTPS (not HTTP)
- [ ] All endpoints use Named Credentials (not hardcoded URLs)
- [ ] API keys/tokens not exposed in logs

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 7.4 Injection and Vulnerability Testing

**Test Case 7.4.1: SOQL Injection Prevention**

**Test Steps:**
1. Attempt to create Case with malicious input in Subject
2. Subject = "Test' OR '1'='1"
3. Save Case

**Expected Results:**
- [ ] Case saved without error
- [ ] Input properly sanitized
- [ ] No SOQL injection vulnerability
- [ ] Query uses bind variables (not string concatenation)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 7.4.2: XSS Prevention**

**Test Steps:**
1. Create Case with Subject containing script tag
2. Subject = "<script>alert('XSS')</script>"
3. View Case in UI

**Expected Results:**
- [ ] Script tag rendered as text (not executed)
- [ ] Lightning Locker Service prevents XSS
- [ ] No JavaScript execution in UI

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 8. REGRESSION TESTING CHECKLIST

### 8.1 Existing Functionality Validation

**Test Case 8.1.1: Existing Triggers Still Function**

**Test Steps:**
1. Review list of all existing triggers not modified by this project
2. Test sample records for each object with existing triggers

**Expected Results:**
- [ ] All existing triggers still execute correctly
- [ ] No unexpected behavior changes
- [ ] Order of execution not adversely affected

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 8.1.2: Existing Flows Still Function**

**Test Steps:**
1. Test all existing Flows not part of this migration
2. Verify they execute as expected

**Expected Results:**
- [ ] All existing Flows execute correctly
- [ ] No interference from new automation

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 8.1.3: CPQ Quote-to-Order Process**

**Test Steps:**
1. Create Quote with products
2. Approve Quote
3. Create Order from Quote
4. Verify all CPQ functionality

**Expected Results:**
- [ ] Quote-to-Order process works identically to before
- [ ] All CPQ calculations correct
- [ ] No errors in CPQ automation

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 8.1.4: Standard Salesforce Features**

**Test Steps:**
1. Test standard features: Tasks, Events, Reports, Dashboards
2. Verify no impact from new automation

**Expected Results:**
- [ ] All standard features work normally
- [ ] No unexpected behavior

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 8.2 Validation Rules Testing

**Test Case 8.2.1: Existing Validation Rules**

**Test Steps:**
1. Test all validation rules on Case, Contact, WorkOrder, Quote, etc.
2. Attempt to violate each validation rule

**Expected Results:**
- [ ] All validation rules still fire correctly
- [ ] Error messages display properly
- [ ] Records blocked when validation fails

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 8.3 Permission Set Testing

**Test Case 8.3.1: Permission Sets Unaffected**

**Test Steps:**
1. Test users with various permission sets
2. Verify object and field access unchanged

**Expected Results:**
- [ ] All permission sets work as before
- [ ] No unexpected access granted or denied

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 9. BULK PROCESSING TESTING

### 9.1 Data Loader Testing

**Test Case 9.1.1: Bulk Insert 200 Cases**

[Covered in Section 4.1.6]

---

**Test Case 9.1.2: Bulk Update 200 Cases**

**Test Steps:**
1. Query 200 existing Cases
2. Update Status field for all
3. Use Data Loader to update

**Expected Results:**
- [ ] All 200 Cases updated successfully
- [ ] Appropriate automation triggered for each
- [ ] No governor limit exceptions
- [ ] Processing time ≤ 5 seconds

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 9.1.3: Bulk Insert 200 Work Orders**

**Test Steps:**
1. Create CSV with 200 Work Orders
2. Import via Data Loader

**Expected Results:**
- [ ] All 200 Work Orders created
- [ ] Acorn integration triggered for each (if applicable)
- [ ] No errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 9.1.4: Bulk Insert 200 Contacts**

**Test Steps:**
1. Create CSV with 200 Contacts with MobilePhone
2. Import via Data Loader

**Expected Results:**
- [ ] All 200 Contacts created
- [ ] SMS opt-in API called asynchronously (if applicable)
- [ ] No blocking of Data Loader operation
- [ ] No errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 9.2 API Bulk Testing

**Test Case 9.2.1: REST API Bulk Insert**

**Test Steps:**
1. Use REST API to insert 200 Cases in bulk
2. Monitor response and processing

**Expected Results:**
- [ ] All 200 Cases created
- [ ] API returns success responses
- [ ] Automation triggered correctly

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 10. ERROR HANDLING TESTING

### 10.1 Exception Handling

**Test Case 10.1.1: Null Pointer Exception Handling**

**Test Steps:**
1. Create Case with missing required related data
2. Trigger automation

**Expected Results:**
- [ ] Exception caught gracefully
- [ ] User-friendly error message (if applicable)
- [ ] Error logged in Integration_Error_Log__c
- [ ] System continues processing other records

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 10.1.2: DML Exception Handling**

**Test Steps:**
1. Create record that violates database constraints
2. Trigger automation

**Expected Results:**
- [ ] DML exception caught
- [ ] Error logged
- [ ] User notified of specific field error
- [ ] Processing continues for valid records

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 10.1.3: Callout Exception Handling**

**Test Steps:**
1. Configure external system to timeout
2. Trigger integration

**Expected Results:**
- [ ] Callout exception caught
- [ ] Retry logic activated
- [ ] Error logged with details
- [ ] Admin notification after retries exhausted

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 10.2 Retry Logic Testing

**Test Case 10.2.1: First Retry Attempt**

[Covered in Section 4.1.5]

---

**Test Case 10.2.2: Exponential Backoff Validation**

**Test Steps:**
1. Force integration failure
2. Monitor retry timing in logs

**Expected Results:**
- [ ] Retry 1 after 2 seconds
- [ ] Retry 2 after 4 seconds
- [ ] Retry 3 after 8 seconds
- [ ] Exponential backoff working correctly

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 10.3 Error Notification Testing

**Test Case 10.3.1: Admin Email Notification**

**Test Steps:**
1. Force permanent integration failure (after 3 retries)
2. Check admin email

**Expected Results:**
- [ ] Email sent to integrations@company.com
- [ ] Email contains: Case Number, Error Message, Correlation ID
- [ ] Email subject line clear: "ALERT: Acorn Integration Failure"

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 10.3.2: Slack Notification (if configured)**

**Test Steps:**
1. Force integration failure
2. Check Slack #integrations-alerts channel

**Expected Results:**
- [ ] Slack message posted
- [ ] Message contains key details
- [ ] Message includes link to dashboard

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 11. MONITORING AND LOGGING TESTING

### 11.1 Logging Validation

**Test Case 11.1.1: Success Logging**

**Test Steps:**
1. Create Case with successful Acorn integration
2. Query Integration_Error_Log__c

**Expected Results:**
- [ ] Log record created
- [ ] Status__c = "Success"
- [ ] Source_Record_Id__c = Case.Id
- [ ] Correlation_Id__c populated
- [ ] Timestamp__c = current time
- [ ] Integration_Name__c = "Case to Acorn"

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 11.1.2: Error Logging**

**Test Steps:**
1. Force integration error
2. Query Integration_Error_Log__c

**Expected Results:**
- [ ] Log record created
- [ ] Status__c = "Failed"
- [ ] Error_Message__c contains error details
- [ ] Stack_Trace__c populated (if exception)
- [ ] Retry_Count__c = 3
- [ ] Payload__c contains request data

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 11.1.3: Retry Logging**

**Test Steps:**
1. Force retriable error
2. Monitor logs for retry attempts

**Expected Results:**
- [ ] Log record created for each retry
- [ ] Status__c = "Retry"
- [ ] Retry_Count__c increments (1, 2, 3)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 11.2 Dashboard Testing

**Test Case 11.2.1: Integration Health Monitor Dashboard**

**Test Steps:**
1. Navigate to Integration_Health_Monitor dashboard
2. Verify all components load

**Expected Results:**
- [ ] Dashboard loads successfully
- [ ] Success Rate by Integration component displays data
- [ ] Failed Integrations table displays recent failures
- [ ] Average Response Time chart displays data
- [ ] Integration Volume chart displays data
- [ ] Retry Queue Depth metric displays current count

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 11.2.2: Dashboard Real-Time Update**

**Test Steps:**
1. Open dashboard
2. Create integration transaction
3. Refresh dashboard

**Expected Results:**
- [ ] Dashboard updates with new data within 1 minute
- [ ] Metrics accurately reflect new transaction

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 11.2.3: Dashboard Drill-Down**

**Test Steps:**
1. Click on Failed Integrations table row
2. Navigate to detail

**Expected Results:**
- [ ] Clicking row opens Integration_Error_Log__c record
- [ ] All details visible (error message, payload, etc.)

**Actual Results:**
- [ ] Pass / [ ] Fail

---

### 11.3 Alert Testing

**Test Case 11.3.1: Failure Rate Alert**

**Test Steps:**
1. Force 20 integration failures out of 100 attempts (20% failure rate, below 90% threshold)
2. Wait for alert processing

**Expected Results:**
- [ ] Email alert sent to integrations@company.com
- [ ] Subject: "WARNING: [Integration] Success Rate Below Threshold"
- [ ] Email contains current success rate (80%)
- [ ] Email contains recommended actions

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 12. PRE-PRODUCTION VALIDATION

### 12.1 Deployment Readiness Checklist

**Code Review:**
- [ ] All code reviewed and approved by Lead Developer
- [ ] Code follows coding standards
- [ ] No hardcoded IDs or URLs
- [ ] All classes have appropriate access modifiers (with sharing / without sharing)

**Testing Completion:**
- [ ] All unit tests pass (90%+ coverage)
- [ ] All integration tests pass
- [ ] All functional tests pass
- [ ] Performance testing completed and targets met
- [ ] Security testing completed with no critical vulnerabilities
- [ ] Regression testing completed
- [ ] UAT sign-off obtained

**Documentation:**
- [ ] Functional/Technical Design Document complete
- [ ] QA Test Results documented
- [ ] UAT Test Results documented
- [ ] Deployment guide prepared
- [ ] Rollback procedures documented and tested

**External Dependencies:**
- [ ] Acorn QA team notified and ready
- [ ] Genesys team notified and ready
- [ ] All external systems in QA environment available

**Change Management:**
- [ ] Change request submitted and approved
- [ ] Deployment window scheduled
- [ ] Operations team briefed
- [ ] Support team briefed
- [ ] Communication sent to end users (if applicable)

**Monitoring:**
- [ ] Monitoring dashboards deployed and tested
- [ ] Alert email addresses confirmed
- [ ] Incident response plan ready

### 12.2 Final Sandbox Validation

**Test Case 12.2.1: Full End-to-End Smoke Test**

**Test Steps:**
1. Create Case → Verify Acorn sync
2. Send Email → Verify Email-to-Case → Verify Genesys routing
3. Create Work Order → Verify Acorn sync
4. Create Quote → Approve → Verify Acorn sync
5. Update Contact phone → Verify SMS API call
6. Create Business Rule → Verify field updates
7. Verify all logs and dashboards

**Expected Results:**
- [ ] All processes complete successfully end-to-end
- [ ] All integrations successful
- [ ] All logs created correctly
- [ ] Dashboard displays accurate data
- [ ] Zero errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 12.2.2: Rollback Procedure Test**

**Test Steps:**
1. Document current state
2. Deactivate new automation
3. Reactivate old automation
4. Test transactions with old automation
5. Verify functionality restored

**Expected Results:**
- [ ] Rollback completes in < 15 minutes
- [ ] Old automation functions correctly
- [ ] All transactions process successfully
- [ ] No data loss or corruption

**Actual Results:**
- [ ] Pass / [ ] Fail

---

## 13. PRODUCTION SMOKE TESTING

### 13.1 Post-Deployment Smoke Tests

**Note:** These tests should be executed immediately after production deployment during the monitoring window.

**Test Case 13.1.1: Case Creation - Production**

**Test Steps:**
1. Login to production
2. Create test Case with Subject = "QA Smoke Test - [Timestamp]"
3. Set Integrate_with_Acorn__c = true
4. Save

**Expected Results:**
- [ ] Case created successfully
- [ ] Reference Number populated
- [ ] Platform Event published (check logs)
- [ ] Acorn integration successful
- [ ] No user errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 13.1.2: Email-to-Case - Production**

**Test Steps:**
1. Send test email to production Email-to-Case address
2. Subject = "QA Smoke Test - [Timestamp]"
3. Wait 5 minutes for processing

**Expected Results:**
- [ ] EmailMessage created
- [ ] Case created from email
- [ ] Genesys routing triggered (if applicable)
- [ ] No errors in logs

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 13.1.3: Work Order Creation - Production**

**Test Steps:**
1. Create test Work Order
2. Leave Acorn_WorkOrder_Id__c blank
3. Save

**Expected Results:**
- [ ] Work Order created
- [ ] Acorn integration triggered
- [ ] Acorn_WorkOrder_Id__c populated
- [ ] No errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 13.1.4: Monitoring Dashboard - Production**

**Test Steps:**
1. Navigate to Integration_Health_Monitor dashboard
2. Verify data is populating

**Expected Results:**
- [ ] Dashboard accessible
- [ ] Real-time data displaying
- [ ] Success rates showing
- [ ] No errors

**Actual Results:**
- [ ] Pass / [ ] Fail

---

**Test Case 13.1.5: Integration Success Rate - First Hour**

**Test Steps:**
1. Monitor integration success rate for first hour post-deployment
2. Check Integration_Error_Log__c every 15 minutes

**Expected Results:**
- [ ] Success rate ≥ 95%
- [ ] No critical errors
- [ ] Response times within acceptable range
- [ ] No governor limit errors

**Actual Results:**
- Hour 1 Success Rate: _____%
- [ ] Pass / [ ] Fail

---

### 13.2 24-Hour Monitoring Checklist

**Checklist for first 24 hours post-deployment:**

**Hour 1:**
- [ ] All smoke tests passed
- [ ] Integration success rate ≥ 95%
- [ ] No critical errors
- [ ] Dashboard updating

**Hour 4:**
- [ ] Success rate still ≥ 95%
- [ ] No new critical errors
- [ ] Performance acceptable
- [ ] User feedback positive (or no complaints)

**Hour 12:**
- [ ] Overnight batch jobs completed successfully
- [ ] Success rate maintained
- [ ] No escalations

**Hour 24:**
- [ ] Full day of successful operations
- [ ] Success rate ≥ 95%
- [ ] All automation functioning correctly
- [ ] Ready to proceed with old automation cleanup

---

## 14. SIGN-OFF

### 14.1 QA Testing Sign-Off

**I certify that all required testing has been completed successfully and the solution is ready for production deployment.**

---

**QA Lead:**

Signature: _________________________ Date: _____________

Name: _________________________

**Test Results Summary:**
- Total Test Cases: _____
- Passed: _____
- Failed: _____
- Blocked: _____
- Pass Rate: _____%

**Critical Defects:**
- P1 (Critical): _____ (must be 0 for sign-off)
- P2 (High): _____ (must be addressed or accepted)
- P3 (Medium): _____ (can be fixed post-deployment)
- P4 (Low): _____ (can be fixed post-deployment)

---

**Lead Developer:**

Signature: _________________________ Date: _____________

Name: _________________________

**Code Quality Confirmation:**
- Apex Test Coverage: _____%
- All Tests Passing: [ ] Yes / [ ] No
- Code Review Complete: [ ] Yes / [ ] No

---

**Project Manager:**

Signature: _________________________ Date: _____________

Name: _________________________

**Project Status:**
- On Schedule: [ ] Yes / [ ] No
- Within Budget: [ ] Yes / [ ] No
- UAT Complete: [ ] Yes / [ ] No
- Ready for Deployment: [ ] Yes / [ ] No

---

**END OF QA TESTING CHECKLIST**

**Total Test Cases:** ~150
**Estimated Testing Time:** 80-120 hours
**Testing Team Size:** 2-3 QA Engineers
