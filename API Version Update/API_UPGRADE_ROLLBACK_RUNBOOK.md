# API UPGRADE ROLLBACK RUNBOOK

**Document Type:** Emergency Rollback Procedures
**Prepared by:** George Martin, Salesforce Technical Architect
**Date:** January 17, 2026
**Version:** 1.0

---

## PURPOSE

This runbook provides step-by-step procedures for rolling back the API version upgrade if critical issues are encountered in production. This document should be readily accessible during and after deployment.

---

## ROLLBACK DECISION CRITERIA

### When to Rollback

Execute rollback if ANY of the following conditions occur:

| Severity | Condition | Response Time | Rollback? |
|----------|-----------|---------------|-----------|
| **P0 - Critical** | Core business process completely broken (case creation, work orders, quotes) | Immediate | YES |
| **P0 - Critical** | Multiple integration failures affecting customers | Within 30 min | YES |
| **P0 - Critical** | Data corruption or loss detected | Immediate | YES |
| **P1 - High** | 2+ high-severity defects discovered within 24 hours | Within 2 hours | YES |
| **P1 - High** | Performance degradation >30% | Within 4 hours | YES |
| **P2 - Medium** | Single high-severity defect with workaround | Next business day | NO - Hotfix |
| **P2 - Medium** | 5+ low-severity defects | Next business day | NO - Hotfix |

### Decision Makers

**Authority to Initiate Rollback:**
1. **Primary:** George Martin (Salesforce Technical Architect)
2. **Backup:** Senior Developer on Call
3. **Emergency:** IT Director

**Notification Required:**
- Project Sponsor
- IT Leadership
- Business Stakeholders
- All Salesforce Users (post-rollback)

---

## PRE-ROLLBACK CHECKLIST

Before initiating rollback, complete this checklist:

- [ ] **Verify Issue Severity:** Confirm issue meets rollback criteria
- [ ] **Document Issue:** Screenshot errors, collect debug logs, note affected records
- [ ] **Notify Decision Makers:** Get approval to proceed with rollback
- [ ] **Assemble Team:** Dev, QA, DevOps available
- [ ] **Verify Backup Availability:** Confirm backup location and integrity
- [ ] **Check Production State:** Document current state for post-mortem
- [ ] **Prepare Communication:** Draft user notification message
- [ ] **Schedule Downtime:** If off-hours rollback, notify security team

**Estimated Time to Complete Rollback:** 30-60 minutes

---

## ROLLBACK PROCEDURE

### Step 1: Stop Any In-Progress Deployment (If Applicable)

If deployment is still in progress:

```bash
# Cancel deployment
sfdx project deploy cancel --target-org Production

# Verify cancellation
sfdx project deploy report --target-org Production
```

**Expected Result:** Deployment status shows "Canceled"

### Step 2: Verify Backup Location

```bash
# List available backups
ls -lh api_upgrade_backup_*/

# Verify backup date matches pre-upgrade
ls -lh api_upgrade_backup_20260117*/default/

# Check backup file count
find api_upgrade_backup_20260117*/default/ -name "*-meta.xml" | wc -l
```

**Expected Result:** Backup folder exists with 1,180+ metadata files

### Step 3: Restore Metadata from Backup

```bash
# Navigate to repository root
cd /home/user/2026TechnicalProjects

# Restore all metadata from backup
cp -r api_upgrade_backup_20260117_*/default/* force-app/main/default/

# Verify restoration
git status
# Should show many modified files with reverted API versions
```

**Expected Result:** Git shows ~1,180 modified metadata XML files

### Step 4: Review Changes

```bash
# Review sample of changes to confirm API versions reverted
git diff force-app/main/default/classes/AccountContactRelationHandler.cls-meta.xml

# Expected: apiVersion changed from 65.0 back to 38.0
```

**Sample Expected Output:**
```diff
-    <apiVersion>65.0</apiVersion>
+    <apiVersion>38.0</apiVersion>
```

### Step 5: Commit Rollback Changes

```bash
# Stage all changes
git add force-app/main/default

# Commit with clear rollback message
git commit -m "ROLLBACK: Revert API version upgrade due to production issues

Reason: [Brief description of issue]
Issue Ticket: [Ticket number if applicable]
Approved by: [Name]
Rollback Date: $(date)

This commit restores all metadata to pre-upgrade API versions:
- Apex classes: Reverted from 65.0 to original versions
- Triggers: Reverted from 65.0 to original versions
- Aura/LWC: Reverted from 65.0 to original versions
- All metadata types restored to pre-upgrade state

Backup used: api_upgrade_backup_20260117_HHMMSS"

# Push to feature branch
git push origin rollback/api-version-emergency
```

### Step 6: Deploy Rollback to Production

**Option A: Quick Deploy (If No Code Changes)**

```bash
# Validate deployment first
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default \
  --dry-run \
  --wait 30

# If validation passes, deploy
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default \
  --wait 30 \
  --test-level NoTestRun
```

**Option B: With Test Execution (Safer)**

```bash
# Deploy with local tests
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default \
  --wait 30 \
  --test-level RunLocalTests
```

**Note:** NoTestRun is acceptable for emergency rollback since we're reverting to known-good state.

**Estimated Deployment Time:** 15-30 minutes

### Step 7: Monitor Deployment

```bash
# Watch deployment status
sfdx project deploy report --target-org Production

# Expected statuses:
# 1. "InProgress" - Deployment running
# 2. "Succeeded" - Deployment complete
```

**If Deployment Fails:**
- Review error messages
- Check for partial deployment success
- Consider metadata-by-metadata rollback (see Step 10)

### Step 8: Verify Rollback Success

```bash
# Query sample class to verify API version reverted
sfdx data query \
  --query "SELECT ApiVersion FROM ApexClass WHERE Name = 'AccountContactRelationHandler'" \
  --target-org Production

# Expected: ApiVersion = 38.0 (original version)
```

**Manual Verification:**
1. Open Salesforce Setup in Production
2. Navigate to: Setup > Apex Classes > AccountContactRelationHandler
3. Click "Version Settings"
4. Verify API Version shows original version (e.g., 38.0)

### Step 9: Smoke Test Production

Execute rapid smoke tests to verify core functionality restored:

#### Test 1: Case Creation (2 minutes)
```
1. Navigate to Cases tab
2. Click "New"
3. Fill in required fields
4. Save
Expected: Case created successfully with no errors
```

#### Test 2: Integration Check (2 minutes)
```
1. Check Integration_Error_Log__c for last 1 hour
2. Query: CreatedDate = LAST_N_HOURS:1
3. Verify no spike in errors
Expected: Error count similar to pre-upgrade baseline
```

#### Test 3: Trigger Execution (2 minutes)
```
1. Update any existing Case record
2. Verify trigger fires without error
3. Check debug logs
Expected: No errors in debug logs
```

#### Test 4: Platform Events (3 minutes)
```
1. Create Case with Integrate_with_Acorn__c = true
2. Check Platform Event monitoring
3. Verify event published
Expected: CaseToAcornEvent__e published successfully
```

**Total Smoke Test Time:** 10 minutes

### Step 10: Alternative - Metadata-by-Metadata Rollback

If full rollback fails, roll back specific metadata types:

```bash
# Rollback Apex Classes only
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default/classes \
  --wait 20

# Rollback Triggers only
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default/triggers \
  --wait 10

# Rollback Aura Components only
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default/aura \
  --wait 15

# Rollback LWC only
sfdx project deploy start \
  --target-org Production \
  --source-dir force-app/main/default/lwc \
  --wait 10
```

---

## POST-ROLLBACK ACTIONS

### Immediate Actions (Within 1 Hour)

1. **Send User Notification**

```
Subject: Salesforce Service Restored - API Upgrade Reverted

Team,

The recent Salesforce API version upgrade has been rolled back due to
[brief issue description]. All functionality has been restored to its
previous state.

Current Status: ✅ RESOLVED
- All systems operational
- No action required from users
- Normal work can resume

The technical team is investigating the root cause. We will communicate
an updated upgrade timeline once the issue is resolved.

If you experience any issues, please contact: [support email/phone]

Thank you for your patience.

George Martin
Salesforce Technical Architect
```

2. **Update Status Page** (if applicable)
   - Status: Resolved
   - Summary: API upgrade rolled back, systems operational

3. **Document Incident**
   - Create incident ticket
   - Attach debug logs
   - Document timeline
   - Note affected users/records

### Within 24 Hours

1. **Root Cause Analysis**
   - Review debug logs
   - Analyze test results
   - Identify specific files/code causing issues
   - Document findings

2. **Post-Mortem Meeting**
   - Attendees: Dev team, QA, stakeholders
   - Review what happened
   - Discuss what went wrong
   - Plan corrective actions

3. **Update Documentation**
   - Document lessons learned
   - Update testing procedures
   - Revise rollout plan
   - Add specific test cases

### Within 1 Week

1. **Fix and Retest**
   - Address root cause issues
   - Update problematic code
   - Create targeted test cases
   - Re-test in sandbox extensively

2. **Prepare for Re-Deployment**
   - Updated rollout plan
   - Enhanced testing checklist
   - Additional safeguards
   - Clear go/no-go criteria

---

## ROLLBACK VERIFICATION CHECKLIST

After rollback completion, verify:

- [ ] **Deployment succeeded** (no errors in deployment log)
- [ ] **API versions reverted** (spot-check 5-10 random files)
- [ ] **Core processes working** (case creation, work orders, quotes)
- [ ] **Integrations functioning** (Acorn, Genesys, Indico)
- [ ] **No spike in errors** (debug logs, integration logs)
- [ ] **Performance normal** (response times similar to baseline)
- [ ] **Users notified** (email sent, status page updated)
- [ ] **Incident documented** (ticket created, logs attached)
- [ ] **Team debriefed** (rollback reason communicated)
- [ ] **Next steps planned** (fix timeline, retest approach)

---

## ROLLBACK TIME ESTIMATES

| Phase | Estimated Time | Notes |
|-------|----------------|-------|
| Decision to rollback | 5-10 min | Severity assessment, approval |
| Prepare rollback | 5 min | Locate backup, stage team |
| Restore from backup | 2-3 min | Copy files from backup |
| Git commit | 2 min | Commit rollback changes |
| Deploy to production | 15-30 min | Metadata deployment |
| Verification | 10-15 min | Smoke tests, spot checks |
| **TOTAL** | **40-65 minutes** | Under 1 hour total |

---

## CONTACT INFORMATION

### Rollback Team

| Role | Name | Phone | Email |
|------|------|-------|-------|
| **Technical Lead** | George Martin | [Phone] | [Email] |
| **Senior Developer** | [Name] | [Phone] | [Email] |
| **QA Lead** | [Name] | [Phone] | [Email] |
| **DevOps Engineer** | [Name] | [Phone] | [Email] |
| **IT Director** | [Name] | [Phone] | [Email] |

### Escalation Path

1. **Level 1:** George Martin (Technical Architect)
2. **Level 2:** IT Director
3. **Level 3:** CTO/VP of Technology

### External Contacts

- **Salesforce Support:** 1-800-NO-SOFTWARE (if platform issue suspected)
- **Acorn Support:** [Contact info]
- **Genesys Support:** [Contact info]

---

## APPENDIX A: Common Rollback Scenarios

### Scenario 1: Apex Test Failures

**Symptoms:**
- Deployment fails due to test failures
- Error: "Test coverage less than 75%"

**Rollback Approach:**
- Full rollback (all metadata)
- Root cause: API version change affected test logic

**Post-Rollback Fix:**
- Update test classes to handle new API behavior
- Add specific test cases for edge conditions

### Scenario 2: Trigger Execution Order Change

**Symptoms:**
- Records not updating as expected
- Debug logs show different trigger execution sequence

**Rollback Approach:**
- Rollback triggers first
- Then rollback related classes

**Post-Rollback Fix:**
- Refactor triggers to be order-independent
- Use TriggerHandler framework bypass flags

### Scenario 3: Platform Event Delivery Issues

**Symptoms:**
- Integration_Error_Log__c shows spike in failures
- External systems not receiving events

**Rollback Approach:**
- Rollback event publishers first
- Monitor for successful delivery

**Post-Rollback Fix:**
- Increase event retry attempts
- Add enhanced logging
- Test event delivery in sandbox

### Scenario 4: Performance Degradation

**Symptoms:**
- Page load times increased >30%
- CPU time limit hits
- Timeout errors

**Rollback Approach:**
- Full rollback
- Capture performance metrics before/after

**Post-Rollback Fix:**
- Optimize SOQL queries
- Review governor limit consumption
- Profile code execution

---

## APPENDIX B: Debug Log Collection

If rollback needed, collect these logs first:

```bash
# Collect Apex debug logs
sfdx data query \
  --query "SELECT Id, Application, DurationMilliseconds, Status, StartTime FROM ApexLog WHERE StartTime = TODAY ORDER BY StartTime DESC LIMIT 100" \
  --target-org Production > apex_logs_before_rollback.txt

# Collect Integration Error Logs
sfdx data query \
  --query "SELECT Id, Integration_Name__c, Status__c, Error_Message__c, Timestamp__c FROM Integration_Error_Log__c WHERE Timestamp__c = LAST_N_HOURS:2 ORDER BY Timestamp__c DESC" \
  --target-org Production > integration_errors_before_rollback.txt

# Export for analysis
echo "Logs collected: $(date)" >> rollback_logs.txt
```

---

## APPENDIX C: Rollback Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│         Is there a critical production issue?                │
└───────────────┬─────────────────────────────────────────────┘
                │
       ┌────────┴────────┐
       │                 │
      YES               NO
       │                 │
       v                 v
┌──────────────┐   ┌──────────────┐
│  P0 Issue?   │   │ Monitor and  │
│ (see table)  │   │  investigate │
└──────┬───────┘   └──────────────┘
       │
       v
┌──────────────────┐
│ Meets rollback   │
│    criteria?     │
└──────┬───────────┘
       │
  ┌────┴────┐
  │         │
 YES       NO
  │         │
  v         v
┌──────────────┐  ┌──────────────┐
│  Notify      │  │  Plan hotfix │
│  decision    │  │  deployment  │
│  makers      │  └──────────────┘
└──────┬───────┘
       │
       v
┌──────────────────┐
│  Get approval    │
└──────┬───────────┘
       │
       v
┌──────────────────┐
│ EXECUTE ROLLBACK │
│  (Steps 1-10)    │
└──────┬───────────┘
       │
       v
┌──────────────────┐
│ Verify success   │
│  Notify users    │
│  Document        │
└──────────────────┘
```

---

## VERSION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 17, 2026 | George Martin | Initial runbook created |

---

**END OF ROLLBACK RUNBOOK**

**Note:** Keep this document accessible during deployment. Print or bookmark for quick reference.
