# Review: Incorporating User Roles and User Categorization Codes into the Permission Realignment Strategy

**Document Type:** Supplemental Analysis and Review
**Version:** 2.0
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
2. [Reframing the Problem: What Each Element Actually Represents](#reframing-the-problem)
3. [User Categorization Codes: The Real Role Definitions](#user-categorization-codes-the-real-role-definitions)
4. [User Roles: Current State and Why They Are Stale](#user-roles-current-state)
5. [The Corrected Architecture: UCC as the Role, Not a Separate Layer](#corrected-architecture)
6. [Proposed Role Hierarchy: One UserRole per UCC](#proposed-role-hierarchy)
7. [UCC-to-PSG Mapping: How Roles Drive Permission Set Groups](#ucc-to-psg-mapping)
8. [CSR_User_Data_Setup__mdt: Operational Configuration per Role](#csr-user-data-setup)
9. [Gap Analysis Against Existing Documentation](#gap-analysis)
10. [Implementation Recommendations](#implementation-recommendations)
11. [Risk Assessment and Migration Concerns](#risk-assessment)
12. [Appendices](#appendices)

---

## Executive Summary

The existing Profiles and Permissions documentation proposes migrating from 17 profiles to a single minimal-access profile with 35 feature-based permission sets organized into 8 persona-based permission set groups (PSGs). The SailPoint integration design uses `UserRoleId` as the trigger for automatic PSG assignment.

This review incorporates two additional elements — **User Roles** and **User_Categorization_Code__c (UCC)** — and arrives at a fundamental reframing of how these pieces relate to one another.

### The Core Insight

The existing documents treat profiles, roles, UCCs, and permission sets as loosely related systems. In reality, they form a clear hierarchy where each element has a specific purpose:

| Element | What It Actually Represents | Analogy |
|---------|----------------------------|---------|
| **Profile** | The department or organizational bucket | "You work in Customer Service" |
| **User Categorization Code (UCC)** | The specific role within that department | "You are a CS Resolution specialist" |
| **UserRole** | Should be the formal Salesforce-recognized role that mirrors UCC | Currently stale; should be rebuilt 1:1 with UCC |
| **Permission Set Group (PSG)** | The collection of system capabilities available to that role | "Here is everything a CS Resolution specialist can do" |
| **Permission Sets** | The individual functional capabilities within a PSG | "Case Management, Quote Read-Only, Task Management, etc." |

### The Key Correction

The original analysis treated UCC as a "parallel access-control system" or "fourth layer" separate from the role hierarchy. **This is wrong.** UCC *is* the role definition. It has been serving that purpose because the UserRole field in Salesforce has gone stale — it doesn't offer much outside of `Intake_Process__c` functionality and is often incorrect.

**The corrected model:** For every UCC record, there should be a corresponding UserRole. They are not separate entities — they are the same concept expressed in two places. When an administrator (or SailPoint) sets a user's UserRole, the system should:

1. Automatically set the corresponding UCC
2. Automatically assign the corresponding PSG
3. The PSG determines what systemic access is available
4. The UCC (via `CSR_User_Data_Setup__mdt`) configures operational routing behavior for that role

---

## Reframing the Problem: What Each Element Actually Represents

### Today's Reality

```
Profile (17 profiles)          → Intended as department-level access
                                  In practice: bloated with embedded permissions,
                                  doing the job of permission sets too

UserRole (28 roles)            → Intended as org hierarchy + record visibility
                                  In practice: stale, often incorrect, only
                                  reliably used for Intake_Process__c

UCC (31 active codes)          → Intended as ???
                                  In practice: THE actual role definition that
                                  drives Genesys routing, task assignment,
                                  quote workflows, validation rules, and
                                  team access — referenced in 12+ Apex classes,
                                  6+ flows, validation rules, and formula fields

Permission Sets (31 existing)  → Intended as feature-level access
                                  In practice: inconsistently built,
                                  no uniform assignment model
```

### The Target State

```
Profile (1 profile)            → "Minimal Access - Organization Standard"
                                  Base read-only access for everyone.
                                  This is your department — everyone is
                                  in the same department from a profile
                                  perspective.

UserRole (rebuilt: 1 per UCC)  → The formal role assignment in Salesforce.
                                  Setting this is THE single action that
                                  cascades everything else.

UCC (1:1 with UserRole)        → Set automatically when UserRole is assigned.
                                  Provides the operational routing config
                                  that makes this role function correctly
                                  (Genesys, task routing, team access, etc.)

PSG (mapped from UserRole)     → Assigned automatically when UserRole is set.
                                  Groups the permission sets that define
                                  what this role can do in the system.

Permission Sets (in PSGs)      → Individual feature capabilities.
                                  Modular, reusable across PSGs.
```

### The Single-Action Provisioning Model

```
Admin/SailPoint sets UserRole = "CS_Resolution_Specialist"
    │
    ├──→ System sets UCC = "CSRES" (via trigger/automation)
    │       └──→ CSR_User_Data_Setup__mdt("CSRES") configures:
    │               - Genesys routing: Yes, flag = "CR"
    │               - Task assignment: Yes
    │               - Team access: "CS Resolution Team"
    │
    └──→ System assigns PSG = "PSG_Customer_Service" (via trigger/automation)
            └──→ PSG contains:
                    - PS_Case_Management
                    - PS_Work_Order_Management
                    - PS_Task_Management
                    - PS_CPQ_Quote_Management
                    - PS_Reporting_User
                    - ... etc.
```

**One action. Everything cascades.**

---

## User Categorization Codes: The Real Role Definitions

### Why UCC Is the Source of Truth for Roles

The UCC system is the most granular, most actively maintained, and most operationally consequential user classification in the org. It is referenced in:

- **12+ Apex classes** including CaseTriggerHelper, HaulAwayService, TaskTriggerHelper, UserServices, PricingJSONRequest, QuoteOnlyController, and more
- **6+ Flows** including Quote_Genesys_Routing_Autoflow, Task_Assignment, Quote_Assignment_Flow, Integration_Task_and_Genesys_Routing, Create_Genesys_Routing, and create_Followup_Task_Pending_case_Info
- **Validation rules** that use UCC as field-level security (e.g., `Restrict_Next_Task_Date_to_SSMGEN_users`)
- **Formula fields** that derive user type from UCC (e.g., `SBQQ__Quote__c.Logged_In_User_Category__c` maps SALESGEN/SALESPREM→"SALES", SSMGEN→"SSM", CSRES→"SST")
- **CSR_User_Data_Setup__mdt** custom metadata records that configure per-role operational behavior

In contrast, the UserRole field is referenced primarily in `Intake_Process__c` functionality and record sharing. It has become stale because it doesn't drive enough behavior to keep it current.

### Complete UCC Inventory (31 Active Codes)

The following table catalogs every active UCC code, its inferred meaning, the department it belongs to, and the PSG it should map to in the new model:

#### Customer Service Department (~15 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `CSGEN` | CS General Representative | Standard front-line customer service agent | Yes (likely) |
| `CSRPR` | CS Premier Representative | Premier/priority customer service agent | Yes (likely) |
| `CSRES` | CS Resolution Specialist | Handles escalated resolution cases | Yes (likely) |
| `CSDTRES` | CS DT Resolution Specialist | Digital transformation resolution team | Yes (likely) |
| `CSOFFGEN` | CS Offline General | Offline/back-office customer service | No |
| `CSMONT` | CS Monitoring Specialist | Monitoring and quality review | No (likely) |
| `CSTRAX` | CS Transaction/Tracking Specialist | Transaction tracking and follow-up | Yes (likely) |
| `CSSVCL` | CS Service Channel Specialist | Channel-specific service handling | Varies |
| `CSCANGEN` | CS Canada General Representative | Canadian market customer service | Yes (likely) |
| `NSGEN` | New Stores General Representative | New store onboarding service | Yes (likely) |
| `NSQTO` | New Stores Quote Only Specialist | Quote-only/container-on-site for new stores | Yes (GR flag: NQ) |
| `WMCST` | WM Compactor Solutions Specialist | WM Compactor Solutions team | No |
| `FASTR` | FAST Representative | FAST (Field Activity Service) representative | Yes (likely) |
| `SPCOR` | Spec Corrections Specialist | Internal specification corrections | No |
| `SPISC` | Internal Spec Correction Specialist | Internal spec correction (alternate code) | No |

#### Customer Service Leadership (~3 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `CSMGR` | CS Manager | Customer service management | No (likely) |
| `CSCANMGR` | CS Canada Manager | Canadian market CS management | No (likely) |
| `GENDEF` | General Default | Default/unassigned — may serve as onboarding placeholder | No |

#### Sales Department (~2 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `SALESGEN` | Sales General Representative | Standard sales team member | No |
| `SALESPREM` | Sales Premier Representative | Premier/national account sales | No |

#### Fulfillment Department - SSM (~2 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `SSMGEN` | SSM General Representative | Service Supply Management agent | Yes (likely) |
| `SSMMGR` | SSM Manager | SSM team management | No (likely) |

#### Fulfillment Department - Vendor Relations (~4 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `VRGEN` | VR General Representative | Vendor relations agent | No (likely) |
| `VRMGR` | VR Manager | Vendor relations management | No (likely) |
| `VORES` | VO Resolution Specialist | Vendor operations resolution | No (likely) |
| `VOMAIN` | VO Maintenance Specialist | Vendor operations maintenance | No (likely) |

#### Fulfillment Department - Service Fulfillment (~4 codes)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `SFNEW` | Service Fulfillment New Installs | New installation fulfillment | No (likely) |
| `SFCHG` | Service Fulfillment Changes | Service change fulfillment | No (likely) |
| `SFCAN` | Service Fulfillment Cancellations | Service cancellation processing | No (likely) |
| `SFMGR` | Service Fulfillment Manager | Service fulfillment management | No (likely) |

#### Other Departments (~1 code)

| UCC Code | Inferred Role Name | Description | Genesys Eligible? |
|----------|-------------------|-------------|-------------------|
| `CPLGEN` | Compliance General | Compliance team member | No |
| `PSNEW` | Project Services New | Project services representative | No (likely) |

**Note:** Genesys eligibility marked as "likely" must be confirmed against complete `CSR_User_Data_Setup__mdt` records from production. Only 6 of ~31 records are currently in source control.

---

## User Roles: Current State and Why They Are Stale

### The Existing 28 Roles

The org currently maintains 28 user roles in a 7-level hierarchy:

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

### Why These Roles Are Stale

1. **They don't drive enough behavior.** Outside of `Intake_Process__c` functionality and OWD record sharing, UserRole has minimal operational impact. UCC took over the role-definition responsibility because it was more actively connected to automation.

2. **They don't match the actual job classifications.** There are 31 UCC codes describing specific job functions, but only 28 roles — and the mapping between them is many-to-one in some cases and nonexistent in others. For example, there is no role for "CS Resolution Specialist" (CSRES), "CS Monitoring Specialist" (CSMONT), or "Service Fulfillment New Installs" (SFNEW).

3. **They are often incorrect.** Because roles don't drive visible behavior for most users, there is limited incentive to keep them current. UCC, by contrast, must be correct or the user's Genesys routing, task assignment, and quote workflows will not function.

4. **All 28 roles share identical access level settings** (`caseAccessLevel: Edit`, `contactAccessLevel: Edit`, `opportunityAccessLevel: Edit`). The hierarchy functions purely as a record visibility tree, not a functional access differentiator.

### What the Roles Do Correctly

Despite being stale, the role hierarchy still provides:
- **Record-level visibility cascading** — Managers and Directors can see records owned by subordinates
- **Reporting hierarchy** — Used in some reporting rollups
- **Intake process routing** — `Intake_Process__c` relies on UserRole

These functions must be preserved in the rebuilt hierarchy.

---

## The Corrected Architecture: UCC as the Role, Not a Separate Layer

### Unified Model

The fundamental correction to the existing documentation is to stop treating UCC, UserRole, and PSG as parallel systems and instead recognize them as a **cascading chain driven by a single assignment action**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  SailPoint IdentityIQ (or Admin Action)                  │
│                                                                         │
│  Single Action: Assign UserRole                                         │
│  Example: UserRole = "CS_Resolution_Specialist"                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Salesforce Platform                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ FOUNDATION: Minimal Access Profile (applied to ALL users)        │   │
│  │ - Single org-wide profile: "Minimal Access - Organization Std"   │   │
│  │ - Read-only base access to core objects                          │   │
│  │ - No embedded feature permissions                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ TRIGGER: UserRole Assignment                                     │   │
│  │ - Admin or SailPoint sets UserRoleId                             │   │
│  │ - UserTrigger fires on User after insert/update                  │   │
│  │ - Queries Role_UCC_PSG_Mapping__mdt for this role                │   │
│  └─────────────────┬─────────────────────┬─────────────────────────┘   │
│                    │                     │                               │
│          ┌─────────▼─────────┐  ┌───────▼──────────────┐               │
│          │ AUTO-SET: UCC     │  │ AUTO-ASSIGN: PSG      │               │
│          │                   │  │                       │               │
│          │ User_categoriza-  │  │ PSG determines what   │               │
│          │ tion_code__c =    │  │ features the role     │               │
│          │ "CSRES"           │  │ can access            │               │
│          │                   │  │                       │               │
│          │ Drives:           │  │ Contains:             │               │
│          │ - Genesys routing │  │ - PS_Case_Management  │               │
│          │ - Task assignment │  │ - PS_Task_Management  │               │
│          │ - Team access     │  │ - PS_CPQ_Quote_Mgmt   │               │
│          │ - Quote workflows │  │ - PS_Reporting_User   │               │
│          │ - Validation rules│  │ - ... etc.            │               │
│          └───────────────────┘  └───────────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### What This Means for the Existing Documentation

| Document | What Changes |
|----------|-------------|
| **Permission-Strategy-Analysis.md** | The 8 PSG model is still valid but the role-to-PSG mapping must be rewritten. Multiple UserRoles (one per UCC) map to the same PSG. PSGs represent departmental access, not individual roles. |
| **Project-Charter-Profile-Permission-Realignment.md** | Scope must expand to include UserRole restructuring and UCC alignment. This is no longer just a profile-and-permission-set project. |
| **SailPoint-Integration-Technical-Design.md** | The provisioning API only needs to accept UserRole. The trigger should set both UCC and PSG. The `Role_Permission_Set_Group_Mapping__mdt` needs a UCC field and must have ~31 records (one per UCC/role), not 8. |

---

## Proposed Role Hierarchy: One UserRole per UCC

### Design Principles

1. **Every active UCC gets a corresponding UserRole.** The role and the UCC are the same concept.
2. **The hierarchy preserves record visibility.** Leadership roles sit above their team's roles so they inherit record access.
3. **Multiple roles share the same PSG.** The PSG represents departmental-level systemic access. All CS roles share `PSG_Customer_Service`; their UCC differentiates their operational behavior.
4. **Role names should be human-readable** and match the actual job function, not cryptic abbreviations.

### Proposed Hierarchy

```
SBS_Leadership                                          [PSG: Executive/Admin]
│
├── Customer_Service_Director                           [PSG: CS + Leadership]
│   ├── CS_Manager (CSMGR)                              [PSG: CS + Leadership]
│   │   ├── CS_General_Representative (CSGEN)            [PSG: CS]
│   │   ├── CS_Premier_Representative (CSRPR)            [PSG: CS]
│   │   ├── CS_Resolution_Specialist (CSRES)             [PSG: CS]
│   │   ├── CS_DT_Resolution_Specialist (CSDTRES)        [PSG: CS]
│   │   ├── CS_Offline_General (CSOFFGEN)                [PSG: CS]
│   │   ├── CS_Monitoring_Specialist (CSMONT)            [PSG: CS]
│   │   ├── CS_Transaction_Tracking (CSTRAX)             [PSG: CS]
│   │   ├── CS_Service_Channel (CSSVCL)                  [PSG: CS]
│   │   ├── FAST_Representative (FASTR)                  [PSG: CS]
│   │   ├── Spec_Corrections_Specialist (SPCOR)          [PSG: CS]
│   │   ├── Internal_Spec_Correction (SPISC)             [PSG: CS]
│   │   ├── New_Stores_General (NSGEN)                   [PSG: CS]
│   │   ├── New_Stores_Quote_Only (NSQTO)                [PSG: CS]
│   │   ├── WM_Compactor_Solutions (WMCST)               [PSG: CS]
│   │   └── General_Default (GENDEF)                     [PSG: CS]
│   │
│   ├── CS_Canada_Manager (CSCANMGR)                     [PSG: CS + Leadership]
│   │   └── CS_Canada_General (CSCANGEN)                 [PSG: CS]
│   │
│   └── CS_Business_Analyst                              [PSG: Reporting]
│       └── Workforce_Management_Analyst                 [PSG: Reporting]
│
├── Sales_Director                                       [PSG: Sales + Leadership]
│   ├── Sales_General_Representative (SALESGEN)          [PSG: Sales]
│   └── Sales_Premier_Representative (SALESPREM)         [PSG: Sales]
│
├── Fulfillment_Director                                 [PSG: Fulfillment + Leadership]
│   ├── SSM_Manager (SSMMGR)                             [PSG: Fulfillment + Leadership]
│   │   └── SSM_General_Representative (SSMGEN)          [PSG: Fulfillment]
│   │
│   ├── VR_Manager (VRMGR)                               [PSG: Fulfillment + Leadership]
│   │   ├── VR_General_Representative (VRGEN)            [PSG: Fulfillment]
│   │   ├── VO_Resolution_Specialist (VORES)             [PSG: Fulfillment]
│   │   └── VO_Maintenance_Specialist (VOMAIN)           [PSG: Fulfillment]
│   │
│   └── SF_Manager (SFMGR)                               [PSG: Fulfillment + Leadership]
│       ├── SF_New_Installs (SFNEW)                      [PSG: Fulfillment]
│       ├── SF_Changes (SFCHG)                           [PSG: Fulfillment]
│       └── SF_Cancellations (SFCAN)                     [PSG: Fulfillment]
│
├── Project_Services_Manager                             [PSG: Fulfillment + Leadership]
│   └── Project_Services_New (PSNEW)                     [PSG: Fulfillment]
│
├── Launch_Manager                                       [PSG: QA/Launch]
│   └── Launch_Team                                      [PSG: QA/Launch]
│
Compliance (standalone root)                             [PSG: Compliance]
│   └── Compliance_General (CPLGEN)                      [PSG: Compliance]
│
System_Administrator (standalone root)                   [PSG: System Admin]
```

### Role Count: ~37 roles (31 UCC-aligned + 6 leadership/structural)

This is an increase from 28, but each role now has a clear purpose and 1:1 relationship with either a UCC code or a structural/leadership function.

---

## UCC-to-PSG Mapping: How Roles Drive Permission Set Groups

### The Mapping Table

Each UserRole maps to exactly one PSG. Multiple roles share the same PSG because the PSG represents departmental access, while the UCC (and thus the role) differentiates operational behavior.

| UserRole (new) | UCC Code | PSG Assignment | Leadership Supplement? |
|---|---|---|---|
| **Customer Service Department** | | | |
| CS_General_Representative | CSGEN | PSG_Customer_Service | No |
| CS_Premier_Representative | CSRPR | PSG_Customer_Service | No |
| CS_Resolution_Specialist | CSRES | PSG_Customer_Service | No |
| CS_DT_Resolution_Specialist | CSDTRES | PSG_Customer_Service | No |
| CS_Offline_General | CSOFFGEN | PSG_Customer_Service | No |
| CS_Monitoring_Specialist | CSMONT | PSG_Customer_Service | No |
| CS_Transaction_Tracking | CSTRAX | PSG_Customer_Service | No |
| CS_Service_Channel | CSSVCL | PSG_Customer_Service | No |
| CS_Canada_General | CSCANGEN | PSG_Customer_Service | No |
| New_Stores_General | NSGEN | PSG_Customer_Service | No |
| New_Stores_Quote_Only | NSQTO | PSG_Customer_Service | No |
| WM_Compactor_Solutions | WMCST | PSG_Customer_Service | No |
| FAST_Representative | FASTR | PSG_Customer_Service | No |
| Spec_Corrections_Specialist | SPCOR | PSG_Customer_Service | No |
| Internal_Spec_Correction | SPISC | PSG_Customer_Service | No |
| General_Default | GENDEF | PSG_Customer_Service | No |
| CS_Manager | CSMGR | PSG_Customer_Service | Yes |
| CS_Canada_Manager | CSCANMGR | PSG_Customer_Service | Yes |
| **Sales Department** | | | |
| Sales_General_Representative | SALESGEN | PSG_Sales | No |
| Sales_Premier_Representative | SALESPREM | PSG_Sales | No |
| Sales_Director | (leadership) | PSG_Sales | Yes |
| **Fulfillment Department** | | | |
| SSM_General_Representative | SSMGEN | PSG_Fulfillment | No |
| SSM_Manager | SSMMGR | PSG_Fulfillment | Yes |
| VR_General_Representative | VRGEN | PSG_Fulfillment | No |
| VR_Manager | VRMGR | PSG_Fulfillment | Yes |
| VO_Resolution_Specialist | VORES | PSG_Fulfillment | No |
| VO_Maintenance_Specialist | VOMAIN | PSG_Fulfillment | No |
| SF_New_Installs | SFNEW | PSG_Fulfillment | No |
| SF_Changes | SFCHG | PSG_Fulfillment | No |
| SF_Cancellations | SFCAN | PSG_Fulfillment | No |
| SF_Manager | SFMGR | PSG_Fulfillment | Yes |
| Project_Services_New | PSNEW | PSG_Fulfillment | No |
| **Compliance Department** | | | |
| Compliance_General | CPLGEN | PSG_Compliance | No |
| **Other** | | | |
| System_Administrator | (admin) | PSG_System_Administrator | N/A |
| CS_Business_Analyst | (analyst) | PSG_Reporting_Analyst | No |
| Workforce_Management_Analyst | (analyst) | PSG_Reporting_Analyst | No |
| Launch_Team | (launch) | PSG_Quality_Assurance | No |

### PSG Summary (unchanged from original analysis, but mapping is now correct)

| PSG | Roles Mapped | Permission Sets Included | Approx. Users |
|-----|-------------|--------------------------|---------------|
| PSG_Customer_Service | 18 roles (16 agent + 2 leadership) | 13 PS (Case, WO, Task, CPQ, Pricing, Asset, Comms, Categorization, Biz Rules, Genesys CTI, MAA, Reporting, Org Mgmt) | ~50 |
| PSG_Sales | 3 roles (2 agent + 1 leadership) | 12 PS (Case, Task, CPQ, CPQ Approval, Pricing, Asset, Approval, Comms, Biz Rules, MAA, Reporting, Org Mgmt) | ~15 |
| PSG_Fulfillment | 12 roles (9 agent + 3 leadership) | 11 PS (CPQ, Pricing, Multi-Vendor, Vendor Mgmt, Task, Asset, WO, Comms, Biz Rules, Reporting, Org Mgmt) | ~10 |
| PSG_Compliance | 1 role | 6 PS (Entitlement, CPQ RO, Approval, Biz Rules, Reporting Creator, Org Mgmt) | 3-5 |
| PSG_IT_Support | (no UCC — retain existing model) | 6 PS (Exception Log, Integration, CPQ RO, Reporting, Project Time, Org Mgmt) | ~5 |
| PSG_System_Administrator | 1 role | 15+ PS (all admin PS) | 2-3 |
| PSG_Reporting_Analyst | 2 roles | 4 PS (Reporting Creator, CPQ RO, Biz Rules, Org Mgmt) | 5-10 |
| PSG_Quality_Assurance | 1 role | 10 PS (broad testing access) | 3-5 |

### Leadership Supplement

Roles flagged with "Leadership Supplement? = Yes" receive the base PSG plus additional permission sets:

- `PS_CPQ_Quote_Approval` (approval authority)
- `PS_Reporting_Creator` (enhanced reporting)
- `PS_Approval_Management` (approval workflow visibility)

This can be implemented as either:
- A separate `PSG_Leadership_Supplement` permission set group, or
- Individual permission set assignments alongside the base PSG, or
- A field on `Role_UCC_PSG_Mapping__mdt` that lists supplemental permission sets

---

## CSR_User_Data_Setup__mdt: Operational Configuration per Role

### Role of CSR_User_Data_Setup__mdt in the Unified Model

In the corrected architecture, `CSR_User_Data_Setup__mdt` is not a separate system — it is the **operational configuration record for each role**. Just as a PSG defines what systemic access a role has, the `CSR_User_Data_Setup__mdt` record defines how the role operates:

| PSG answers... | CSR_User_Data_Setup__mdt answers... |
|---|---|
| Can this role create Cases? | Does this role receive Genesys-routed tasks? |
| Can this role edit Quotes? | Which Genesys routing queue does this role use? |
| Can this role run Reports? | Which teams can this role access? |
| Can this role manage Entitlements? | Does this role appear in SFDC task assignment? |

**They are complementary halves of the same role definition:**
- PSG = security access (what you *can* do)
- CSR_User_Data_Setup__mdt = operational behavior (how the system *treats* you)

### Fields on CSR_User_Data_Setup__mdt

| Field | Type | Purpose |
|-------|------|---------|
| `User_categorization_code__c` | Picklist | Code identifier — the key that links to User.User_categorization_code__c |
| `User_categorization__c` | Picklist | Human-readable role name/team (e.g., "CS Agent", "Sales Premier", "VR Agent") |
| `Is_Genesys_User__c` | Checkbox | Whether this role receives Genesys CTI routing |
| `GR_Service_Flag__c` | Text | Genesys Routing service flag value — determines routing queue |
| `SFDC_Task_User__c` | Checkbox | Whether this role receives SFDC task assignments |
| `Team_Acess__c` | Text | Semicolon-delimited list of team names this role can access |
| `SFDC_Team__c` | Text | SFDC team assignment for this role |
| `SFDC_user_Id__c` | Text | Specific user ID for direct routing |
| `Email_Id__c` | Text | Email address for routing lookups |
| `Acorn_Team__c` | Text | Acorn Field Service team assignment |
| `Acorn_Team_Queue__c` | Text | Acorn queue assignment |
| `Team_User_Name__c` | Text | Named user for team routing |

### Current State: Only 6 of ~31 Records in Source Control

The codebase contains only these CSR_User_Data_Setup__mdt records:

| Record | UCC Code | Key Config |
|--------|----------|-----------|
| NSQTO | NSQTO | Genesys: Yes, Flag: NQ, Team: New Stores Team |
| WMCST | WMCST | Genesys: No, Team: WM Compactor Solutions Team |
| SPCOR | SPCOR | Genesys: No, Team: Internal Spec Correction Team |
| SALESPREM | SALESPREM | Team: Sales Home Depot Projects; Sales Home Depot Team; Sales Dollar Tree/Family Dollar Team; Sales Amazon Team; Sales M&I Team; Sales Greystar Team; Sales Broker Team |
| Internal_Spec_Correction | (internal) | Genesys: No |
| New_Stores_Quote_Only_Container_on_Site | (NSQTO duplicate?) | Related to NSQTO |

**Critical action item:** All remaining ~25 records must be extracted from production before the role restructuring can be completed. Each UCC code needs its operational configuration documented.

---

## Gap Analysis Against Existing Documentation

### Gap 1: The Model Is Inverted

**In the existing docs:** Profile defines the department → PSG defines the persona → UserRole is for record sharing → UCC is not mentioned.

**Corrected model:** Profile provides base access → UserRole defines the specific role (1:1 with UCC) → UserRole triggers PSG assignment AND UCC assignment → PSG defines systemic access, UCC defines operational behavior.

The existing documents get the *pieces* right (minimal profile, feature-based PS, persona-based PSG) but they miss the *glue* — that UserRole should be the single trigger point, and UCC is the role definition that has been doing UserRole's job.

### Gap 2: Role_Permission_Set_Group_Mapping__mdt Needs ~31 Records, Not 8

The SailPoint Technical Design specifies 8 mapping records using fictional role names. The corrected model requires one record per UCC-aligned role (~31 records), each specifying:
- The role developer name
- The corresponding UCC code
- The PSG to assign
- Any supplemental permission sets (for leadership roles)

### Gap 3: The User Trigger Must Set UCC, Not Just PSG

The proposed `UserTriggerHandler` only assigns PSGs on role change. It must also set `User_categorization_code__c` from the mapping metadata. This ensures the UCC is always synchronized with the role.

### Gap 4: Project Scope Must Include Role Restructuring

The Project Charter scopes the work as profile consolidation + permission set creation + SailPoint integration. It must also include:
- Creating ~9 new UserRoles (to get from 28 to ~37, one per UCC)
- Migrating existing users from old roles to new UCC-aligned roles
- Verifying that record sharing still functions correctly after role restructuring

### Gap 5: CSR_User_Data_Setup__mdt Records Are Incomplete in Source Control

Only 6 records exist in the repository. A production extraction and gap analysis is required.

### Gap 6: Validation Rules Reference Profile Names That Will Change

The `Restrict_Next_Task_Date_to_SSMGEN_users` validation rule checks `$Profile.Name = "Customer Service"`. After migrating to a single minimal-access profile, this condition will either always be true (if all users are on the new profile) or never true (if the profile is named differently). All validation rules referencing `$Profile.Name` must be refactored to reference UCC, custom permissions, or PSG membership instead.

---

## Implementation Recommendations

### Phase 0: Discovery and Data Extraction

1. **Extract all CSR_User_Data_Setup__mdt records from production.** Ensure every active UCC code has a complete record with all operational configuration fields populated.
2. **Validate UCC code inventory.** Confirm the 31 active codes on the User object are correct and complete. Identify any codes that are no longer in use.
3. **Audit all references to `$Profile.Name` in validation rules, formula fields, and automation.** These will break when profiles are consolidated and must be refactored.
4. **Map every existing user to their current UCC.** This provides the baseline for role migration.

### Phase 1: Build the New Role Hierarchy

1. **Create new UserRoles** for UCC codes that don't have a corresponding role today (~9 new roles).
2. **Restructure the hierarchy** to follow the proposed tree (see Proposed Role Hierarchy section).
3. **Test record sharing** — verify that managers can still see subordinate records after restructuring.
4. **Preserve the existing hierarchy in parallel** during transition (dual-role period).

### Phase 2: Build the Unified Mapping Metadata

1. **Create `Role_UCC_PSG_Mapping__mdt`** (or extend `Role_Permission_Set_Group_Mapping__mdt`) with ~31 records, one per UCC-aligned role.
2. **Each record specifies:**
   - Role Developer Name
   - UCC Code to auto-set
   - PSG to auto-assign
   - Supplemental Permission Sets (for leadership roles)
   - Active flag and effective dates
3. **Build or update the `UserTriggerHandler`** to set both UCC and PSG on role change.

### Phase 3: Profile Consolidation and Permission Sets (as documented)

Proceed with the existing plan:
1. Create minimal-access profile
2. Create 35 feature-based permission sets
3. Create 8 PSGs
4. Migrate users from old profiles to new profile

### Phase 4: SailPoint Integration

1. SailPoint only needs to set **UserRole** — the Salesforce trigger handles UCC and PSG.
2. Optionally, SailPoint can pass UCC as a validation/override parameter.
3. Provisioning log captures role, UCC, and PSG for audit trail.

### Phase 5: Cutover and Validation

1. Migrate existing users to new roles (batch update UserRoleId).
2. Verify UCC was auto-set correctly for each user.
3. Verify PSG was auto-assigned correctly for each user.
4. Validate Genesys routing still functions.
5. Validate task assignment flows still function.
6. Validate quote workflows still function.
7. Validate all validation rules still enforce correctly (especially those refactored from `$Profile.Name`).

---

## Risk Assessment and Migration Concerns

### Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Role restructuring breaks record sharing | Medium | High | Test in sandbox with production data; map out every OWD and sharing rule dependency |
| Missing CSR_User_Data_Setup__mdt records cause routing failures | High | High | Full production extraction is mandatory Phase 0 work |
| Validation rules that check `$Profile.Name` break after profile consolidation | High | High | Audit and refactor all such rules in Phase 0; convert to UCC or custom permission checks |
| Users assigned to wrong role during migration | Medium | Medium | Batch migration script with validation against current UCC; dry-run before go-live |
| SailPoint provisioning doesn't account for UCC synchronization | Low | Medium | Trigger handles UCC auto-set; SailPoint only needs to set UserRole |
| Genesys routing disrupted during transition | Medium | High | UCC values are preserved even during role changes; test routing end-to-end in sandbox |
| Downstream formula fields (Logged_In_User_Category) break | Low | Medium | No change to UCC values = no change to formula outputs; validate post-migration |

### Key Constraint: UCC Values Must Not Change

The most critical migration constraint is that **User_categorization_code__c values must remain unchanged** for existing users during the transition. The entire operational layer (Genesys, tasks, quotes, validation rules) depends on these values. The role restructuring and PSG assignment happen *around* the UCC — they don't change it.

---

## Appendices

### Appendix A: Where User Categorization Code Is Referenced in Code

#### Apex Classes (12+ classes)

| Class | How UCC Is Used |
|-------|----------------|
| `UserServices.cls` | Checks UCC against `InternalCorrectionTeamUCC` custom label to determine if user is on the internal corrections team |
| `HaulAwayService.cls` | Queries `CSR_User_Data_Setup__mdt` by UCC to determine Genesys eligibility and service flag for haul-away quote routing |
| `CaseTriggerHelper.cls` | Uses UCC in case assignment and processing logic |
| `TaskTriggerHelper.cls` | Drives task assignment and routing behavior |
| `QuoteOnlyController.cls` | UCC-dependent quote creation logic |
| `PricingJSONRequest.cls` | Includes UCC in pricing API request payloads sent to external systems |
| `PersonalQueueTriggerHelper.cls` | Queue management based on UCC |
| `MyTaskListController.cls` | Task list filtering by UCC |
| `IVRUtility.cls` | IVR integration behavior |
| `GetSFDCServiceFlag.cls` | Resolves service flag by UCC for integrations |
| `GetCaseInformation.cls` | Case data retrieval with UCC context |
| `BatchToCreateGenesysForPITasks.cls` | Batch Genesys routing creation |
| `UserSelector.cls` | Queries User by UCC; also queries CSR_User_Data_Setup__mdt by email to resolve UCC config (invocable from flows) |

#### Flows (6+ flows)

| Flow | How UCC Is Used |
|------|----------------|
| `Quote_Genesys_Routing_Autoflow` | Checks assigned user's UCC → looks up CSR_User_Data_Setup__mdt → determines Genesys routing eligibility → creates/deletes Genesys Routing records |
| `Task_Assignment` | Queries CSR_User_Data_Setup__mdt by user's UCC to determine task routing |
| `Quote_Assignment_Flow` | Quote assignment routing decisions based on UCC |
| `Integration_Task_and_Genesys_Routing` | Integration task routing by UCC |
| `Create_Genesys_Routing` | Genesys routing record creation using UCC config |
| `create_Followup_Task_Pending_case_Info` | Follow-up task creation based on UCC |

#### Validation Rules

| Object | Rule | Logic |
|--------|------|-------|
| Task | `Restrict_Next_Task_Date_to_SSMGEN_users` | `$Profile.Name = "Customer Service" AND TEXT($User.User_categorization_code__c) != "SSMGEN"` → Prevents non-SSM users from editing Next Task Due Date Time. **Must refactor `$Profile.Name` check after migration.** |

#### Formula Fields

| Object | Field | Formula Logic |
|--------|-------|--------------|
| SBQQ__Quote__c | `Logged_In_User_Category__c` | SALESGEN or SALESPREM → "SALES"; SSMGEN → "SSM"; CSRES → "SST"; all others → "NONE". Used downstream in quote processing to determine workflow behavior. |

### Appendix B: CSR_User_Data_Setup__mdt vs Proposed Role_UCC_PSG_Mapping__mdt

These are **complementary** metadata types, not competing ones:

| Aspect | CSR_User_Data_Setup__mdt | Role_UCC_PSG_Mapping__mdt |
|--------|--------------------------|---------------------------|
| **Purpose** | Operational config for each role | Security/access assignment for each role |
| **Keyed by** | UCC code (DeveloperName) | Role Developer Name |
| **Contains** | Genesys settings, team access, task routing config | PSG name, UCC code, supplemental PS, active flag |
| **Used by** | Apex classes, flows, validation rules | UserTriggerHandler (auto-assignment) |
| **When queried** | During operational processing (case/task/quote) | During user provisioning (role change) |
| **Relationship** | One record per UCC code | One record per UserRole (which maps 1:1 to a UCC) |

### Appendix C: User_categorization__c (Human-Readable Categories)

The `User_categorization__c` field on `CSR_User_Data_Setup__mdt` provides a human-readable grouping. Active values:

| Category | UCC Codes That Belong |
|----------|----------------------|
| CS Agent | CSGEN, CSRPR, CSRES, CSDTRES, and other CS-prefixed codes |
| CS Leadership | CSMGR |
| Canada CS Agent | CSCANGEN |
| Canada CS Leadership | CSCANMGR |
| Sales Agent | SALESGEN |
| Sales Premier | SALESPREM |
| NS Agent | NSGEN, NSQTO |
| SSM Leadership | SSMMGR |
| VR Agent | VRGEN |
| VR Leadership | VRMGR |
| Compliance Team | CPLGEN |
| Spec Corrections Team | SPCOR, SPISC |
| New Stores - Quote Only/Container on Site | NSQTO |
| WM Compactor Solutions | WMCST |

**Note:** Several additional categories exist as inactive values (Project Services, SSM Team, Service Fulfillment Change Team, Service Fulfillment Leadership, VO Maintenance, VO Resolution, etc.). These likely represent historical categories that were replaced by the current UCC codes.

---

**Document Status:** DRAFT v2.0
**Key Change from v1.0:** Reframed UCC from a "parallel system" to the actual role definition. The corrected model treats UserRole and UCC as 1:1, with UserRole assignment as the single trigger that cascades both PSG assignment and UCC configuration.
**Next Steps:** Review with George Martin and project stakeholders; extract complete CSR_User_Data_Setup__mdt records from production.
**Document Owner:** George Martin, Salesforce Technical Architect

---

**END OF REVIEW DOCUMENT**
