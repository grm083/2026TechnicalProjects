# USER ACCEPTANCE TESTING (UAT) CHECKLIST
## Workflow Rules and Process Builder Modernization

**Project Name:** Process Builder and Workflow Rule Modernization Initiative
**Project Code:** PBWR-2026
**Document Type:** User Acceptance Testing Checklist
**Document Version:** 1.0
**Date:** January 15, 2026
**Status:** READY FOR UAT

---

## DOCUMENT PURPOSE

This User Acceptance Testing (UAT) Checklist is designed for business users to validate that all existing business processes continue to function correctly after the Process Builder and Workflow Rule modernization. No technical knowledge is required to complete this testing.

**Important:** This modernization project maintains all existing functionality. Everything should work exactly as it did before - no changes to business processes or user experience.

---

## TABLE OF CONTENTS

1. [UAT Overview](#1-uat-overview)
2. [Getting Started](#2-getting-started)
3. [Case Management Testing](#3-case-management-testing)
4. [Email and Communication Testing](#4-email-and-communication-testing)
5. [Work Order Testing](#5-work-order-testing)
6. [Quote and Pricing Testing](#6-quote-and-pricing-testing)
7. [Contact Management Testing](#7-contact-management-testing)
8. [Task Management Testing](#8-task-management-testing)
9. [Business Rules Testing](#9-business-rules-testing)
10. [General System Testing](#10-general-system-testing)
11. [Feedback and Issue Reporting](#11-feedback-and-issue-reporting)
12. [UAT Sign-Off](#12-uat-sign-off)

---

## 1. UAT OVERVIEW

### 1.1 What Is Being Tested?

We have modernized the underlying technology that powers your Salesforce automation (the "behind-the-scenes" processes). The way you use Salesforce should not change at all. This testing verifies that:

- ✅ All your daily tasks work the same way
- ✅ Cases, Work Orders, and Quotes process correctly
- ✅ Integrations with external systems (Acorn, Genesys) work properly
- ✅ Email processing and notifications work as expected
- ✅ Nothing is broken or behaving differently

### 1.2 What's NOT Changing?

- ❌ No changes to how you create Cases, Work Orders, or Quotes
- ❌ No changes to screens, layouts, or buttons
- ❌ No changes to business rules or processes
- ❌ No changes to reports or dashboards
- ❌ No new features or functionality

### 1.3 Who Should Participate in UAT?

**Primary Testers (Required):**
- Case Management Representatives (2-3 people)
- Work Order Coordinators (1-2 people)
- Quote/Pricing Team Representatives (1-2 people)
- Customer Service Supervisors (1-2 people)

**Secondary Testers (Optional but Recommended):**
- Field Service Coordinators
- Contact Center Agents
- Sales Representatives
- Managers/Team Leads

### 1.4 Testing Timeline

**Week 1:** UAT training and environment setup
**Week 2-3:** Active testing by business users
**Week 4:** Issue resolution and retesting
**Final:** UAT sign-off and production deployment planning

### 1.5 Time Commitment

- **Training Session:** 1 hour
- **Testing Time:** 4-8 hours per tester (spread over 2 weeks)
- **Flexibility:** Test during your normal work hours using real scenarios

---

## 2. GETTING STARTED

### 2.1 Test Environment Access

**Sandbox Environment:** You will be testing in a copy of production called a "sandbox."

**Access Instructions:**
1. Navigate to: [Sandbox URL will be provided]
2. Login with your username + ".sandbox"
   - Example: If your production username is john.doe@company.com, use john.doe@company.com.sandbox
3. Use your regular password

**Important Notes:**
- This is NOT the production environment - it's safe to test!
- Data in sandbox is a copy from [date] - recent records may not exist
- Changes you make in sandbox will NOT affect production

### 2.2 What You'll Need

**Before Starting UAT:**
- [ ] Sandbox access confirmed (can login successfully)
- [ ] Attended UAT kickoff training session
- [ ] Received this UAT checklist
- [ ] Know how to report issues (see Section 11)
- [ ] Have 30-60 minutes of uninterrupted time for first testing session

**Testing Materials:**
- This checklist (print or keep open on second screen)
- Your normal business processes and scenarios
- Real examples of Cases, Work Orders, Quotes you typically create

### 2.3 How to Complete This Checklist

**For Each Test Scenario:**

1. **Read the scenario description**
2. **Follow the steps exactly as written**
3. **Verify the expected outcome**
4. **Mark Pass ✅ or Fail ❌**
   - **Pass:** Everything works as expected, same as before
   - **Fail:** Something is different, broken, or doesn't work
5. **If Fail, describe the issue in the Notes section**
6. **Report any failures immediately** (don't wait until end of testing)

**Example:**
```
Test: Create a Case
Steps: 1. Click Cases tab, 2. Click New, 3. Fill in required fields, 4. Save
Expected: Case created successfully, Case Number assigned
Result: ✅ Pass  ❌ Fail
Notes: _______________
```

### 2.4 Testing Tips

**DO:**
- ✅ Test using your real, daily scenarios
- ✅ Test the processes you use most often
- ✅ Report issues as soon as you find them
- ✅ Ask questions if anything is unclear
- ✅ Test like you're working normally (don't try to "break" the system)

**DON'T:**
- ❌ Rush through the checklist
- ❌ Skip scenarios that seem unimportant
- ❌ Assume someone else will find the issue
- ❌ Wait until the end to report problems
- ❌ Test in production (only test in sandbox!)

---

## 3. CASE MANAGEMENT TESTING

### 3.1 Creating a New Case

**Business Context:** You need to create a new service request for a customer.

**Test Scenario 3.1.1: Standard Case Creation**

**Steps:**
1. Click on the **Cases** tab
2. Click **New** button
3. Fill in the following:
   - **Account:** Select a test account (e.g., "Test Account ABC")
   - **Contact:** Select a contact for the account
   - **Subject:** "UAT Test - New Service Case [Your Name] [Today's Date]"
   - **Status:** New
   - **Description:** "This is a test case for UAT"
   - **Case Type:** Select appropriate type (e.g., New Service)
4. Click **Save**

**Expected Outcome:**
- ✅ Case is created successfully
- ✅ You see the Case detail page
- ✅ Case Number is automatically assigned (e.g., 00001234)
- ✅ Reference Number field is populated (should match Case Number)
- ✅ No error messages appear

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 3.1.2: Case Status Changes**

**Steps:**
1. Open the Case you just created
2. Click **Edit** button
3. Change **Status** from "New" to "In Progress"
4. Click **Save**
5. Wait 1-2 minutes
6. Refresh the page
7. Check if Acorn Issue ID field is populated (if applicable for your cases)

**Expected Outcome:**
- ✅ Case Status changes to "In Progress" successfully
- ✅ Page saves without errors
- ✅ If your cases integrate with Acorn, the Acorn Issue ID should appear within 2 minutes
- ✅ Case updates work the same as before

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 3.1.3: Closing a Case**

**Steps:**
1. Open an existing Case (or use the one from 3.1.1)
2. Update **Status** to "Closed"
3. Fill in any required closure fields (e.g., Resolution Notes)
4. Click **Save**

**Expected Outcome:**
- ✅ Case closes successfully
- ✅ Case appears as Closed in your Case list
- ✅ Closing process works identically to before

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 3.2 Case with Parent-Child Relationship

**Test Scenario 3.2.1: Creating a Child Case**

**Steps:**
1. Find an existing Case to use as the parent
2. On the parent Case, click **New** in the Related Cases section
3. Fill in child Case details
4. Ensure **Parent Case** field is populated
5. Click **Save**

**Expected Outcome:**
- ✅ Child Case created successfully
- ✅ Child Case's Reference Number is BLANK (only parent cases get Reference Number)
- ✅ Parent-child relationship visible on both Case records

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 3.3 Multiple Cases (Bulk Testing)

**Test Scenario 3.3.1: Creating 5 Cases Quickly**

**Steps:**
1. Create 5 Cases back-to-back using the same steps as 3.1.1
2. Use different Subjects: "UAT Bulk Test 1", "UAT Bulk Test 2", etc.
3. Save each Case
4. Verify all 5 Cases are in your Recent Cases list

**Expected Outcome:**
- ✅ All 5 Cases created successfully
- ✅ No errors or slowdowns
- ✅ All Case Numbers assigned
- ✅ System performance feels normal

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 4. EMAIL AND COMMUNICATION TESTING

### 4.1 Email-to-Case Processing

**Business Context:** Customers send emails that automatically create Cases.

**Test Scenario 4.1.1: Sending Email to Create Case**

**Steps:**
1. Send an email to your organization's Email-to-Case address
   - **To:** [Your Email-to-Case address - will be provided]
   - **From:** Your email address
   - **Subject:** "UAT Test Email to Case [Your Name] [Date]"
   - **Body:** "This is a test email to verify Email-to-Case is working"
2. Wait 5 minutes for processing
3. Search for the Case in Salesforce:
   - Go to Cases tab
   - Search for your Subject line

**Expected Outcome:**
- ✅ Case is created from the email within 5 minutes
- ✅ Case Subject matches email Subject
- ✅ Case Description contains email Body text
- ✅ Email message appears in Case Activity/Emails section
- ✅ If you have a Contact record with that email, Case is linked to your Contact

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 4.1.2: Email with Attachment**

**Steps:**
1. Send an email to Email-to-Case address with an attachment (e.g., PDF or image)
2. Wait 5 minutes
3. Find the created Case
4. Check if attachment is visible

**Expected Outcome:**
- ✅ Case created successfully
- ✅ Attachment appears on the Case (in Files or Email section)
- ✅ You can open and view the attachment

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 4.2 Case Comments and Communication

**Test Scenario 4.2.1: Adding a Case Comment**

**Steps:**
1. Open any Case
2. Scroll to **Case Comments** section
3. Click **New Case Comment**
4. Enter comment: "UAT Test Comment [Your Name]"
5. Click **Save**

**Expected Outcome:**
- ✅ Comment saves successfully
- ✅ Comment appears on Case immediately
- ✅ Comment timestamp is correct

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 5. WORK ORDER TESTING

### 5.1 Creating Work Orders

**Business Context:** You create Work Orders for field service activities.

**Test Scenario 5.1.1: New Work Order Creation**

**Steps:**
1. Navigate to **Work Orders** tab
2. Click **New**
3. Fill in required fields:
   - **Subject:** "UAT Test Work Order [Your Name] [Date]"
   - **Case:** Link to a Case (or create one first)
   - **Status:** New
   - **Priority:** Normal
4. Click **Save**
5. Wait 1-2 minutes
6. Refresh the page
7. Check if **Acorn Work Order ID** field is populated (if your work orders sync to Acorn)

**Expected Outcome:**
- ✅ Work Order created successfully
- ✅ Work Order appears in your Work Orders list
- ✅ If applicable, Acorn Work Order ID appears within 2 minutes
- ✅ No errors displayed

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 5.1.2: Work Order Status Change**

**Steps:**
1. Open the Work Order created in 5.1.1
2. Change **Status** to "In Progress"
3. Click **Save**
4. Change **Status** to "Completed"
5. Fill in any required completion fields
6. Click **Save**

**Expected Outcome:**
- ✅ Status changes save successfully
- ✅ Work Order progresses through lifecycle normally
- ✅ Acorn system reflects status changes (if applicable)

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 5.2 Work Order and Case Relationship

**Test Scenario 5.2.1: Work Order Linked to Case**

**Steps:**
1. Create or find a Case
2. Create a Work Order and link it to the Case
3. Save Work Order
4. Go back to the Case
5. Verify Work Order appears in **Related Work Orders** section on Case

**Expected Outcome:**
- ✅ Work Order linked to Case correctly
- ✅ Work Order visible from Case record
- ✅ Relationship works both ways (Case to WO, WO to Case)

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 6. QUOTE AND PRICING TESTING

### 6.1 Quote Creation and Approval

**Business Context:** You create quotes for customers and submit them for approval.

**Test Scenario 6.1.1: Creating a New Quote**

**Steps:**
1. Navigate to **Quotes** tab (or **Opportunities** if your quotes are there)
2. Click **New Quote**
3. Fill in required fields:
   - **Quote Name:** "UAT Test Quote [Your Name] [Date]"
   - **Account:** Select test account
   - **Status:** Draft
4. Add at least one Product/Line Item
5. Click **Save**

**Expected Outcome:**
- ✅ Quote created successfully
- ✅ Quote appears in your Quotes list
- ✅ Status = Draft
- ✅ No errors

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 6.1.2: Quote Approval**

**Steps:**
1. Open the Quote created in 6.1.1
2. Change **Status** to "Approved" (or follow your normal approval process)
3. Click **Save**
4. Wait 2-3 minutes
5. Refresh the page
6. Check **Chatter** feed on Quote - you should see a notification post

**Expected Outcome:**
- ✅ Quote Status changes to Approved
- ✅ Chatter post appears notifying stakeholders
- ✅ If your quotes sync to Acorn for asset creation, verify sync happens within 3 minutes
- ✅ Approval process works identically to before

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 6.1.3: Quote Manual Resync (if applicable)**

**Steps:**
1. Open an existing Approved Quote
2. Find the **Resync to Acorn** checkbox (or similar field)
3. Check the box
4. Click **Save**
5. Wait 1-2 minutes
6. Refresh page
7. Verify checkbox is automatically unchecked

**Expected Outcome:**
- ✅ Quote saves successfully
- ✅ Resync triggered (verify in Acorn if possible)
- ✅ Checkbox automatically unchecked after sync
- ✅ Manual resync works as before

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 7. CONTACT MANAGEMENT TESTING

### 7.1 Contact Updates

**Business Context:** You update Contact information including phone numbers and language preferences.

**Test Scenario 7.1.1: Updating Contact Preferred Language**

**Steps:**
1. Navigate to **Contacts** tab
2. Open a test Contact
3. Click **Edit**
4. Change **Preferred Language** field (e.g., from English to Spanish)
5. Click **Save**
6. Create a new Case for this Contact
7. Check if Case reflects the language preference

**Expected Outcome:**
- ✅ Contact saves successfully
- ✅ Preferred Language updated
- ✅ Related records (Cases) reflect language preference
- ✅ Works same as before

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 7.1.2: Updating Contact Mobile Phone**

**Steps:**
1. Open a test Contact
2. Click **Edit**
3. Change **Mobile Phone** to a new number (e.g., 555-123-4567)
4. Click **Save**
5. Page should save immediately without delays

**Expected Outcome:**
- ✅ Contact saves immediately (no waiting)
- ✅ Mobile Phone updated to new number
- ✅ If your org uses SMS notifications, opt-in status may be updated in background
- ✅ No errors or delays

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 7.2 Contact Communication Preferences

**Test Scenario 7.2.1: Text Notification Opt-In**

**Steps:**
1. Open a Contact with Mobile Phone
2. Check the **Text Notifications Opt-In** field status
3. Change Mobile Phone number
4. Save Contact
5. After 1-2 minutes, check if **Text Notifications Opt-In** status updated

**Expected Outcome:**
- ✅ Contact saves successfully
- ✅ Opt-in status may update after phone change (checks with SMS provider)
- ✅ Process happens in background, doesn't slow you down

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 8. TASK MANAGEMENT TESTING

### 8.1 Task Creation

**Business Context:** You create Tasks for yourself or team members.

**Test Scenario 8.1.1: Creating a Standard Task**

**Steps:**
1. Navigate to **Tasks** tab or create from a Case/Work Order
2. Click **New Task**
3. Fill in:
   - **Subject:** "UAT Test Task [Your Name]"
   - **Status:** Not Started
   - **Priority:** Normal
   - **Assigned To:** Yourself
4. Click **Save**

**Expected Outcome:**
- ✅ Task created successfully
- ✅ Task appears in your Task list
- ✅ No errors

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 8.1.2: Customer Notification Task**

**Steps:**
1. Create a Task
2. Set **Process** field = "Notify Customer Of Service Update" (if this field exists in your org)
3. Set **Attempt** field = 1
4. Click **Save**
5. Immediately view the Task
6. Check **Attempt** field value

**Expected Outcome:**
- ✅ Task saves successfully
- ✅ **Attempt** field automatically updates to 2 (from 1)
- ✅ Task counter works as expected

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

### 8.2 Task Assignment and Routing

**Test Scenario 8.2.1: Task Assignment (Genesys Routing)**

**Steps:**
1. Create a Task that should route to your call center (if applicable)
2. Fill in required routing fields
3. Save Task
4. Check if Task is assigned to appropriate agent/queue

**Expected Outcome:**
- ✅ Task created successfully
- ✅ Task routed to correct queue/agent (visible in Genesys or Salesforce)
- ✅ Routing happens within 1-2 minutes
- ✅ Process works same as before

**Result:** ☐ Pass ☐ Fail
**N/A:** ☐ (check if your org doesn't use task routing)

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 9. BUSINESS RULES TESTING

### 9.1 Business Rule Configuration

**Business Context:** Business Rules are used to configure automated behavior in the system.

**Test Scenario 9.1.1: Creating a Business Rule**

**Steps:**
1. Navigate to **Business Rules** tab
2. Click **New**
3. Fill in:
   - **Name:** "UAT Test Rule [Your Name]"
   - **Active:** Checked
   - **Start Date:** Today
   - **End Date:** Tomorrow
4. Leave **Alias** field BLANK
5. Click **Save**
6. View the saved Business Rule
7. Check **Alias** field

**Expected Outcome:**
- ✅ Business Rule created successfully
- ✅ **Alias** field automatically populated with same value as **Name**
- ✅ Auto-population works as expected

**Result:** ☐ Pass ☐ Fail
**N/A:** ☐ (check if your org doesn't use Business Rules)

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 9.1.2: Business Rule with Channel Requirements**

**Steps:**
1. Open the Business Rule from 9.1.1
2. Click **Edit**
3. Fill in **Channel Requirements** field with any text
4. Click **Save**
5. View the saved Business Rule
6. Check **Is Channel Requirements** checkbox

**Expected Outcome:**
- ✅ Business Rule saves successfully
- ✅ **Is Channel Requirements** checkbox automatically checked
- ✅ Flag set correctly

**Result:** ☐ Pass ☐ Fail
**N/A:** ☐

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 9.1.3: Business Rule with Special Instructions**

**Steps:**
1. Open a Business Rule
2. Click **Edit**
3. Fill in **Special Instructions** field with any text
4. Click **Save**
5. Check **Is Special Instructions** checkbox

**Expected Outcome:**
- ✅ Business Rule saves successfully
- ✅ **Is Special Instructions** checkbox automatically checked

**Result:** ☐ Pass ☐ Fail
**N/A:** ☐

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 9.1.4: Business Rule End Date Validation**

**Steps:**
1. Create a Business Rule
2. Set **Active** = Checked
3. Set **End Date** = Yesterday's date (in the past)
4. Click **Save**
5. View the saved Business Rule
6. Check **Active** checkbox status

**Expected Outcome:**
- ✅ Business Rule saves successfully
- ✅ **Active** checkbox automatically UNCHECKED (because end date is in past)
- ✅ System prevents active rules with past end dates

**Result:** ☐ Pass ☐ Fail
**N/A:** ☐

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 10. GENERAL SYSTEM TESTING

### 10.1 Overall System Performance

**Test Scenario 10.1.1: Page Load Times**

**Steps:**
1. Navigate to different tabs: Cases, Work Orders, Quotes, Contacts
2. Open 5 different records
3. Notice if pages feel slower or faster than usual

**Expected Outcome:**
- ✅ Pages load at normal speed (same or faster than before)
- ✅ No noticeable delays or slowdowns
- ✅ System feels responsive

**Result:** ☐ Pass ☐ Fail

**Notes (if Failed or Slower):**
_________________________________________________________________________
_________________________________________________________________________

---

**Test Scenario 10.1.2: Error Messages**

**Steps:**
1. During all your testing, watch for error messages
2. Note if you see any unexpected errors
3. Compare to your normal experience in production

**Expected Outcome:**
- ✅ No new error messages appear
- ✅ System behaves as it did before
- ✅ Any errors you see are familiar (same as production)

**Result:** ☐ Pass ☐ Fail

**Notes (if any new errors seen):**
_________________________________________________________________________
_________________________________________________________________________

---

### 10.2 Your Daily Workflow

**Test Scenario 10.2.1: Typical Day Simulation**

**Steps:**
1. Perform your most common daily activities in Salesforce:
   - Create the types of Cases you normally create
   - Update records as you normally would
   - Run reports you typically run
   - Complete any other routine tasks
2. Do this for 30-60 minutes as if you're working normally

**Expected Outcome:**
- ✅ All your normal activities work exactly as before
- ✅ No disruption to your workflow
- ✅ Nothing feels different or broken
- ✅ You could do your job with this system

**Result:** ☐ Pass ☐ Fail

**Notes (if anything felt different):**
_________________________________________________________________________
_________________________________________________________________________

---

### 10.3 Integration Verification

**Test Scenario 10.3.1: External System Integration Check**

**Steps:**
1. If you have access to external systems (Acorn, Genesys, etc.):
   - Create a Case in Salesforce that should sync to Acorn
   - Wait 2-3 minutes
   - Check Acorn to verify Case appears there
2. If you don't have access to external systems:
   - Ask your IT team to verify integrations are working

**Expected Outcome:**
- ✅ Data syncs to external systems within 2-3 minutes
- ✅ Same sync speed as before (or faster)
- ✅ No sync failures or delays

**Result:** ☐ Pass ☐ Fail ☐ N/A (no access to external systems)

**Notes (if Failed):**
_________________________________________________________________________
_________________________________________________________________________

---

## 11. FEEDBACK AND ISSUE REPORTING

### 11.1 How to Report Issues

**If You Find a Problem:**

1. **Stop testing that scenario** (don't keep trying)
2. **Take a screenshot** of the error or unexpected behavior
3. **Document the issue:**
   - What were you trying to do?
   - What happened (the problem)?
   - What should have happened?
   - Include the Case/Work Order/Quote number if applicable
4. **Report immediately using one of these methods:**

**Reporting Method 1: Email**
- **To:** [QA Team Email - will be provided]
- **Subject:** UAT Issue - [Brief Description]
- **Body:** Include your documentation and screenshot

**Reporting Method 2: Jira/Issue Tracker**
- **URL:** [Will be provided]
- Create new issue with label "UAT"
- Fill in template fields

**Reporting Method 3: Slack** (if applicable)
- **Channel:** #pbwr-migration-uat
- Post issue with @qa-team tag

### 11.2 Issue Priority Guidelines

**Critical (Report Immediately via Phone):**
- ❗ System is down or completely broken
- ❗ Cannot create Cases, Work Orders, or Quotes at all
- ❗ Data loss or corruption
- ❗ Security issue (seeing data you shouldn't see)

**High (Report within 1 hour via Email/Jira):**
- 🔴 Feature that worked before is now broken
- 🔴 Error messages prevent completing work
- 🔴 Integration not working (Acorn, Genesys)
- 🔴 Performance is significantly slower

**Medium (Report within 4 hours):**
- 🟡 Minor errors that don't block work
- 🟡 Confusing behavior but can work around it
- 🟡 Slight performance difference

**Low (Report by end of day):**
- 🟢 Cosmetic issues (alignment, typos)
- 🟢 Nice-to-have suggestions
- 🟢 Questions about the new system

### 11.3 Getting Help

**If You Need Help During UAT:**

**Question About How to Test:**
- Email: [Project Manager Email]
- Slack: #pbwr-migration-uat

**Technical Issue:**
- Email: [QA Team Email]
- Phone: [QA Team Phone]

**Business Process Question:**
- Contact your supervisor or team lead

**Urgent Issues:**
- Call: [Emergency Contact Number]

---

## 12. UAT SIGN-OFF

### 12.1 Testing Completion Checklist

Before signing off, confirm:

- [ ] I completed all applicable test scenarios in this checklist
- [ ] I tested my daily workflow scenarios for at least 2-4 hours
- [ ] I reported all issues I found
- [ ] All critical and high issues I reported have been resolved
- [ ] I re-tested scenarios that previously failed
- [ ] I am comfortable using this system for my daily work
- [ ] The system works the same as (or better than) the current production system

### 12.2 UAT Feedback Survey

**Overall System Performance:**
☐ Better than before
☐ Same as before (good)
☐ Slightly worse but acceptable
☐ Worse - have concerns

**Ease of Use:**
☐ Easier to use than before
☐ Same ease of use
☐ Slightly harder but manageable
☐ Harder to use - have concerns

**Confidence in Using This System:**
☐ Very confident - ready for production
☐ Confident - ready with minor reservations
☐ Somewhat confident - have concerns
☐ Not confident - need more testing

**Additional Comments:**
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

### 12.3 UAT Sign-Off Form

**I certify that I have completed User Acceptance Testing and:**

☐ **APPROVE** - The system is ready for production deployment

☐ **APPROVE WITH RESERVATIONS** - Ready for production but I have minor concerns (listed below)

☐ **DO NOT APPROVE** - Not ready for production due to issues (listed below)

**Concerns or Issues (if any):**
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

---

**User/Tester Name:** _______________________________________

**Role/Department:** _______________________________________

**Date Completed:** _______________________________________

**Signature:** _______________________________________

---

**Business Owner/Manager Approval:**

**Name:** _______________________________________

**Title:** _______________________________________

**Date:** _______________________________________

**Signature:** _______________________________________

**Comments:**
_________________________________________________________________________
_________________________________________________________________________

---

## APPENDIX A: TEST DATA REFERENCE

### Sample Test Accounts

Use these test accounts for your testing (or create your own):

| Account Name | Type | Status |
|--------------|------|--------|
| Test Account Alpha | Customer | Active |
| Test Account Beta | Customer | Active |
| Test Account Gamma | Prospect | Active |

### Sample Test Contacts

| Contact Name | Email | Phone | Account |
|--------------|-------|-------|---------|
| Test Contact One | test.contact1@example.com | 555-0101 | Test Account Alpha |
| Test Contact Two | test.contact2@example.com | 555-0102 | Test Account Beta |

### Test Email Address

**Email-to-Case Test Address:** [Will be provided by IT team]

---

## APPENDIX B: GLOSSARY FOR BUSINESS USERS

| Term | What It Means |
|------|---------------|
| **Sandbox** | A copy of Salesforce for testing (not the real production system) |
| **Process Builder** | Old technology being replaced (you won't see this anymore) |
| **Workflow Rule** | Old technology being replaced (you won't see this anymore) |
| **Flow** | New technology replacing Process Builders (runs in background) |
| **Acorn** | External system for field service management |
| **Genesys** | External system for call center routing |
| **Integration** | Connection between Salesforce and other systems (like Acorn) |
| **Sync** | When data is sent from Salesforce to another system |
| **Platform Event** | New technology for sending data to external systems (runs in background) |
| **UAT** | User Acceptance Testing (this testing you're doing!) |

---

## APPENDIX C: QUICK REFERENCE - WHAT TO WATCH FOR

**✅ Things That Should Work Exactly the Same:**

- Creating Cases, Work Orders, Quotes
- Changing statuses
- Adding comments
- Sending emails
- Creating tasks
- Updating contacts
- Running reports
- Everything you do every day!

**🔍 Things to Check Specifically:**

- Case Number assignment (automatic)
- Reference Number (should match Case Number)
- Acorn ID fields populate within 2-3 minutes
- Chatter notifications on Quotes
- Email-to-Case creates Cases within 5 minutes
- Task routing to agents (if applicable)
- Business Rule flags set automatically
- No unexpected error messages

**⏱️ Performance Benchmarks:**

- Page loads: Should feel same or faster
- Case creation: Save instantly
- Integration sync: 2-3 minutes max
- Email-to-Case: 5 minutes max

---

**END OF UAT CHECKLIST**

**Thank you for your participation in User Acceptance Testing!**

Your feedback is crucial to ensuring a successful deployment. If you have any questions or concerns at any time, please don't hesitate to reach out to the project team.

---

**Contact Information:**

**Project Manager:** [Name] - [Email] - [Phone]

**QA Lead:** [Name] - [Email] - [Phone]

**Business Owner:** [Name] - [Email] - [Phone]

**IT Support:** [Email] - [Phone]

---

**Document Version:** 1.0
**Last Updated:** January 15, 2026
**Total Test Scenarios:** 30+
**Estimated Testing Time:** 4-8 hours per tester
