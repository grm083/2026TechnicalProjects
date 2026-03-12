# Review: Incorporating User Roles and User Categorization Codes into the Permission Realignment Strategy

**Document Type:** Supplemental Analysis and Review
**Version:** 1.0
**Date:** March 12, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT - Ready for Review
**Related Documents:**
- Permission-Strategy-Analysis.md
- Project-Charter-Profile-Permission-Realignment.md
- SailPoint-Integration-Technical-Design.md
- User-Group-Reference.md

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [User Roles: Current State Analysis](#user-roles-current-state-analysis)
3. [User Categorization Codes: Current State Analysis](#user-categorization-codes-current-state-analysis)
4. [Gap Analysis: What the Existing Documents Miss](#gap-analysis-what-the-existing-documents-miss)
5. [Recommendations](#recommendations)
6. [Updated Architecture Proposal](#updated-architecture-proposal)
7. [Risk Assessment and Migration Concerns](#risk-assessment-and-migration-concerns)
8. [Appendices](#appendices)

---

## Executive Summary

The existing Profiles and Permissions project documentation (Permission Strategy Analysis, Project Charter, and SailPoint Integration Technical Design) proposes a well-structured migration from 17 profiles to a single minimal-access profile with 35 feature-based permission sets organized into 8 persona-based permission set groups. The SailPoint integration design uses `UserRoleId` changes as the trigger for automatic permission set group assignment via a custom metadata mapping (`Role_Permission_Set_Group_Mapping__mdt`).

However, the current analysis does not fully account for two critical elements that are already deeply embedded in the org's operational logic:

1. **User Roles (28 existing roles in a 7-level hierarchy)** - The actual role hierarchy is significantly more granular than the 8 PSG personas proposed. The SailPoint design references simplified role names (e.g., `Customer_Service_Representative`) but the org has 5 distinct CSR sub-roles, regional variants, and a deeply nested hierarchy that controls record-level visibility through OWD sharing.

2. **User_Categorization_Code__c and CSR_User_Data_Setup__mdt** - This is a parallel access-control system that the existing documents do not address at all. There are 31 active categorization codes on the User object that drive Genesys CTI routing, task assignment, team access, validation rules, and quote workflow behavior through custom metadata records. This system acts as a **sub-persona layer** beneath the profile/permission set model and must be preserved or consciously migrated.

**Key Finding:** The permission realignment cannot be treated as a profile-and-permission-set-only exercise. The User Categorization Code system effectively functions as a secondary authorization layer that gates operational behavior at a more granular level than profiles or permission sets can replicate. Any migration plan must account for this or risk breaking existing automation.

---

## User Roles: Current State Analysis

### Role Hierarchy Structure

The org maintains 28 user roles organized into 3 root hierarchies with a maximum depth of 7 levels:

```
SBS_SLT (SBS Leadership)
├── Sales_Director
│   └── Program_Manager
│       └── National_Account_Manager
├── Project_Services_Manager
│   └── Project_Service_Supervisor
│       └── Project_Service_Represenative
├── Customer_Experience_Director
│   ├── CS_Business_Analyst
│   └── Customer_Experience_Manager
│       └── Workforce_Management_Analyst
│           └── Customer_Experience_Supervisor
│               ├── Customer_Experience_Representative
│               ├── Canada_Customer_Service_Representative
│               ├── M_I_Customer_Experience_Representative
│               ├── India_Customer_Experience_Representative
│               └── Customer_Experience_Representative_II
├── Vendor_Relations_Director
│   └── Vendor_Relations_Manager
│       └── Vendor_Relations_Representative
└── Client_Setup_Maintenance_Manager
    └── Client_Setup_Maintenance_Supervisor
        └── Client_Setup_Maintenance_Representative_Representative
            └── Launch_manager
                └── Launch_Supervisor
                    └── Launch_team

System_Administrator (standalone root)

Compliance (standalone root)
```

### Key Observations

#### 1. All roles share identical access level settings
Every role in the hierarchy has:
- `caseAccessLevel: Edit`
- `contactAccessLevel: Edit`
- `opportunityAccessLevel: Edit`
- `mayForecastManagerShare: false`

This means the role hierarchy currently serves primarily as a **record visibility hierarchy** rather than a functional access differentiator. Higher roles in the tree inherit visibility into records owned by subordinate roles.

#### 2. Mismatch between existing roles and proposed PSG personas

The SailPoint Integration Technical Design defines Role_Permission_Set_Group_Mapping__mdt records that reference role developer names like `Customer_Service_Representative`, `Sales_Team_Member`, `Fulfillment_Specialist`, etc. However:

| Proposed PSG Mapping Role | Actual Existing Roles That Map to This Persona |
|---|---|
| `Customer_Service_Representative` | `Customer_Experience_Representative`, `Customer_Experience_Representative_II`, `Canada_Customer_Service_Representative`, `India_Customer_Experience_Representative`, `M_I_Customer_Experience_Representative` |
| `Sales_Team_Member` | `Sales_Director`, `Program_Manager`, `National_Account_Manager` |
| `Fulfillment_Specialist` | `Vendor_Relations_Director`, `Vendor_Relations_Manager`, `Vendor_Relations_Representative`, `Client_Setup_Maintenance_Manager`, `Client_Setup_Maintenance_Supervisor`, `Client_Setup_Maintenance_Representative_Representative` |
| `IT_Support_Member` | No direct role exists (users on Digital Transformation Team profile) |
| `Compliance_Team_Member` | `Compliance` (standalone root) |
| `System_Administrator` | `System_Administrator` (standalone root) |
| `Reporting_Analyst` | `CS_Business_Analyst`, `Workforce_Management_Analyst` |
| `Quality_Assurance_Tester` | No direct role exists |

**Critical Issue:** The Role_Permission_Set_Group_Mapping__mdt records must either:
- (a) Map each actual existing role developer name to a PSG (requiring 28 mapping records, not 8), or
- (b) Restructure the role hierarchy itself to consolidate into the 8 proposed PSG personas

Option (a) is lower risk; option (b) would break record-level sharing rules that depend on the current hierarchy.

#### 3. Regional and specialization variants need consideration

The Customer Experience branch has 5 leaf-level representative roles. These exist for a reason — likely data visibility segmentation (Canada, India, M&I). The current analysis treats all CSRs as a single persona (`PSG_Customer_Service_Representative`), which is correct from a *permission* perspective but does not account for:
- Regional data visibility requirements
- Potential regulatory implications (Canada data residency)
- Different business process requirements by geography

#### 4. Manager/Director roles in the hierarchy

The hierarchy includes Director and Manager-level roles (e.g., `Customer_Experience_Director`, `Vendor_Relations_Director`, `Customer_Experience_Manager`) that serve dual purposes:
- **Record visibility:** These roles see all records owned by subordinates
- **Functional access:** Managers and directors likely need additional capabilities (approval authority, reporting, team management)

The current PSG model does not include a management tier. A `Customer_Experience_Manager` user would receive `PSG_Customer_Service_Representative`, but they likely also need `PS_CPQ_Quote_Approval`, `PS_Reporting_Creator`, or other elevated permissions.

---

## User Categorization Codes: Current State Analysis

### What Is User_Categorization_Code__c?

`User_categorization_code__c` is a **restricted picklist** on the User object with **31 active values**. It acts as a sub-classification of users that drives operational behavior through the `CSR_User_Data_Setup__mdt` custom metadata type.

### Active Categorization Codes (31 values on User object)

| Code | Inferred Meaning | User Group |
|------|-------------------|------------|
| `CSRPR` | CS Representative - Premier | Customer Service |
| `CSRES` | CS Resolution | Customer Service |
| `CSGEN` | CS General | Customer Service |
| `SSMGEN` | SSM General | Fulfillment |
| `SPCOR` | Spec Corrections | Customer Service (specialized) |
| `CSMGR` | CS Manager | Customer Service (leadership) |
| `SALESGEN` | Sales General | Sales |
| `CSCANGEN` | CS Canada General | Customer Service (Canada) |
| `WMCST` | WM Compactor Solutions Team | Customer Service (specialized) |
| `NSQTO` | New Stores - Quote Only | Customer Service (specialized) |
| `CSCANMGR` | CS Canada Manager | Customer Service (Canada leadership) |
| `NSGEN` | New Stores General | Customer Service (specialized) |
| `FASTR` | FAST (Field Service?) Representative | Customer Service (specialized) |
| `CPLGEN` | Compliance General | Compliance |
| `SSMMGR` | SSM Manager | Fulfillment (leadership) |
| `VRGEN` | Vendor Relations General | Fulfillment (VR) |
| `VRMGR` | Vendor Relations Manager | Fulfillment (VR leadership) |
| `SALESPREM` | Sales Premier | Sales (premium accounts) |
| `CSDTRES` | CS DT Resolution | Customer Service (specialized) |
| `VORES` | VO Resolution | Fulfillment (specialized) |
| `VOMAIN` | VO Maintenance | Fulfillment (specialized) |
| `CSOFFGEN` | CS Offline General | Customer Service (offline) |
| `SFNEW` | Service Fulfillment New | Fulfillment (new installs) |
| `SFCHG` | Service Fulfillment Change | Fulfillment (changes) |
| `SFCAN` | Service Fulfillment Cancel | Fulfillment (cancellations) |
| `SFMGR` | Service Fulfillment Manager | Fulfillment (leadership) |
| `PSNEW` | Project Services New | Project Services |
| `SPISC` | Spec/Internal Spec Correction | Specialized |
| `CSSVCL` | CS Service Channel | Customer Service (channel-specific) |
| `CSMONT` | CS Monitoring | Customer Service (monitoring) |
| `CSTRAX` | CS Transaction/Tracking | Customer Service (tracking) |
| `GENDEF` | General Default | Default/unassigned |

### CSR_User_Data_Setup__mdt: The Operational Configuration Layer

This custom metadata type is keyed by the User Categorization Code and stores per-code operational settings:

| Field | Purpose | Impact on Access/Behavior |
|-------|---------|---------------------------|
| `User_categorization_code__c` | Code identifier (matches User field) | Links user to operational config |
| `User_categorization__c` | Human-readable team name | Descriptive grouping |
| `Is_Genesys_User__c` | Whether this code gets Genesys CTI routing | **Controls whether tasks and quotes are routed through Genesys** |
| `GR_Service_Flag__c` | Genesys Routing service flag value | **Determines which Genesys routing queue/service the user is assigned to** |
| `SFDC_Task_User__c` | Whether user receives SFDC task assignments | **Controls task assignment flow behavior** |
| `Team_Acess__c` | Semicolon-delimited list of team names | **Controls which teams/queues the user can access** |
| `SFDC_Team__c` | SFDC team assignment | Team-level routing |
| `SFDC_user_Id__c` | Specific user ID for routing | Direct user routing |
| `Email_Id__c` | Email for routing lookups | Email-based routing resolution |
| `Acorn_Team__c` | Acorn Field Service team | Integration-specific routing |
| `Acorn_Team_Queue__c` | Acorn queue assignment | Integration-specific routing |
| `Team_User_Name__c` | Named user for team routing | Named routing |

### Where User Categorization Code Drives Behavior

Through analysis of the codebase, the User Categorization Code is actively referenced in:

#### Apex Classes (12+ classes)
- **`UserServices.cls`** — Checks UCC against `InternalCorrectionTeamUCC` custom label to determine if user is on the internal corrections team (gates specific case behavior)
- **`HaulAwayService.cls`** — Queries `CSR_User_Data_Setup__mdt` by UCC to determine Genesys eligibility and service flag for haul-away quote routing
- **`CaseTriggerHelper.cls`** — Uses UCC in case assignment and processing logic
- **`TaskTriggerHelper.cls`** — Drives task assignment and routing behavior
- **`QuoteOnlyController.cls`** — UCC-dependent quote creation logic
- **`PricingJSONRequest.cls`** — Includes UCC in pricing API request payloads
- **`PersonalQueueTriggerHelper.cls`** — Queue management based on UCC
- **`MyTaskListController.cls`** — Task list filtering by UCC
- **`IVRUtility.cls`** — IVR integration behavior
- **`GetSFDCServiceFlag.cls`** — Resolves service flag by UCC for integrations
- **`GetCaseInformation.cls`** — Case data retrieval with UCC context
- **`BatchToCreateGenesysForPITasks.cls`** — Batch Genesys routing creation

#### Flows (6+ flows)
- **`Quote_Genesys_Routing_Autoflow`** — Checks UCC to determine Genesys routing eligibility and creates routing records based on `CSR_User_Data_Setup__mdt` config
- **`Task_Assignment`** — Queries `CSR_User_Data_Setup__mdt` by the assigned user's UCC to determine routing
- **`Quote_Assignment_Flow`** — Quote assignment routing decisions
- **`Integration_Task_and_Genesys_Routing`** — Integration task routing
- **`Create_Genesys_Routing`** — Genesys routing record creation
- **`create_Followup_Task_Pending_case_Info`** — Follow-up task creation

#### Validation Rules
- **`Restrict_Next_Task_Date_to_SSMGEN_users`** — Prevents non-SSMGEN users on the Customer Service profile from editing the Next Task Due Date Time field on Tasks with "Future Date Request" outcome. This is a direct example of UCC acting as a **field-level security mechanism** outside of permission sets.

#### Formula Fields
- **`SBQQ__Quote__c.Logged_In_User_Category__c`** — Formula that categorizes the logged-in user based on UCC:
  - `SALESGEN` or `SALESPREM` → "SALES"
  - `SSMGEN` → "SSM"
  - `CSRES` → "SST"
  - All others → "NONE"

  This field is used downstream in quote processing to determine workflow behavior based on user type.

---

## Gap Analysis: What the Existing Documents Miss

### Gap 1: Role Hierarchy Mapping Is Incomplete

**Issue:** The `Role_Permission_Set_Group_Mapping__mdt` design specifies 8 records mapping simplified role names to 8 PSGs. The actual org has 28 roles. The proposed role names (e.g., `Fulfillment_Specialist`) don't match any existing role developer names.

**Impact:** The SailPoint provisioning trigger (`UserTriggerHandler`) will find no mapping match for any existing role, meaning zero automatic PSG assignments will occur for current users.

**Recommendation:** Create mapping records for all 28 existing roles, allowing multiple roles to map to the same PSG. See updated mapping table in Recommendations section.

### Gap 2: User Categorization Code Is Not Addressed

**Issue:** None of the three Profiles and Permissions documents mention `User_categorization_code__c` or `CSR_User_Data_Setup__mdt`. This system is deeply embedded in operational automation.

**Impact:** The permission realignment will not break UCC-driven behavior directly (since UCC operates independently of profiles/permissions), but it represents a missed opportunity to:
- Align UCC with the new permission model
- Reduce parallel access-control systems
- Ensure SailPoint can provision UCC values alongside role and PSG assignments
- Prevent future drift between the permission model and operational routing

### Gap 3: No Management/Leadership Tier in PSG Model

**Issue:** The 5 primary PSGs (CSR, Sales, Fulfillment, IT Support, Compliance) treat all users in a persona as having identical permission needs. The org has distinct Manager and Director roles with different operational requirements.

**Impact:** A `Customer_Experience_Manager` would receive `PSG_Customer_Service_Representative` but may also need approval authority, enhanced reporting, and team management capabilities that the PSG does not include.

### Gap 4: Regional Variants Are Not Considered

**Issue:** Canada, India, and M&I representatives have distinct roles in the hierarchy and distinct UCC codes (`CSCANGEN`, `CSCANMGR`), but the PSG model provides a single `PSG_Customer_Service_Representative`.

**Impact:** While permission-level access may be identical, the lack of recognition in the model means:
- No pathway for region-specific permission variations in the future
- No alignment between regional UCC codes and the PSG model
- Potential confusion during SailPoint provisioning

### Gap 5: Validation Rules Use UCC as Field-Level Security

**Issue:** The `Restrict_Next_Task_Date_to_SSMGEN_users` validation rule uses `User_categorization_code__c` to enforce field-level restrictions that would normally be handled by permission sets. This pattern may exist in other undiscovered validation rules.

**Impact:** If the permission realignment creates new permission sets that grant field edit access (e.g., `PS_Task_Management` includes Edit on Task), but the validation rule still restricts based on UCC, there will be a disconnect between what the permission set allows and what the validation rule enforces. This is not necessarily harmful (defense in depth), but it should be documented and consciously maintained.

### Gap 6: CSR_User_Data_Setup__mdt Only Has 6 Records in Source Control

**Issue:** The codebase contains only 6 `CSR_User_Data_Setup__mdt` records (SALESPREM, WMCST, NSQTO, SPCOR, Internal_Spec_Correction, New_Stores_Quote_Only_Container_on_Site) but there are 31 active UCC codes. The remaining ~25 records likely exist in the org but were not retrieved or are managed in production only.

**Impact:** Any migration plan that involves restructuring CSR_User_Data_Setup__mdt must first perform a complete extraction of all records from production.

---

## Recommendations

### Recommendation 1: Expand Role-to-PSG Mapping to Cover All 28 Roles

Create a comprehensive mapping table that maps every existing role to the appropriate PSG:

| Role Developer Name | PSG Assignment | Notes |
|---|---|---|
| **Customer Experience Branch** | | |
| `Customer_Experience_Representative` | `PSG_Customer_Service_Representative` | Primary CSR role |
| `Customer_Experience_Representative_II` | `PSG_Customer_Service_Representative` | Senior CSR - same PSG |
| `Canada_Customer_Service_Representative` | `PSG_Customer_Service_Representative` | Canada variant - same PSG |
| `India_Customer_Experience_Representative` | `PSG_Customer_Service_Representative` | India variant - same PSG |
| `M_I_Customer_Experience_Representative` | `PSG_Customer_Service_Representative` | M&I variant - same PSG |
| `Customer_Experience_Supervisor` | `PSG_Customer_Service_Representative` + addl PS | See Rec 3 |
| `Workforce_Management_Analyst` | `PSG_Reporting_Analyst` | Primarily analytics |
| `Customer_Experience_Manager` | `PSG_Customer_Service_Representative` + addl PS | See Rec 3 |
| `CS_Business_Analyst` | `PSG_Reporting_Analyst` | Analytics focus |
| `Customer_Experience_Director` | `PSG_Customer_Service_Representative` + addl PS | See Rec 3 |
| **Sales Branch** | | |
| `National_Account_Manager` | `PSG_Sales_Team_Member` | Field sales |
| `Program_Manager` | `PSG_Sales_Team_Member` + addl PS | See Rec 3 |
| `Sales_Director` | `PSG_Sales_Team_Member` + addl PS | See Rec 3 |
| **Vendor Relations Branch** | | |
| `Vendor_Relations_Representative` | `PSG_Fulfillment_Specialist` | VR leaf role |
| `Vendor_Relations_Manager` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| `Vendor_Relations_Director` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| **Client Setup / Launch Branch** | | |
| `Client_Setup_Maintenance_Representative_Representative` | `PSG_Fulfillment_Specialist` | Client setup role |
| `Client_Setup_Maintenance_Supervisor` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| `Client_Setup_Maintenance_Manager` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| `Launch_team` | `PSG_Quality_Assurance_Tester` | Launch/implementation |
| `Launch_Supervisor` | `PSG_Quality_Assurance_Tester` + addl PS | See Rec 3 |
| `Launch_manager` | `PSG_Quality_Assurance_Tester` + addl PS | See Rec 3 |
| **Project Services Branch** | | |
| `Project_Service_Represenative` | `PSG_Fulfillment_Specialist` | Project delivery |
| `Project_Service_Supervisor` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| `Project_Services_Manager` | `PSG_Fulfillment_Specialist` + addl PS | See Rec 3 |
| **Standalone Roots** | | |
| `SBS_SLT` | `PSG_System_Administrator` or custom | Executive leadership |
| `System_Administrator` | `PSG_System_Administrator` | System admin |
| `Compliance` | `PSG_Compliance_Team_Member` | Compliance team |

### Recommendation 2: Create a Leadership/Management Permission Set

Introduce a new permission set `PS_Leadership_Management` to address the management tier gap:

**API Name:** `PS_Leadership_Management`

**Purpose:** Additional capabilities for users in Supervisor, Manager, and Director roles

**Proposed Permissions:**
- `PS_CPQ_Quote_Approval` (approval authority)
- `PS_Reporting_Creator` (enhanced reporting)
- Enhanced visibility on team-owned records
- Access to team performance dashboards
- Ability to reassign records within their team

**Assignment Logic:** The `UserTriggerHandler` should be enhanced to support mapping a role to both a PSG **and** one or more supplemental permission sets. The `Role_Permission_Set_Group_Mapping__mdt` could include a new field `Supplemental_Permission_Sets__c` (comma-separated PS API names) or a separate child metadata type.

### Recommendation 3: Integrate User Categorization Code into SailPoint Provisioning

The SailPoint integration should be expanded to manage `User_categorization_code__c` as a provisioned attribute:

#### 3a. Add UCC to SailPoint Provisioning Payload

Update the `SailPointUserProvisioningService` REST endpoint to accept and set `User_categorization_code__c` during user creation/update:

```
{
  "username": "jdoe@company.com",
  "firstName": "John",
  "lastName": "Doe",
  "roleId": "Customer_Experience_Representative",
  "userCategorizationCode": "CSGEN",    // NEW
  ...
}
```

#### 3b. Create UCC-to-Role Validation Mapping

Create a new custom metadata type or extend `Role_Permission_Set_Group_Mapping__mdt` to include valid UCC codes per role:

| Role | Valid UCC Codes |
|------|----------------|
| `Customer_Experience_Representative` | CSGEN, CSRPR, CSRES, CSDTRES, CSOFFGEN, CSMONT, CSTRAX, WMCST, NSQTO, NSGEN, FASTR, SPCOR, SPISC, GENDEF |
| `Canada_Customer_Service_Representative` | CSCANGEN |
| `Customer_Experience_Supervisor` | CSMGR |
| `Customer_Experience_Manager` | CSMGR, CSCANMGR |
| `National_Account_Manager` | SALESGEN, SALESPREM |
| `Program_Manager` | SALESGEN, SALESPREM |
| `Sales_Director` | SALESGEN, SALESPREM |
| `Vendor_Relations_Representative` | VRGEN, VORES, VOMAIN |
| `Vendor_Relations_Manager` | VRMGR |
| `Client_Setup_Maintenance_Representative_Representative` | SFNEW, SFCHG, SFCAN, SSMGEN |
| `Client_Setup_Maintenance_Supervisor` | SFMGR, SSMMGR |
| `Project_Service_Represenative` | PSNEW |
| `Compliance` | CPLGEN |

This validation ensures that when SailPoint provisions a user with a role and UCC, the combination is valid and the downstream automation (Genesys routing, task assignment, etc.) will function correctly.

#### 3c. Validate CSR_User_Data_Setup__mdt Record Completeness

Before migration, extract all `CSR_User_Data_Setup__mdt` records from production. Ensure every active UCC code has a corresponding metadata record with complete configuration (Is_Genesys_User, GR_Service_Flag, Team_Access, etc.).

### Recommendation 4: Document UCC as a Recognized Access Layer

The Permission Strategy Analysis should be updated to formally recognize the three-plus-one tier model:

```
Tier 1: Minimal Access Profile (base read-only)
    ↓
Tier 2: Permission Set Groups (persona-level functional access)
    ↓
Tier 3: Feature Permission Sets (specific capabilities)
    ↓
Tier 4: User Categorization Code (operational routing and sub-persona behavior)
         ├── Genesys CTI routing eligibility and queue assignment
         ├── Task assignment flow routing
         ├── Quote workflow behavior
         ├── Team/queue access scoping
         └── Validation rule enforcement
```

This makes it explicit that UCC is a recognized and maintained part of the access model, not a legacy artifact to be ignored.

### Recommendation 5: Plan for UCC Consolidation (Future Phase)

In a future phase, evaluate whether UCC functionality can be partially absorbed into the permission set model:

| Current UCC Function | Can Be Migrated to Perm Sets? | Notes |
|---|---|---|
| Genesys CTI routing eligibility | Partially (via PS_Genesys_CTI_User) | The boolean Is_Genesys_User flag could be replaced by PSG membership, but GR_Service_Flag granularity requires UCC |
| Task assignment routing | No | Requires per-user team/queue configuration that is more granular than permission sets |
| Team access scoping | No | Team_Acess__c is a data-driven config, not a permission |
| Validation rule enforcement | Partially | Could be replaced with permission-set-based custom permissions, but requires refactoring validation rules |
| Quote workflow behavior | No | Logged_In_User_Category formula and downstream logic are tightly coupled to UCC values |

**Conclusion:** UCC cannot be fully replaced by permission sets. It serves a different purpose (operational routing configuration vs. security access). The recommended approach is to **maintain UCC as the operational routing layer** and **use permission sets/PSGs for security access**, ensuring both are provisioned together through SailPoint.

---

## Updated Architecture Proposal

### Complete Access Model with All Four Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SailPoint IdentityIQ                            │
│                    (Authoritative IAM System)                           │
│                                                                         │
│  Provisions:                                                            │
│    1. User Record (name, email, etc.)                                   │
│    2. UserRoleId (from 28 existing roles)                               │
│    3. User_categorization_code__c (operational routing code)            │
│    4. IsActive (activation/deactivation)                                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Salesforce Platform                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 1: Minimal Access Profile                                  │   │
│  │ - Single org-wide profile: "Minimal Access - Organization Std"   │   │
│  │ - Read-only base access to core objects                          │   │
│  │ - Applied to ALL users                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 2: Role Hierarchy (28 existing roles)                      │   │
│  │ - Controls record-level visibility (OWD sharing)                 │   │
│  │ - Manager/Director roles inherit subordinate record access       │   │
│  │ - Triggers PSG auto-assignment via UserTriggerHandler            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 3: Permission Set Groups + Permission Sets                 │   │
│  │ - 8 PSGs mapped to role hierarchy via Role_PSG_Mapping__mdt      │   │
│  │ - 35 feature-based permission sets within PSGs                   │   │
│  │ - Supplemental PS for leadership/management roles                │   │
│  │ - Auto-assigned on UserRoleId change                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ LAYER 4: User Categorization Code + CSR_User_Data_Setup__mdt     │   │
│  │ - 31 active UCC codes on User object                             │   │
│  │ - Drives Genesys CTI routing (Is_Genesys_User, GR_Service_Flag) │   │
│  │ - Controls task assignment flow routing                          │   │
│  │ - Scopes team/queue access (Team_Acess__c)                      │   │
│  │ - Enforces field restrictions via validation rules               │   │
│  │ - Shapes quote workflow behavior (Logged_In_User_Category)       │   │
│  │ - Provisioned by SailPoint alongside role assignment             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Updated SailPoint Provisioning Flow

```
1. SailPoint detects new hire or role change in HR system
2. SailPoint calls Salesforce API with:
   - User details (name, email, etc.)
   - Role Developer Name (from 28 existing roles)
   - User Categorization Code (operational sub-classification)    ← NEW
3. SailPointUserProvisioningService:
   a. Creates/updates User record
   b. Sets UserRoleId
   c. Sets User_categorization_code__c                            ← NEW
   d. Validates Role + UCC combination                             ← NEW
   e. Logs to SailPoint_Provisioning_Log__c
4. UserTrigger fires on User insert/update
5. UserTriggerHandler:
   a. Detects UserRoleId change
   b. Queries Role_Permission_Set_Group_Mapping__mdt (28 records)
   c. Assigns PSG
   d. Assigns supplemental permission sets for leadership roles    ← NEW
6. Downstream automation picks up UCC for routing:
   - Genesys routing flows use CSR_User_Data_Setup__mdt
   - Task assignment flows route by UCC team config
   - Quote workflows behave per Logged_In_User_Category formula
```

### Updated Role_Permission_Set_Group_Mapping__mdt Schema

Add the following fields to the existing design:

| Field | Type | Purpose |
|-------|------|---------|
| `Supplemental_Permission_Sets__c` | Text(2000) | Comma-separated API names of additional PS to assign |
| `Valid_User_Categorization_Codes__c` | Text(2000) | Comma-separated valid UCC codes for this role |
| `Is_Leadership_Role__c` | Checkbox | Whether this role receives PS_Leadership_Management |

---

## Risk Assessment and Migration Concerns

### High Risk Items

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Breaking Genesys routing during migration | Medium | High | UCC is independent of profile changes; ensure UCC values are preserved during any user record updates |
| Missing role-to-PSG mapping causes provisioning failures | High | High | Create all 28 mapping records before go-live; test every role in sandbox |
| Validation rules conflict with new permission sets | Low | Medium | Audit all validation rules that reference `$User.User_categorization_code__c` or `$Profile.Name`; update profile references to use custom permissions |
| Incomplete CSR_User_Data_Setup__mdt extraction | Medium | High | Full production extraction required; compare against all 31 active UCC codes |

### Migration Sequence Recommendation

1. **Phase 0 (Pre-migration):**
   - Extract all CSR_User_Data_Setup__mdt records from production
   - Audit all validation rules, formula fields, flows, and Apex that reference UCC
   - Create all 28 Role_Permission_Set_Group_Mapping__mdt records
   - Validate role-to-UCC mapping matrix with business stakeholders

2. **Phase 1 (Profile Consolidation):**
   - Proceed as documented in existing project charter
   - No changes to UCC or role hierarchy
   - Preserve all User_categorization_code__c values during profile migration

3. **Phase 2 (SailPoint Integration):**
   - Include UCC in provisioning payload
   - Implement role-UCC validation
   - Test full provisioning flow with all 28 roles and their valid UCC combinations

4. **Phase 3 (Optimization - Future):**
   - Evaluate which validation rules can be converted to custom permissions
   - Assess whether `$Profile.Name` references in validation rules need updating
   - Consider UCC code consolidation if business processes have simplified

---

## Appendices

### Appendix A: User Categorization Code Cross-Reference

**CSR_User_Data_Setup__mdt field-level comparison (from metadata records in source control):**

| UCC Code | User Categorization Label | Is Genesys User | GR Service Flag | Team Access |
|----------|---------------------------|-----------------|-----------------|-------------|
| NSQTO | New Stores - Quote Only/Container on Site | Yes | NQ | New Stores Team |
| WMCST | WM Compactor Solutions | No | (null) | WM Compactor Solutions Team |
| SPCOR | (Spec Corrections) | No | (null) | Internal Spec Correction Team |
| SALESPREM | SALESPREM | (incomplete record) | (null) | Sales Home Depot Projects; Sales Home Depot Team; Sales Dollar Tree/Family Dollar Team; Sales Amazon Team; Sales M&I Team; Sales Greystar Team; Sales Broker Team |
| Internal_Spec_Correction | Internal Spec Correction | No | (null) | (not set) |

**Note:** Only 6 of ~31 expected records are in source control. Remaining records must be extracted from production.

### Appendix B: CSR_User_Data_Setup__mdt vs Role_Permission_Set_Group_Mapping__mdt Comparison

| Aspect | CSR_User_Data_Setup__mdt | Role_Permission_Set_Group_Mapping__mdt (Proposed) |
|--------|--------------------------|---------------------------------------------------|
| **Purpose** | Operational routing configuration | Security access assignment |
| **Keyed by** | User_categorization_code__c | Role Developer Name |
| **Granularity** | 31 codes (sub-persona level) | 8-28 mappings (persona/role level) |
| **Controls** | Genesys routing, task assignment, team access, validation rules | Permission set group assignment |
| **Provisioning** | Currently manual on User record | Proposed via SailPoint |
| **Can replace the other?** | No — different purposes | No — different purposes |

### Appendix C: Validation Rules Referencing Profile or UCC

Known validation rules that reference `$Profile.Name` or `$User.User_categorization_code__c`:

| Object | Validation Rule | References |
|--------|-----------------|------------|
| Task | `Restrict_Next_Task_Date_to_SSMGEN_users` | `$Profile.Name = "Customer Service"` AND `$User.User_categorization_code__c != "SSMGEN"` |

**Action Required:** A full audit of all validation rules across all objects should be performed to identify any additional rules that reference profile names (which will change during migration) or UCC codes (which should be preserved).

---

**Document Status:** DRAFT
**Next Steps:** Review with George Martin and project stakeholders
**Document Owner:** George Martin, Salesforce Technical Architect

---

**END OF REVIEW DOCUMENT**
