# SailPoint Integration Technical Design Document

**Document Type:** Technical Design Document (TDD)
**Version:** 1.0
**Date:** January 19, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT - Ready for Development
**Target Audience:** Salesforce Developers, Integration Engineers, System Administrators

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-19 | Claude / George Martin | Initial technical design |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Integration Architecture](#integration-architecture)
3. [Data Model](#data-model)
4. [Permission Set Inventory](#permission-set-inventory)
5. [Permission Set Group Inventory](#permission-set-group-inventory)
6. [Custom Metadata Configuration](#custom-metadata-configuration)
7. [API Specifications](#api-specifications)
8. [Automation Implementation](#automation-implementation)
9. [Error Handling and Logging](#error-handling-and-logging)
10. [Security and Authentication](#security-and-authentication)
11. [Testing Strategy](#testing-strategy)
12. [Deployment Guide](#deployment-guide)
13. [Appendices](#appendices)

---

## Executive Summary

### Purpose

This technical design document provides complete implementation specifications for integrating Salesforce with SailPoint IdentityIQ, enabling centralized identity and access management (IAM) for the Salesforce platform.

### Integration Overview

**SailPoint IdentityIQ** will serve as the authoritative source (master) for user provisioning and access control:

1. **SailPoint** creates/updates User records in Salesforce via REST API
2. **SailPoint** assigns UserRoleId to users based on organizational role
3. **Salesforce** automation triggers on UserRoleId assignment/change
4. **Salesforce** automatically assigns Permission Set Groups based on role mapping
5. **Salesforce** sends provisioning status back to SailPoint via callbacks

### Key Components to Build

| Component | Type | Purpose |
|-----------|------|---------|
| `Role_Permission_Set_Group_Mapping__mdt` | Custom Metadata | Role-to-PSG mapping configuration |
| `SailPoint_Provisioning_Log__c` | Custom Object | Audit trail for SailPoint actions |
| `SailPoint_Integration_Setting__c` | Custom Metadata | SailPoint connection settings |
| `SailPointUserProvisioningService` | Apex REST Resource | API endpoint for SailPoint |
| `UserTrigger` | Apex Trigger | User record change detection |
| `UserTriggerHandler` | Apex Class | Trigger handler logic |
| `SailPointProvisioningHelper` | Apex Class | SailPoint-specific provisioning logic |
| `PermissionSetGroupAssignmentService` | Apex Class | PSG assignment service |
| 35 Permission Sets | Permission Set | Feature-based access control |
| 8 Permission Set Groups | Permission Set Group | Persona-based access bundles |

### Development Effort Estimate

| Phase | Effort (Story Points) | Duration |
|-------|----------------------|----------|
| Data Model & Custom Metadata | 8 | 1 week |
| Permission Sets Creation | 21 | 2-3 weeks |
| Permission Set Groups Creation | 8 | 1 week |
| API Development | 13 | 1.5 weeks |
| Automation Logic | 13 | 1.5 weeks |
| Error Handling & Logging | 8 | 1 week |
| Testing & QA | 21 | 2 weeks |
| Documentation & Deployment | 8 | 1 week |
| **TOTAL** | **100 points** | **10-12 weeks** |

---

## Integration Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       SailPoint IdentityIQ                       │
│                  (Authoritative IAM System)                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ REST API (HTTPS)
                            │ - Create User
                            │ - Update User
                            │ - Assign Role
                            │ - Query Provisioning Status
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Salesforce Platform                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  SailPointUserProvisioningService (REST Endpoint)       │    │
│  │  - POST /services/apexrest/sailpoint/provision          │    │
│  │  - POST /services/apexrest/sailpoint/deprovision        │    │
│  │  - GET  /services/apexrest/sailpoint/status/{userId}    │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │          User Record (Standard Object)                  │    │
│  │          - Fields: UserRoleId, IsActive, etc.           │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     │ Trigger Event                              │
│                     ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  UserTrigger → UserTriggerHandler                       │    │
│  │  - Detects UserRoleId changes                           │    │
│  │  - Calls PermissionSetGroupAssignmentService            │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Role_Permission_Set_Group_Mapping__mdt                 │    │
│  │  (Custom Metadata - Configuration)                      │    │
│  │  - Maps Role DeveloperName → PSG API Name              │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  PermissionSetGroupAssignment (Standard Object)         │    │
│  │  - Assigns PSG to User                                  │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     ▼                                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  SailPoint_Provisioning_Log__c                          │    │
│  │  (Audit Trail)                                          │    │
│  └──────────────────┬─────────────────────────────────────┘    │
│                     │                                            │
│                     │ Callback (Optional)                        │
│                     ▼                                            │
└─────────────────────┼─────────────────────────────────────────┘
                      │
                      │ HTTP Callout (Status Update)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│            SailPoint Callback Endpoint (Optional)                │
│            - Receives provisioning status updates                │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Flow

#### Flow 1: User Creation/Update from SailPoint

```
1. SailPoint detects new hire or role change in HR system
2. SailPoint calls Salesforce API: POST /services/apexrest/sailpoint/provision
3. Salesforce receives request with user details and role
4. SailPointUserProvisioningService:
   a. Creates or updates User record
   b. Sets UserRoleId based on role mapping
   c. Creates SailPoint_Provisioning_Log__c record
   d. Returns success/failure status to SailPoint
5. UserTrigger fires on User insert/update
6. UserTriggerHandler detects UserRoleId change
7. PermissionSetGroupAssignmentService:
   a. Queries Role_Permission_Set_Group_Mapping__mdt
   b. Determines which PSG to assign
   c. Removes old PSG assignments (if role changed)
   d. Assigns new PSG
   e. Logs to SailPoint_Provisioning_Log__c
8. (Optional) Salesforce calls back to SailPoint with final status
```

#### Flow 2: User Deprovisioning from SailPoint

```
1. SailPoint detects user termination or role removal
2. SailPoint calls Salesforce API: POST /services/apexrest/sailpoint/deprovision
3. Salesforce receives deprovision request
4. SailPointUserProvisioningService:
   a. Deactivates User (IsActive = false)
   b. Removes all PermissionSetGroupAssignments
   c. Removes all PermissionSetAssignments
   d. Updates UserRoleId to null
   e. Logs to SailPoint_Provisioning_Log__c
   f. Returns success status to SailPoint
```

#### Flow 3: Provisioning Status Query from SailPoint

```
1. SailPoint queries provisioning status
2. SailPoint calls: GET /services/apexrest/sailpoint/status/{userId}
3. Salesforce queries:
   a. User record (IsActive, UserRoleId)
   b. PermissionSetGroupAssignments
   c. Latest SailPoint_Provisioning_Log__c record
4. Salesforce returns JSON with complete provisioning status
```

---

## Data Model

### New Custom Objects

#### 1. SailPoint_Provisioning_Log__c

**Purpose:** Audit trail for all SailPoint provisioning actions

**API Name:** `SailPoint_Provisioning_Log__c`

**Fields:**

| Field Label | API Name | Data Type | Length | Required | Description |
|-------------|----------|-----------|--------|----------|-------------|
| Log Name | Name | Auto Number | - | Yes | Auto-generated: SPL-{0000} |
| User | User__c | Lookup(User) | - | Yes | User being provisioned |
| SailPoint Transaction ID | SailPoint_Transaction_Id__c | Text | 255 | No | SailPoint's transaction identifier |
| Action Type | Action_Type__c | Picklist | - | Yes | Provision, Deprovision, Update, Query |
| Role Assigned | Role_Assigned__c | Lookup(UserRole) | - | No | Role assigned to user |
| Permission Set Groups Assigned | Permission_Set_Groups_Assigned__c | Long Text Area | 32,768 | No | JSON list of PSGs assigned |
| Status | Status__c | Picklist | - | Yes | Success, Failed, In Progress, Rolled Back |
| Error Message | Error_Message__c | Long Text Area | 32,768 | No | Error details if failed |
| Request Payload | Request_Payload__c | Long Text Area | 32,768 | No | JSON of SailPoint request |
| Response Payload | Response_Payload__c | Long Text Area | 32,768 | No | JSON of Salesforce response |
| Processing Time (ms) | Processing_Time_Ms__c | Number(18,0) | - | No | Time taken to process request |
| Source System | Source_System__c | Text | 50 | No | Always "SailPoint" |
| Integration User | Integration_User__c | Lookup(User) | - | No | API user who made the call |
| Callback Sent | Callback_Sent__c | Checkbox | - | No | Whether callback was sent to SailPoint |
| Callback Status | Callback_Status__c | Picklist | - | No | Success, Failed, Not Sent |

**Picklist Values:**

**Action_Type__c:**
- Provision
- Deprovision
- Update
- Role_Change
- Query

**Status__c:**
- Success
- Failed
- In Progress
- Rolled Back
- Partial Success

**Callback_Status__c:**
- Success
- Failed
- Not Sent
- Pending

**Security:**
- OWD: Private
- Access: System Administrators and Integration Users only

**Page Layouts:**
- Standard layout with all fields visible
- Read-only for all users except System Administrators

---

### Custom Metadata Types

#### 1. Role_Permission_Set_Group_Mapping__mdt

**Purpose:** Map Salesforce Roles to Permission Set Groups

**API Name:** `Role_Permission_Set_Group_Mapping__mdt`

**Fields:**

| Field Label | API Name | Data Type | Length | Required | Description |
|-------------|----------|-----------|--------|----------|-------------|
| Label | Label | Text | 40 | Yes | Display name |
| Role_Permission_Set_Group_Mapping Name | DeveloperName | Text | 40 | Yes | API name |
| Role Developer Name | Role_Developer_Name__c | Text | 255 | Yes | DeveloperName of UserRole |
| Permission Set Group Name | Permission_Set_Group_Name__c | Text | 255 | Yes | DeveloperName of PSG |
| Active | Active__c | Checkbox | - | Yes | Whether mapping is active |
| Priority | Priority__c | Number(2,0) | - | No | Priority if multiple mappings (1=highest) |
| Description | Description__c | Long Text Area | 32,768 | No | Business description |
| Effective Date | Effective_Date__c | Date | - | No | When mapping becomes active |
| End Date | End_Date__c | Date | - | No | When mapping expires |
| SailPoint Role Name | SailPoint_Role_Name__c | Text | 255 | No | Role name in SailPoint system |

**Sample Records (to be created):**

```
Label: Customer Service Role Mapping
DeveloperName: Customer_Service_Representative_Mapping
Role_Developer_Name__c: Customer_Service_Representative
Permission_Set_Group_Name__c: PSG_Customer_Service_Representative
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: CS_Representative
```

---

#### 2. SailPoint_Integration_Setting__mdt

**Purpose:** Configuration settings for SailPoint integration

**API Name:** `SailPoint_Integration_Setting__mdt`

**Fields:**

| Field Label | API Name | Data Type | Length | Required | Description |
|-------------|----------|-----------|--------|----------|-------------|
| Label | Label | Text | 40 | Yes | Display name |
| SailPoint_Integration_Setting Name | DeveloperName | Text | 40 | Yes | API name |
| Setting Key | Setting_Key__c | Text | 255 | Yes | Configuration key |
| Setting Value | Setting_Value__c | Text | 255 | No | Configuration value |
| Setting Value Long | Setting_Value_Long__c | Long Text Area | 32,768 | No | Long configuration value |
| Active | Active__c | Checkbox | - | Yes | Whether setting is active |
| Category | Category__c | Picklist | - | Yes | Connection, Security, Callback, Logging |
| Description | Description__c | Long Text Area | 32,768 | No | Description of setting |
| Environment | Environment__c | Picklist | - | No | Production, Sandbox, All |

**Sample Records (to be created):**

```
Label: SailPoint Callback URL
Setting_Key__c: SAILPOINT_CALLBACK_URL
Setting_Value__c: https://sailpoint.example.com/api/provisioning/callback
Category__c: Callback
Environment__c: Production

Label: Enable SailPoint Callbacks
Setting_Key__c: ENABLE_SAILPOINT_CALLBACKS
Setting_Value__c: true
Category__c: Callback
Environment__c: All

Label: SailPoint Timeout (ms)
Setting_Key__c: SAILPOINT_TIMEOUT_MS
Setting_Value__c: 30000
Category__c: Connection
Environment__c: All

Label: Enable Provisioning Logging
Setting_Key__c: ENABLE_PROVISIONING_LOGGING
Setting_Value__c: true
Category__c: Logging
Environment__c: All
```

---

### Standard Object Extensions

#### User Object (Standard)

**New Custom Fields:** None required (uses standard fields)

**Standard Fields Used:**
- UserRoleId (Lookup to UserRole)
- IsActive (Checkbox)
- Username (Text)
- Email (Text)
- FirstName (Text)
- LastName (Text)
- Federation Identifier (FederationIdentifier) - for SSO integration with SailPoint

**Field History Tracking:** Enable on UserRoleId to track role changes

---

## Permission Set Inventory

### Complete List of 35 Permission Sets

This section provides the complete inventory of all permission sets that must be created. Each permission set includes detailed object and field permissions.

---

### Core Service Delivery Permission Sets (7)

#### PS_Case_Management

**API Name:** `PS_Case_Management`

**Description:** Full case lifecycle management including creation, editing, and resolution

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Case | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Case_History_Tracker__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Case_Asset_Header__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Case_Task_Tracker__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Account | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Contact | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All standard and custom fields on Case object

**Apex Class Access:**
- CaseTriggerHandler
- CaseTriggerHelper
- CaseController (all case-related controllers)

**Visualforce Page Access:**
- None (Lightning only)

**Application Permissions:**
- Standard Lightning Service: Visible

**Record Type Access:**
- All Case record types

---

#### PS_Work_Order_Management

**API Name:** `PS_Work_Order_Management`

**Description:** Work order creation, editing, and tracking

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| WorkOrder | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| WorkOrderLineItem | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| ServiceAppointment | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Case | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Asset | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on WorkOrder and WorkOrderLineItem

**Apex Class Access:**
- WorkOrderTriggerHandler
- WorkOrderTriggerHelper
- WorkOrderController (all WO-related controllers)

**Record Type Access:**
- All WorkOrder record types

---

#### PS_Task_Management

**API Name:** `PS_Task_Management`

**Description:** Task creation, assignment, and completion tracking

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Task | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Complete_Task__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Task_Genesys_Routing_Control__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Event | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on Task and Event

**Apex Class Access:**
- TaskTriggerHandler
- TaskTriggerHelper
- OutofOfficeTriggerHelper

---

#### PS_Asset_Management

**API Name:** `PS_Asset_Management`

**Description:** Asset tracking, availability viewing, and case association

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Asset | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| AAV_Asset_Availability__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SBS_Case_Asset__c | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on Asset

**Apex Class Access:**
- AAV_APIIntegration
- AAV_AvailabilityUtility
- AssetTriggerHandler

**Lightning Component Access:**
- aavAlternateContainers
- aavAppOutputPanel
- All AAV-related LWC components

---

#### PS_Entitlement_Management

**API Name:** `PS_Entitlement_Management`

**Description:** Service level agreement and entitlement governance (Compliance Team)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Entitlement | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| ServiceContract | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| sla_calculation__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Account | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Case | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on Entitlement and ServiceContract

**Apex Class Access:**
- Entitlement-related controllers

---

#### PS_Communication_Management

**API Name:** `PS_Communication_Management`

**Description:** Notification preferences and communication channel management

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Account_Notification_Preference__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Contact_Notification_Preference__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Communication_Channel__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Notification_Asset__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Notification_Contact__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SFDCEmailMessage__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on notification objects

---

#### PS_Categorization_Management

**API Name:** `PS_Categorization_Management`

**Description:** Case and issue categorization and disposition

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Categorization__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Category__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Disposition__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on categorization objects

---

### Quote and Pricing Permission Sets (5)

#### PS_CPQ_Quote_Management

**API Name:** `PS_CPQ_Quote_Management`

**Description:** Full quote lifecycle management including creation, editing, and line items

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| SBQQ__Quote__c | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| SBQQ__QuoteLine__c | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| SBQQ__ConfigurationAttribute__c | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| SBQQ__ProductFeature__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SBQQ__ProductOption__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| QuoteApproval__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Quote_Order__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Quote_Line_History_Tracking__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All standard CPQ fields and custom fields on quote objects

**Apex Class Access:**
- All quote-related controllers
- ShowQuoteLineHistoryController
- CPQ-related helpers

**Lightning Component Access:**
- quoteSummaryComp
- pricingOutputScreen
- multiVendorPricingResponse

---

#### PS_CPQ_Quote_Approval

**API Name:** `PS_CPQ_Quote_Approval`

**Description:** Quote approval authority (Sales Team, Management)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| SBQQ__Quote__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| QuoteApproval__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Approval_Log__c | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

**Field Permissions:** Approval-related fields on Quote

**System Permissions:**
- Approve records in approval processes

---

#### PS_CPQ_Read_Only

**API Name:** `PS_CPQ_Read_Only`

**Description:** View-only access to quotes (IT Support, Compliance)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| SBQQ__Quote__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SBQQ__QuoteLine__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| QuoteApproval__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on all quote fields

---

#### PS_Pricing_Access

**API Name:** `PS_Pricing_Access`

**Description:** Pricing request creation and calculation access

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Pricing_Request__c | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Quote_Line_History_Tracking__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on Pricing_Request__c

**Apex Class Access:**
- Pricing-related controllers and helpers

---

#### PS_Multi_Vendor_Pricing

**API Name:** `PS_Multi_Vendor_Pricing`

**Description:** Multi-vendor pricing workflows (Fulfillment Team)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Pricing_Request__c | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Account | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Vendor-related fields on Pricing_Request__c

**Apex Class Access:**
- Multi-vendor pricing controllers

---

### Operational Management Permission Sets (6)

#### PS_Vendor_Management

**API Name:** `PS_Vendor_Management`

**Description:** Vendor relationship management and scorecarding (Fulfillment Team)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Account (Vendor RT) | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| SBS_Supplier_Scorecard__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Contact | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

**Field Permissions:** Vendor-specific fields on Account

**Record Type Access:**
- Vendor record type on Account

**Apex Class Access:**
- VendorEscalationContactController
- Vendor-related helpers

---

#### PS_Approval_Management

**API Name:** `PS_Approval_Management`

**Description:** View and participate in approval workflows

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Approval_Log__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| ApprovalImages__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Service_Approver__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on approval objects

---

#### PS_Approval_Administration

**API Name:** `PS_Approval_Administration`

**Description:** Configure approval routing and approvers (Administrators)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Approval_Log__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Service_Approver__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| ApprovalImages__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on approval objects

---

#### PS_Business_Rules_User

**API Name:** `PS_Business_Rules_User`

**Description:** View business rules (Customer Service, Sales)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Business_Rule__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| STP_Criteria__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on business rule objects

---

#### PS_Business_Rules_Admin

**API Name:** `PS_Business_Rules_Admin`

**Description:** Configure business rules (Administrators)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Business_Rule__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| STP_Criteria__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on business rule objects

**Apex Class Access:**
- BusinessRuleHelper
- BusinessRuleTriggerHandler

---

#### PS_STP_Administration

**API Name:** `PS_STP_Administration`

**Description:** Straight-through processing administration

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| STP_Criteria__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Code_Switch__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** All fields on STP objects

---

### Reporting and Analytics Permission Sets (3)

#### PS_Reporting_User

**API Name:** `PS_Reporting_User`

**Description:** View and run reports (All personas)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Report | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Dashboard | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**System Permissions:**
- Run Reports

**Folder Access:**
- Public reports folders: Read

---

#### PS_Reporting_Creator

**API Name:** `PS_Reporting_Creator`

**Description:** Create custom reports (Reporting Team, Management)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Report | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Dashboard | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |

**System Permissions:**
- Run Reports
- Create and Customize Reports
- Create Dashboard Folders
- Edit My Reports
- Export Reports

**Folder Access:**
- Shared reports folders: Read/Write

---

#### PS_Reporting_Admin

**API Name:** `PS_Reporting_Admin`

**Description:** Full reporting administration (Reporting Team, Administrators)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Report | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Dashboard | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |

**System Permissions:**
- Run Reports
- Create and Customize Reports
- Create Dashboard Folders
- Edit My Reports
- Export Reports
- Manage Reports in Public Folders
- Manage Dashboards in Public Folders

**Folder Access:**
- All folders: Read/Write/Delete

---

### System and Integration Permission Sets (5)

#### PS_Exception_Log_User

**API Name:** `PS_Exception_Log_User`

**Description:** View error logs for troubleshooting (IT Support)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| ExceptionLog__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| System_Log__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| FAST_Activity_Log__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SailPoint_Provisioning_Log__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on all log fields

---

#### PS_Exception_Log_Admin

**API Name:** `PS_Exception_Log_Admin`

**Description:** Configure logging framework (Administrators)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| ExceptionLog__c | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| System_Log__c | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Logging_Framework_Control__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| ExceptionLog_Settings__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| SailPoint_Provisioning_Log__c | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |

**Field Permissions:** All fields on log objects

---

#### PS_Integration_User

**API Name:** `PS_Integration_User`

**Description:** View integration status (Customer Service, IT Support)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Integration_Process_Manager__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Genesys_Routing__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Genesys_Reporting__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on integration objects

---

#### PS_Integration_Admin

**API Name:** `PS_Integration_Admin`

**Description:** Configure integrations (Integration Administrators)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Integration_Process_Manager__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Genesys_Routing__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Genesys_Reporting__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SailPoint_Provisioning_Log__c | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ |

**System Permissions:**
- API Enabled

**Apex Class Access:**
- All integration-related classes
- SailPointUserProvisioningService
- SailPointProvisioningHelper

---

#### PS_Genesys_CTI_User

**API Name:** `PS_Genesys_CTI_User`

**Description:** Genesys contact center access (Customer Service)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Task_Genesys_Routing_Control__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Genesys_Routing__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Genesys_Reporting__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**Field Permissions:** Read-only on Genesys objects

---

### Administrative Permission Sets (5)

#### PS_System_Configuration

**API Name:** `PS_System_Configuration`

**Description:** System configuration (Administrators only)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Code_Switch__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Config_PO__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Data_Store__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| EmailTemplateLogoId__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Max_RecursiveCall__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Object_Save_Mode__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Origin__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| VRBatchSetting__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| MAA_Admin_Settings__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| MAS_Setup_Detail__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Market_Area_Alerts_Settings__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**System Permissions:**
- View Setup and Configuration

**Field Permissions:** All fields on configuration objects

---

#### PS_Market_Area_Alerts_User

**API Name:** `PS_Market_Area_Alerts_User`

**Description:** View and receive market area alerts

**Object Permissions:**

Market area alert objects (Read only)

**Apex Class Access:**
- MarketAreaAlertController (Read)

---

#### PS_Market_Area_Alerts_Admin

**API Name:** `PS_Market_Area_Alerts_Admin`

**Description:** Configure market area alerts (MAA Admin Panel Team)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| MAA_Admin_Settings__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Market_Area_Alerts_Settings__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Apex Class Access:**
- MarketAreaAlertController (Full access)

---

#### PS_Knowledge_Author

**API Name:** `PS_Knowledge_Author`

**Description:** Create and edit knowledge articles (Subject Matter Experts)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Knowledge__kav | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

**System Permissions:**
- Create Articles
- Edit Articles

**Field Permissions:** All fields on Knowledge articles

---

#### PS_Knowledge_Publisher

**API Name:** `PS_Knowledge_Publisher`

**Description:** Publish knowledge articles (Knowledge Managers)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Knowledge__kav | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**System Permissions:**
- Create Articles
- Edit Articles
- Publish Articles
- Manage Article Import and Export
- Manage Knowledge Base

**Field Permissions:** All fields on Knowledge articles

---

### Specialized Functions Permission Sets (4)

#### PS_Project_Time_Tracking

**API Name:** `PS_Project_Time_Tracking`

**Description:** Time tracking for projects (Project Team, IT Support)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Project_Code__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Digital_Transformation_Time_Tracking__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on time tracking objects

---

#### PS_Survey_Management

**API Name:** `PS_Survey_Management`

**Description:** Survey administration (Marketing, Operations)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Survey__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields on Survey__c

---

#### PS_Organizational_Management

**API Name:** `PS_Organizational_Management`

**Description:** Manage personal settings (All users)

**Object Permissions:**

| Object API Name | Create | Read | Edit | Delete | View All | Modify All |
|-----------------|--------|------|------|--------|----------|------------|
| Department__c | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Out_of_Office__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Personal_Queue_Info__c | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |

**Field Permissions:** All fields (with sharing rules limiting to own records)

---

#### PS_Premium_Deliveries

**API Name:** `PS_Premium_Deliveries`

**Description:** Manage premium service delivery (Operations Team)

**Object Permissions:**

Premium delivery objects (CRUD)

**Field Permissions:** All fields on premium delivery objects

---

## Permission Set Group Inventory

### Complete List of 8 Permission Set Groups

This section details all permission set groups and their constituent permission sets.

---

### PSG_Customer_Service_Representative

**API Name:** `PSG_Customer_Service_Representative`

**Target Persona:** Customer Service Representatives (~50 users)

**Description:** Front-line customer service personnel who create and manage cases, work orders, and standard quotes

**Included Permission Sets (13):**

1. `PS_Case_Management`
2. `PS_Work_Order_Management`
3. `PS_Task_Management`
4. `PS_CPQ_Quote_Management`
5. `PS_Pricing_Access`
6. `PS_Asset_Management`
7. `PS_Communication_Management`
8. `PS_Categorization_Management`
9. `PS_Business_Rules_User`
10. `PS_Genesys_CTI_User`
11. `PS_Market_Area_Alerts_User`
12. `PS_Reporting_User`
13. `PS_Organizational_Management`

**SailPoint Role Name:** `CS_Representative`

**UserRole Developer Name:** `Customer_Service_Representative`

---

### PSG_Sales_Team_Member

**API Name:** `PSG_Sales_Team_Member`

**Target Persona:** Sales Team Members (~15 users)

**Description:** Sales personnel with escalation authority, complex quote management, and approval capabilities

**Included Permission Sets (12):**

1. `PS_Case_Management`
2. `PS_Task_Management`
3. `PS_CPQ_Quote_Management`
4. `PS_CPQ_Quote_Approval` ⭐ (Approval authority)
5. `PS_Pricing_Access`
6. `PS_Asset_Management`
7. `PS_Approval_Management`
8. `PS_Communication_Management`
9. `PS_Business_Rules_User`
10. `PS_Market_Area_Alerts_User`
11. `PS_Reporting_User`
12. `PS_Organizational_Management`

**SailPoint Role Name:** `Sales_Team_Member`

**UserRole Developer Name:** `Sales_Team_Member`

---

### PSG_Fulfillment_Specialist

**API Name:** `PSG_Fulfillment_Specialist`

**Target Persona:** Fulfillment Team Members (~10 users)

**Description:** Fulfillment personnel responsible for quote fulfillment, vendor management, and multi-vendor coordination

**Included Permission Sets (11):**

1. `PS_CPQ_Quote_Management`
2. `PS_Pricing_Access`
3. `PS_Multi_Vendor_Pricing` ⭐ (Vendor pricing)
4. `PS_Vendor_Management` ⭐ (Vendor CRUD)
5. `PS_Task_Management`
6. `PS_Asset_Management`
7. `PS_Work_Order_Management`
8. `PS_Communication_Management`
9. `PS_Business_Rules_User`
10. `PS_Reporting_User`
11. `PS_Organizational_Management`

**SailPoint Role Name:** `Fulfillment_Specialist`

**UserRole Developer Name:** `Fulfillment_Specialist`

---

### PSG_IT_Support_Member

**API Name:** `PSG_IT_Support_Member`

**Target Persona:** IT Support Members (~5 users)

**Description:** IT support personnel with read-only production access for troubleshooting and exception analysis

**Included Permission Sets (6):**

1. `PS_Exception_Log_User` ⭐ (Primary function)
2. `PS_Integration_User` ⭐ (Monitor integrations)
3. `PS_CPQ_Read_Only`
4. `PS_Reporting_User`
5. `PS_Project_Time_Tracking`
6. `PS_Organizational_Management`

**SailPoint Role Name:** `IT_Support_Member`

**UserRole Developer Name:** `IT_Support_Member`

**Note:** Base minimal access profile provides read-only to all objects

---

### PSG_Compliance_Team_Member

**API Name:** `PSG_Compliance_Team_Member`

**Target Persona:** Compliance Team Members (3-5 users)

**Description:** Compliance personnel responsible for entitlement governance, SLA management, and SOX audit compliance

**Included Permission Sets (6):**

1. `PS_Entitlement_Management` ⭐ (Primary function)
2. `PS_CPQ_Read_Only`
3. `PS_Approval_Management`
4. `PS_Business_Rules_User`
5. `PS_Reporting_Creator` ⭐ (Compliance reports)
6. `PS_Organizational_Management`

**SailPoint Role Name:** `Compliance_Team_Member`

**UserRole Developer Name:** `Compliance_Team_Member`

---

### PSG_System_Administrator

**API Name:** `PSG_System_Administrator`

**Target Persona:** System Administrators (2-3 users)

**Description:** System administrators with full configuration and administration capabilities

**Included Permission Sets (15+):**

1. `PS_System_Configuration` ⭐
2. `PS_Business_Rules_Admin` ⭐
3. `PS_STP_Administration` ⭐
4. `PS_Approval_Administration` ⭐
5. `PS_Exception_Log_Admin` ⭐
6. `PS_Integration_Admin` ⭐
7. `PS_Market_Area_Alerts_Admin`
8. `PS_Knowledge_Publisher`
9. `PS_Reporting_Admin`
10. `PS_Case_Management`
11. `PS_Work_Order_Management`
12. `PS_CPQ_Quote_Management`
13. `PS_CPQ_Quote_Approval`
14. `PS_Vendor_Management`
15. `PS_Organizational_Management`

**SailPoint Role Name:** `System_Administrator`

**UserRole Developer Name:** `System_Administrator`

**Alternative:** Consider using standard System Administrator profile instead of minimal access + PSG

---

### PSG_Reporting_Analyst

**API Name:** `PSG_Reporting_Analyst`

**Target Persona:** Business Analysts and Reporting Team (5-10 users)

**Description:** Reporting personnel who create custom reports and dashboards for business analysis

**Included Permission Sets (4):**

1. `PS_Reporting_Creator` ⭐ (Primary function)
2. `PS_CPQ_Read_Only`
3. `PS_Business_Rules_User`
4. `PS_Organizational_Management`

**SailPoint Role Name:** `Reporting_Analyst`

**UserRole Developer Name:** `Reporting_Analyst`

---

### PSG_Quality_Assurance_Tester

**API Name:** `PSG_Quality_Assurance_Tester`

**Target Persona:** QA Team (3-5 users)

**Description:** Quality assurance personnel who perform UAT testing across all features

**Included Permission Sets (10):**

1. `PS_Case_Management`
2. `PS_Work_Order_Management`
3. `PS_Task_Management`
4. `PS_CPQ_Quote_Management`
5. `PS_Pricing_Access`
6. `PS_Asset_Management`
7. `PS_Vendor_Management`
8. `PS_Communication_Management`
9. `PS_Reporting_User`
10. `PS_Organizational_Management`

**SailPoint Role Name:** `QA_Tester`

**UserRole Developer Name:** `Quality_Assurance_Tester`

---

## Custom Metadata Configuration

### Role to Permission Set Group Mapping Records

Create the following custom metadata records in `Role_Permission_Set_Group_Mapping__mdt`:

```apex
// Record 1: Customer Service Representative
Label: Customer Service Role Mapping
DeveloperName: Customer_Service_Representative_Mapping
Role_Developer_Name__c: Customer_Service_Representative
Permission_Set_Group_Name__c: PSG_Customer_Service_Representative
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: CS_Representative
Description__c: Maps Customer Service Representative role to CS PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 2: Sales Team Member
Label: Sales Team Member Role Mapping
DeveloperName: Sales_Team_Member_Mapping
Role_Developer_Name__c: Sales_Team_Member
Permission_Set_Group_Name__c: PSG_Sales_Team_Member
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: Sales_Team_Member
Description__c: Maps Sales Team Member role to Sales PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 3: Fulfillment Specialist
Label: Fulfillment Specialist Role Mapping
DeveloperName: Fulfillment_Specialist_Mapping
Role_Developer_Name__c: Fulfillment_Specialist
Permission_Set_Group_Name__c: PSG_Fulfillment_Specialist
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: Fulfillment_Specialist
Description__c: Maps Fulfillment Specialist role to Fulfillment PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 4: IT Support Member
Label: IT Support Member Role Mapping
DeveloperName: IT_Support_Member_Mapping
Role_Developer_Name__c: IT_Support_Member
Permission_Set_Group_Name__c: PSG_IT_Support_Member
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: IT_Support_Member
Description__c: Maps IT Support Member role to IT Support PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 5: Compliance Team Member
Label: Compliance Team Member Role Mapping
DeveloperName: Compliance_Team_Member_Mapping
Role_Developer_Name__c: Compliance_Team_Member
Permission_Set_Group_Name__c: PSG_Compliance_Team_Member
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: Compliance_Team_Member
Description__c: Maps Compliance Team Member role to Compliance PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 6: System Administrator
Label: System Administrator Role Mapping
DeveloperName: System_Administrator_Mapping
Role_Developer_Name__c: System_Administrator
Permission_Set_Group_Name__c: PSG_System_Administrator
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: System_Administrator
Description__c: Maps System Administrator role to Admin PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 7: Reporting Analyst
Label: Reporting Analyst Role Mapping
DeveloperName: Reporting_Analyst_Mapping
Role_Developer_Name__c: Reporting_Analyst
Permission_Set_Group_Name__c: PSG_Reporting_Analyst
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: Reporting_Analyst
Description__c: Maps Reporting Analyst role to Reporting PSG
Effective_Date__c: 2026-02-01
End_Date__c: null

// Record 8: Quality Assurance Tester
Label: QA Tester Role Mapping
DeveloperName: Quality_Assurance_Tester_Mapping
Role_Developer_Name__c: Quality_Assurance_Tester
Permission_Set_Group_Name__c: PSG_Quality_Assurance_Tester
Active__c: true
Priority__c: 1
SailPoint_Role_Name__c: QA_Tester
Description__c: Maps QA Tester role to QA PSG
Effective_Date__c: 2026-02-01
End_Date__c: null
```

### SailPoint Integration Settings

Create the following custom metadata records in `SailPoint_Integration_Setting__mdt`:

```apex
// Connection Settings
Label: SailPoint Callback URL Production
DeveloperName: SAILPOINT_CALLBACK_URL_PROD
Setting_Key__c: SAILPOINT_CALLBACK_URL
Setting_Value__c: https://sailpoint.example.com/api/provisioning/callback
Category__c: Callback
Environment__c: Production
Active__c: true
Description__c: SailPoint callback endpoint for production environment

Label: SailPoint Callback URL Sandbox
DeveloperName: SAILPOINT_CALLBACK_URL_SAND
Setting_Key__c: SAILPOINT_CALLBACK_URL
Setting_Value__c: https://sailpoint-sandbox.example.com/api/provisioning/callback
Category__c: Callback
Environment__c: Sandbox
Active__c: true
Description__c: SailPoint callback endpoint for sandbox environment

// Feature Toggles
Label: Enable SailPoint Callbacks
DeveloperName: ENABLE_SAILPOINT_CALLBACKS
Setting_Key__c: ENABLE_SAILPOINT_CALLBACKS
Setting_Value__c: true
Category__c: Callback
Environment__c: All
Active__c: true
Description__c: Enable or disable SailPoint callbacks

Label: Enable Provisioning Logging
DeveloperName: ENABLE_PROVISIONING_LOGGING
Setting_Key__c: ENABLE_PROVISIONING_LOGGING
Setting_Value__c: true
Category__c: Logging
Environment__c: All
Active__c: true
Description__c: Enable detailed provisioning logging

// Timeout Settings
Label: SailPoint Timeout
DeveloperName: SAILPOINT_TIMEOUT_MS
Setting_Key__c: SAILPOINT_TIMEOUT_MS
Setting_Value__c: 30000
Category__c: Connection
Environment__c: All
Active__c: true
Description__c: Timeout for SailPoint HTTP callouts in milliseconds

// Security Settings
Label: SailPoint API Token
DeveloperName: SAILPOINT_API_TOKEN
Setting_Key__c: SAILPOINT_API_TOKEN
Setting_Value__c: {use Named Credential instead}
Category__c: Security
Environment__c: Production
Active__c: true
Description__c: API token for SailPoint callbacks (use Named Credential)
```

---

## API Specifications

### REST API Endpoints for SailPoint

Create a new Apex REST Resource class to handle SailPoint requests.

#### Endpoint 1: Provision User

**URL:** `/services/apexrest/sailpoint/provision`

**Method:** POST

**Authentication:** OAuth 2.0 or Named Credential

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {access_token}
X-SailPoint-Transaction-ID: {transaction_id}
```

**Request Body:**
```json
{
  "transactionId": "SP-TXN-12345",
  "action": "provision",
  "user": {
    "username": "jdoe@example.com",
    "email": "jdoe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "federationIdentifier": "jdoe",
    "isActive": true,
    "roleName": "CS_Representative",
    "profileName": "Minimal Access - Organization Standard",
    "alias": "jdoe",
    "timeZoneSidKey": "America/New_York",
    "localeSidKey": "en_US",
    "emailEncodingKey": "UTF-8",
    "languageLocaleKey": "en_US"
  }
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "transactionId": "SP-TXN-12345",
  "salesforceUserId": "0051234567890ABCD",
  "username": "jdoe@example.com",
  "roleAssigned": "Customer_Service_Representative",
  "permissionSetGroupsAssigned": [
    "PSG_Customer_Service_Representative"
  ],
  "provisioningLogId": "a001234567890ABCD",
  "message": "User successfully provisioned",
  "processingTimeMs": 1234
}
```

**Response (Error - 400/500):**
```json
{
  "success": false,
  "transactionId": "SP-TXN-12345",
  "errorCode": "DUPLICATE_USERNAME",
  "errorMessage": "A user with username jdoe@example.com already exists",
  "provisioningLogId": "a001234567890ABCD",
  "processingTimeMs": 456
}
```

---

#### Endpoint 2: Deprovision User

**URL:** `/services/apexrest/sailpoint/deprovision`

**Method:** POST

**Request Body:**
```json
{
  "transactionId": "SP-TXN-12346",
  "action": "deprovision",
  "username": "jdoe@example.com",
  "reason": "User terminated"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "transactionId": "SP-TXN-12346",
  "salesforceUserId": "0051234567890ABCD",
  "username": "jdoe@example.com",
  "userDeactivated": true,
  "permissionSetGroupsRemoved": [
    "PSG_Customer_Service_Representative"
  ],
  "provisioningLogId": "a001234567890ABCE",
  "message": "User successfully deprovisioned",
  "processingTimeMs": 987
}
```

---

#### Endpoint 3: Update User Role

**URL:** `/services/apexrest/sailpoint/provision`

**Method:** POST

**Request Body:**
```json
{
  "transactionId": "SP-TXN-12347",
  "action": "update",
  "user": {
    "username": "jdoe@example.com",
    "roleName": "Sales_Team_Member"
  }
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "transactionId": "SP-TXN-12347",
  "salesforceUserId": "0051234567890ABCD",
  "username": "jdoe@example.com",
  "previousRole": "Customer_Service_Representative",
  "newRole": "Sales_Team_Member",
  "permissionSetGroupsRemoved": [
    "PSG_Customer_Service_Representative"
  ],
  "permissionSetGroupsAssigned": [
    "PSG_Sales_Team_Member"
  ],
  "provisioningLogId": "a001234567890ABCF",
  "message": "User role successfully updated",
  "processingTimeMs": 1456
}
```

---

#### Endpoint 4: Query Provisioning Status

**URL:** `/services/apexrest/sailpoint/status/{username}`

**Method:** GET

**Request:** No body (username in URL)

**Response (Success - 200):**
```json
{
  "success": true,
  "salesforceUserId": "0051234567890ABCD",
  "username": "jdoe@example.com",
  "email": "jdoe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isActive": true,
  "userRoleId": "00E1234567890ABCD",
  "userRoleName": "Sales_Team_Member",
  "profileName": "Minimal Access - Organization Standard",
  "permissionSetGroups": [
    {
      "id": "0PG1234567890ABCD",
      "developerName": "PSG_Sales_Team_Member",
      "label": "Sales Team Member",
      "assignedDate": "2026-01-19T10:30:00.000Z"
    }
  ],
  "lastProvisioningAction": {
    "id": "a001234567890ABCF",
    "transactionId": "SP-TXN-12347",
    "actionType": "Update",
    "status": "Success",
    "createdDate": "2026-01-19T10:30:00.000Z"
  }
}
```

---

### SailPoint Callback API

Salesforce will call back to SailPoint after provisioning actions complete.

**URL:** (Configured in `SailPoint_Integration_Setting__mdt`)

**Method:** POST

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {token from Named Credential}
```

**Request Body:**
```json
{
  "transactionId": "SP-TXN-12345",
  "salesforceUserId": "0051234567890ABCD",
  "username": "jdoe@example.com",
  "action": "provision",
  "status": "success",
  "timestamp": "2026-01-19T10:30:00.000Z",
  "message": "User successfully provisioned with PSG_Customer_Service_Representative"
}
```

---

## Automation Implementation

### Complete Code Implementation

This section provides production-ready code for developers to implement.

---

### 1. Apex REST Resource: SailPointUserProvisioningService

**File:** `force-app/main/default/classes/SailPointUserProvisioningService.cls`

```apex
/**
 * @description REST API endpoint for SailPoint user provisioning
 * @author Development Team
 * @date 2026-01-19
 */
@RestResource(urlMapping='/sailpoint/*')
global with sharing class SailPointUserProvisioningService {

    /**
     * @description Provision or update user from SailPoint
     * @return ProvisioningResponse
     */
    @HttpPost
    global static ProvisioningResponse provisionUser() {
        Long startTime = System.currentTimeMillis();
        ProvisioningRequest req;
        ProvisioningResponse res = new ProvisioningResponse();

        try {
            // Parse request
            String requestBody = RestContext.request.requestBody.toString();
            req = (ProvisioningRequest) JSON.deserialize(requestBody, ProvisioningRequest.class);

            // Validate request
            if (req == null || req.user == null) {
                return createErrorResponse('Invalid request body', 'INVALID_REQUEST', null, startTime);
            }

            // Determine action
            if (req.action == 'provision') {
                res = handleProvision(req, requestBody, startTime);
            } else if (req.action == 'update') {
                res = handleUpdate(req, requestBody, startTime);
            } else if (req.action == 'deprovision') {
                res = handleDeprovision(req, requestBody, startTime);
            } else {
                res = createErrorResponse('Invalid action: ' + req.action, 'INVALID_ACTION', req.transactionId, startTime);
            }

        } catch (Exception e) {
            res = createErrorResponse(e.getMessage(), 'EXCEPTION', req?.transactionId, startTime);

            // Log exception
            SailPointProvisioningHelper.logException(e, req);
        }

        // Set HTTP status code
        RestContext.response.statusCode = res.success ? 200 : 400;

        return res;
    }

    /**
     * @description Query provisioning status
     * @return StatusResponse
     */
    @HttpGet
    global static StatusResponse getProvisioningStatus() {
        String username = RestContext.request.requestURI.substring(
            RestContext.request.requestURI.lastIndexOf('/') + 1
        );

        try {
            User u = [
                SELECT Id, Username, Email, FirstName, LastName, IsActive,
                       UserRoleId, UserRole.Name, UserRole.DeveloperName,
                       Profile.Name, FederationIdentifier
                FROM User
                WHERE Username = :username
                LIMIT 1
            ];

            // Query permission set groups
            List<PermissionSetGroupInfo> psgList = new List<PermissionSetGroupInfo>();
            for (PermissionSetAssignment psa : [
                SELECT PermissionSetGroup.Id, PermissionSetGroup.DeveloperName,
                       PermissionSetGroup.Label, CreatedDate
                FROM PermissionSetAssignment
                WHERE AssigneeId = :u.Id
                AND PermissionSetGroupId != null
            ]) {
                psgList.add(new PermissionSetGroupInfo(
                    psa.PermissionSetGroup.Id,
                    psa.PermissionSetGroup.DeveloperName,
                    psa.PermissionSetGroup.Label,
                    psa.CreatedDate
                ));
            }

            // Query last provisioning action
            SailPoint_Provisioning_Log__c lastLog = [
                SELECT Id, SailPoint_Transaction_Id__c, Action_Type__c,
                       Status__c, CreatedDate
                FROM SailPoint_Provisioning_Log__c
                WHERE User__c = :u.Id
                ORDER BY CreatedDate DESC
                LIMIT 1
            ];

            StatusResponse res = new StatusResponse();
            res.success = true;
            res.salesforceUserId = u.Id;
            res.username = u.Username;
            res.email = u.Email;
            res.firstName = u.FirstName;
            res.lastName = u.LastName;
            res.isActive = u.IsActive;
            res.userRoleId = u.UserRoleId;
            res.userRoleName = u.UserRole?.Name;
            res.profileName = u.Profile.Name;
            res.permissionSetGroups = psgList;
            res.lastProvisioningAction = lastLog != null ? new LastProvisioningAction(
                lastLog.Id,
                lastLog.SailPoint_Transaction_Id__c,
                lastLog.Action_Type__c,
                lastLog.Status__c,
                lastLog.CreatedDate
            ) : null;

            RestContext.response.statusCode = 200;
            return res;

        } catch (QueryException e) {
            StatusResponse res = new StatusResponse();
            res.success = false;
            res.errorCode = 'USER_NOT_FOUND';
            res.errorMessage = 'User not found: ' + username;
            RestContext.response.statusCode = 404;
            return res;
        }
    }

    /**
     * @description Handle provision action (create new user)
     */
    private static ProvisioningResponse handleProvision(ProvisioningRequest req, String requestBody, Long startTime) {
        ProvisioningResponse res = new ProvisioningResponse();

        try {
            // Check if user already exists
            List<User> existingUsers = [
                SELECT Id, Username
                FROM User
                WHERE Username = :req.user.username
                LIMIT 1
            ];

            if (!existingUsers.isEmpty()) {
                return createErrorResponse(
                    'User already exists: ' + req.user.username,
                    'DUPLICATE_USERNAME',
                    req.transactionId,
                    startTime
                );
            }

            // Get profile
            Profile profile = [
                SELECT Id
                FROM Profile
                WHERE Name = :req.user.profileName
                LIMIT 1
            ];

            // Create user
            User newUser = new User(
                Username = req.user.username,
                Email = req.user.email,
                FirstName = req.user.firstName,
                LastName = req.user.lastName,
                FederationIdentifier = req.user.federationIdentifier,
                IsActive = req.user.isActive,
                ProfileId = profile.Id,
                Alias = req.user.alias != null ? req.user.alias : generateAlias(req.user.firstName, req.user.lastName),
                TimeZoneSidKey = req.user.timeZoneSidKey != null ? req.user.timeZoneSidKey : 'America/New_York',
                LocaleSidKey = req.user.localeSidKey != null ? req.user.localeSidKey : 'en_US',
                EmailEncodingKey = req.user.emailEncodingKey != null ? req.user.emailEncodingKey : 'UTF-8',
                LanguageLocaleKey = req.user.languageLocaleKey != null ? req.user.languageLocaleKey : 'en_US'
            );

            // Get role if specified
            if (String.isNotBlank(req.user.roleName)) {
                UserRole role = SailPointProvisioningHelper.getRoleBySailPointName(req.user.roleName);
                if (role != null) {
                    newUser.UserRoleId = role.Id;
                }
            }

            insert newUser;

            // Assign permission set groups (will be done by trigger, but we can also do it synchronously)
            List<String> assignedPSGs = SailPointProvisioningHelper.assignPermissionSetGroupsByRole(newUser.Id, newUser.UserRoleId);

            // Create log
            String provisioningLogId = SailPointProvisioningHelper.createProvisioningLog(
                newUser.Id,
                req.transactionId,
                'Provision',
                'Success',
                newUser.UserRoleId,
                assignedPSGs,
                requestBody,
                null,
                (System.currentTimeMillis() - startTime)
            );

            // Build response
            res.success = true;
            res.transactionId = req.transactionId;
            res.salesforceUserId = newUser.Id;
            res.username = newUser.Username;
            res.roleAssigned = req.user.roleName;
            res.permissionSetGroupsAssigned = assignedPSGs;
            res.provisioningLogId = provisioningLogId;
            res.message = 'User successfully provisioned';
            res.processingTimeMs = System.currentTimeMillis() - startTime;

            // Send callback to SailPoint (asynchronously)
            if (SailPointProvisioningHelper.isCallbackEnabled()) {
                SailPointProvisioningHelper.sendCallbackAsync(res);
            }

        } catch (Exception e) {
            res = createErrorResponse(e.getMessage(), 'PROVISION_FAILED', req.transactionId, startTime);

            // Log error
            SailPointProvisioningHelper.createProvisioningLog(
                null,
                req.transactionId,
                'Provision',
                'Failed',
                null,
                null,
                requestBody,
                e.getMessage(),
                (System.currentTimeMillis() - startTime)
            );
        }

        return res;
    }

    /**
     * @description Handle update action (update existing user role)
     */
    private static ProvisioningResponse handleUpdate(ProvisioningRequest req, String requestBody, Long startTime) {
        ProvisioningResponse res = new ProvisioningResponse();

        try {
            // Find user
            User existingUser = [
                SELECT Id, Username, UserRoleId, UserRole.DeveloperName
                FROM User
                WHERE Username = :req.user.username
                LIMIT 1
            ];

            String previousRole = existingUser.UserRole?.DeveloperName;

            // Update role if specified
            if (String.isNotBlank(req.user.roleName)) {
                UserRole newRole = SailPointProvisioningHelper.getRoleBySailPointName(req.user.roleName);
                if (newRole != null) {
                    existingUser.UserRoleId = newRole.Id;
                    update existingUser;
                }
            }

            // Reassign permission set groups
            List<String> removedPSGs = SailPointProvisioningHelper.removeAllPermissionSetGroups(existingUser.Id);
            List<String> assignedPSGs = SailPointProvisioningHelper.assignPermissionSetGroupsByRole(existingUser.Id, existingUser.UserRoleId);

            // Create log
            String provisioningLogId = SailPointProvisioningHelper.createProvisioningLog(
                existingUser.Id,
                req.transactionId,
                'Update',
                'Success',
                existingUser.UserRoleId,
                assignedPSGs,
                requestBody,
                null,
                (System.currentTimeMillis() - startTime)
            );

            // Build response
            res.success = true;
            res.transactionId = req.transactionId;
            res.salesforceUserId = existingUser.Id;
            res.username = existingUser.Username;
            res.previousRole = previousRole;
            res.newRole = req.user.roleName;
            res.permissionSetGroupsRemoved = removedPSGs;
            res.permissionSetGroupsAssigned = assignedPSGs;
            res.provisioningLogId = provisioningLogId;
            res.message = 'User role successfully updated';
            res.processingTimeMs = System.currentTimeMillis() - startTime;

            // Send callback
            if (SailPointProvisioningHelper.isCallbackEnabled()) {
                SailPointProvisioningHelper.sendCallbackAsync(res);
            }

        } catch (QueryException e) {
            res = createErrorResponse('User not found: ' + req.user.username, 'USER_NOT_FOUND', req.transactionId, startTime);
        } catch (Exception e) {
            res = createErrorResponse(e.getMessage(), 'UPDATE_FAILED', req.transactionId, startTime);
        }

        return res;
    }

    /**
     * @description Handle deprovision action (deactivate user)
     */
    private static ProvisioningResponse handleDeprovision(ProvisioningRequest req, String requestBody, Long startTime) {
        ProvisioningResponse res = new ProvisioningResponse();

        try {
            // Find user
            User existingUser = [
                SELECT Id, Username, IsActive
                FROM User
                WHERE Username = :req.username
                LIMIT 1
            ];

            // Deactivate user
            existingUser.IsActive = false;
            existingUser.UserRoleId = null;
            update existingUser;

            // Remove all permission set groups
            List<String> removedPSGs = SailPointProvisioningHelper.removeAllPermissionSetGroups(existingUser.Id);

            // Create log
            String provisioningLogId = SailPointProvisioningHelper.createProvisioningLog(
                existingUser.Id,
                req.transactionId,
                'Deprovision',
                'Success',
                null,
                null,
                requestBody,
                null,
                (System.currentTimeMillis() - startTime)
            );

            // Build response
            res.success = true;
            res.transactionId = req.transactionId;
            res.salesforceUserId = existingUser.Id;
            res.username = existingUser.Username;
            res.userDeactivated = true;
            res.permissionSetGroupsRemoved = removedPSGs;
            res.provisioningLogId = provisioningLogId;
            res.message = 'User successfully deprovisioned';
            res.processingTimeMs = System.currentTimeMillis() - startTime;

            // Send callback
            if (SailPointProvisioningHelper.isCallbackEnabled()) {
                SailPointProvisioningHelper.sendCallbackAsync(res);
            }

        } catch (QueryException e) {
            res = createErrorResponse('User not found: ' + req.username, 'USER_NOT_FOUND', req.transactionId, startTime);
        } catch (Exception e) {
            res = createErrorResponse(e.getMessage(), 'DEPROVISION_FAILED', req.transactionId, startTime);
        }

        return res;
    }

    /**
     * @description Create error response
     */
    private static ProvisioningResponse createErrorResponse(String message, String errorCode, String transactionId, Long startTime) {
        ProvisioningResponse res = new ProvisioningResponse();
        res.success = false;
        res.transactionId = transactionId;
        res.errorCode = errorCode;
        res.errorMessage = message;
        res.processingTimeMs = System.currentTimeMillis() - startTime;
        return res;
    }

    /**
     * @description Generate user alias from name
     */
    private static String generateAlias(String firstName, String lastName) {
        String alias = firstName.substring(0, 1) + lastName;
        if (alias.length() > 8) {
            alias = alias.substring(0, 8);
        }
        return alias;
    }

    // Inner classes for request/response

    global class ProvisioningRequest {
        global String transactionId;
        global String action; // provision, update, deprovision
        global String username; // for deprovision
        global String reason; // for deprovision
        global UserInfo user;
    }

    global class UserInfo {
        global String username;
        global String email;
        global String firstName;
        global String lastName;
        global String federationIdentifier;
        global Boolean isActive;
        global String roleName; // SailPoint role name
        global String profileName;
        global String alias;
        global String timeZoneSidKey;
        global String localeSidKey;
        global String emailEncodingKey;
        global String languageLocaleKey;
    }

    global class ProvisioningResponse {
        global Boolean success;
        global String transactionId;
        global String salesforceUserId;
        global String username;
        global String roleAssigned;
        global String previousRole;
        global String newRole;
        global Boolean userDeactivated;
        global List<String> permissionSetGroupsAssigned;
        global List<String> permissionSetGroupsRemoved;
        global String provisioningLogId;
        global String message;
        global String errorCode;
        global String errorMessage;
        global Long processingTimeMs;
    }

    global class StatusResponse {
        global Boolean success;
        global String salesforceUserId;
        global String username;
        global String email;
        global String firstName;
        global String lastName;
        global Boolean isActive;
        global String userRoleId;
        global String userRoleName;
        global String profileName;
        global List<PermissionSetGroupInfo> permissionSetGroups;
        global LastProvisioningAction lastProvisioningAction;
        global String errorCode;
        global String errorMessage;
    }

    global class PermissionSetGroupInfo {
        global String id;
        global String developerName;
        global String label;
        global DateTime assignedDate;

        global PermissionSetGroupInfo(String id, String developerName, String label, DateTime assignedDate) {
            this.id = id;
            this.developerName = developerName;
            this.label = label;
            this.assignedDate = assignedDate;
        }
    }

    global class LastProvisioningAction {
        global String id;
        global String transactionId;
        global String actionType;
        global String status;
        global DateTime createdDate;

        global LastProvisioningAction(String id, String transactionId, String actionType, String status, DateTime createdDate) {
            this.id = id;
            this.transactionId = transactionId;
            this.actionType = actionType;
            this.status = status;
            this.createdDate = createdDate;
        }
    }
}
```

---

### 2. Helper Class: SailPointProvisioningHelper

**File:** `force-app/main/default/classes/SailPointProvisioningHelper.cls`

```apex
/**
 * @description Helper class for SailPoint provisioning operations
 * @author Development Team
 * @date 2026-01-19
 */
public class SailPointProvisioningHelper {

    /**
     * @description Get Salesforce role by SailPoint role name
     */
    public static UserRole getRoleBySailPointName(String sailPointRoleName) {
        // Query custom metadata to find mapping
        Role_Permission_Set_Group_Mapping__mdt mapping = [
            SELECT Role_Developer_Name__c
            FROM Role_Permission_Set_Group_Mapping__mdt
            WHERE SailPoint_Role_Name__c = :sailPointRoleName
            AND Active__c = true
            LIMIT 1
        ];

        if (mapping != null) {
            List<UserRole> roles = [
                SELECT Id, DeveloperName
                FROM UserRole
                WHERE DeveloperName = :mapping.Role_Developer_Name__c
                LIMIT 1
            ];
            return !roles.isEmpty() ? roles[0] : null;
        }

        return null;
    }

    /**
     * @description Assign permission set groups based on user role
     * @return List of assigned PSG developer names
     */
    public static List<String> assignPermissionSetGroupsByRole(Id userId, Id userRoleId) {
        List<String> assignedPSGs = new List<String>();

        if (userRoleId == null) {
            return assignedPSGs;
        }

        // Get role developer name
        UserRole role = [SELECT DeveloperName FROM UserRole WHERE Id = :userRoleId LIMIT 1];

        // Query metadata mapping
        List<Role_Permission_Set_Group_Mapping__mdt> mappings = [
            SELECT Permission_Set_Group_Name__c
            FROM Role_Permission_Set_Group_Mapping__mdt
            WHERE Role_Developer_Name__c = :role.DeveloperName
            AND Active__c = true
            AND (Effective_Date__c = null OR Effective_Date__c <= TODAY)
            AND (End_Date__c = null OR End_Date__c >= TODAY)
        ];

        if (mappings.isEmpty()) {
            return assignedPSGs;
        }

        // Get permission set group IDs
        Set<String> psgNames = new Set<String>();
        for (Role_Permission_Set_Group_Mapping__mdt mapping : mappings) {
            psgNames.add(mapping.Permission_Set_Group_Name__c);
        }

        List<PermissionSetGroup> psgs = [
            SELECT Id, DeveloperName
            FROM PermissionSetGroup
            WHERE DeveloperName IN :psgNames
        ];

        // Create assignments
        List<PermissionSetAssignment> assignments = new List<PermissionSetAssignment>();
        for (PermissionSetGroup psg : psgs) {
            assignments.add(new PermissionSetAssignment(
                AssigneeId = userId,
                PermissionSetGroupId = psg.Id
            ));
            assignedPSGs.add(psg.DeveloperName);
        }

        if (!assignments.isEmpty()) {
            insert assignments;
        }

        return assignedPSGs;
    }

    /**
     * @description Remove all permission set groups from user
     * @return List of removed PSG developer names
     */
    public static List<String> removeAllPermissionSetGroups(Id userId) {
        List<String> removedPSGs = new List<String>();

        // Query existing assignments
        List<PermissionSetAssignment> assignments = [
            SELECT Id, PermissionSetGroup.DeveloperName
            FROM PermissionSetAssignment
            WHERE AssigneeId = :userId
            AND PermissionSetGroupId != null
        ];

        for (PermissionSetAssignment psa : assignments) {
            removedPSGs.add(psa.PermissionSetGroup.DeveloperName);
        }

        if (!assignments.isEmpty()) {
            delete assignments;
        }

        return removedPSGs;
    }

    /**
     * @description Create provisioning log record
     * @return Log record ID
     */
    public static String createProvisioningLog(
        Id userId,
        String transactionId,
        String actionType,
        String status,
        Id roleId,
        List<String> psgNames,
        String requestPayload,
        String errorMessage,
        Long processingTimeMs
    ) {
        // Check if logging is enabled
        if (!isLoggingEnabled()) {
            return null;
        }

        SailPoint_Provisioning_Log__c log = new SailPoint_Provisioning_Log__c(
            User__c = userId,
            SailPoint_Transaction_Id__c = transactionId,
            Action_Type__c = actionType,
            Status__c = status,
            Role_Assigned__c = roleId,
            Permission_Set_Groups_Assigned__c = psgNames != null ? JSON.serialize(psgNames) : null,
            Request_Payload__c = requestPayload,
            Error_Message__c = errorMessage,
            Processing_Time_Ms__c = processingTimeMs,
            Source_System__c = 'SailPoint',
            Integration_User__c = UserInfo.getUserId()
        );

        insert log;
        return log.Id;
    }

    /**
     * @description Log exception
     */
    public static void logException(Exception e, Object request) {
        SailPoint_Provisioning_Log__c log = new SailPoint_Provisioning_Log__c(
            Action_Type__c = 'Query',
            Status__c = 'Failed',
            Error_Message__c = e.getMessage() + '\n' + e.getStackTraceString(),
            Request_Payload__c = JSON.serialize(request),
            Source_System__c = 'SailPoint',
            Integration_User__c = UserInfo.getUserId()
        );

        insert log;
    }

    /**
     * @description Send callback to SailPoint asynchronously
     */
    @future(callout=true)
    public static void sendCallbackAsync(SailPointUserProvisioningService.ProvisioningResponse response) {
        sendCallback(response);
    }

    /**
     * @description Send callback to SailPoint
     */
    public static void sendCallback(SailPointUserProvisioningService.ProvisioningResponse response) {
        try {
            String callbackUrl = getSetting('SAILPOINT_CALLBACK_URL');
            if (String.isBlank(callbackUrl)) {
                return;
            }

            // Build callback payload
            Map<String, Object> payload = new Map<String, Object>{
                'transactionId' => response.transactionId,
                'salesforceUserId' => response.salesforceUserId,
                'username' => response.username,
                'action' => 'provision', // or update/deprovision
                'status' => response.success ? 'success' : 'failed',
                'timestamp' => DateTime.now().format('yyyy-MM-dd\'T\'HH:mm:ss.SSS\'Z\''),
                'message' => response.message
            };

            // Make HTTP callout
            HttpRequest req = new HttpRequest();
            req.setEndpoint(callbackUrl);
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            req.setBody(JSON.serialize(payload));
            req.setTimeout(30000);

            Http http = new Http();
            HttpResponse res = http.send(req);

            // Log callback result
            // (Add logging here if needed)

        } catch (Exception e) {
            // Log callback error
            System.debug('SailPoint callback failed: ' + e.getMessage());
        }
    }

    /**
     * @description Check if callbacks are enabled
     */
    public static Boolean isCallbackEnabled() {
        String setting = getSetting('ENABLE_SAILPOINT_CALLBACKS');
        return setting == 'true';
    }

    /**
     * @description Check if logging is enabled
     */
    public static Boolean isLoggingEnabled() {
        String setting = getSetting('ENABLE_PROVISIONING_LOGGING');
        return setting == 'true';
    }

    /**
     * @description Get integration setting value
     */
    public static String getSetting(String settingKey) {
        List<SailPoint_Integration_Setting__mdt> settings = [
            SELECT Setting_Value__c
            FROM SailPoint_Integration_Setting__mdt
            WHERE Setting_Key__c = :settingKey
            AND Active__c = true
            AND (Environment__c = :getEnvironmentType() OR Environment__c = 'All')
            LIMIT 1
        ];

        return !settings.isEmpty() ? settings[0].Setting_Value__c : null;
    }

    /**
     * @description Get environment type (Production, Sandbox)
     */
    private static String getEnvironmentType() {
        return [SELECT IsSandbox FROM Organization LIMIT 1].IsSandbox ? 'Sandbox' : 'Production';
    }
}
```

---

### 3. User Trigger

**File:** `force-app/main/default/triggers/UserTrigger.trigger`

```apex
/**
 * @description Trigger on User object for permission set group assignment
 * @author Development Team
 * @date 2026-01-19
 */
trigger UserTrigger on User (after insert, after update) {
    if (Trigger.isAfter) {
        if (Trigger.isInsert) {
            UserTriggerHandler.handleAfterInsert(Trigger.new);
        }
        if (Trigger.isUpdate) {
            UserTriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
        }
    }
}
```

---

### 4. User Trigger Handler

**File:** `force-app/main/default/classes/UserTriggerHandler.cls`

```apex
/**
 * @description Handler for User trigger
 * @author Development Team
 * @date 2026-01-19
 */
public class UserTriggerHandler {

    /**
     * @description Handle after insert - assign permission set groups based on role
     */
    public static void handleAfterInsert(List<User> newUsers) {
        List<Id> userIdsWithRoles = new List<Id>();

        for (User u : newUsers) {
            if (u.UserRoleId != null) {
                userIdsWithRoles.add(u.Id);
            }
        }

        if (!userIdsWithRoles.isEmpty()) {
            assignPermissionSetGroupsAsync(userIdsWithRoles);
        }
    }

    /**
     * @description Handle after update - reassign permission set groups if role changed
     */
    public static void handleAfterUpdate(List<User> newUsers, Map<Id, User> oldMap) {
        List<Id> userIdsWithChangedRoles = new List<Id>();

        for (User u : newUsers) {
            User oldUser = oldMap.get(u.Id);
            if (u.UserRoleId != oldUser.UserRoleId) {
                userIdsWithChangedRoles.add(u.Id);
            }
        }

        if (!userIdsWithChangedRoles.isEmpty()) {
            reassignPermissionSetGroupsAsync(userIdsWithChangedRoles);
        }
    }

    /**
     * @description Assign permission set groups asynchronously
     */
    @future
    public static void assignPermissionSetGroupsAsync(List<Id> userIds) {
        for (Id userId : userIds) {
            User u = [SELECT UserRoleId FROM User WHERE Id = :userId LIMIT 1];
            SailPointProvisioningHelper.assignPermissionSetGroupsByRole(userId, u.UserRoleId);
        }
    }

    /**
     * @description Reassign permission set groups asynchronously
     */
    @future
    public static void reassignPermissionSetGroupsAsync(List<Id> userIds) {
        for (Id userId : userIds) {
            // Remove old assignments
            SailPointProvisioningHelper.removeAllPermissionSetGroups(userId);

            // Assign new based on current role
            User u = [SELECT UserRoleId FROM User WHERE Id = :userId LIMIT 1];
            SailPointProvisioningHelper.assignPermissionSetGroupsByRole(userId, u.UserRoleId);
        }
    }
}
```

---

## Error Handling and Logging

### Error Handling Strategy

1. **API Level:** All REST endpoints return standardized error responses with error codes
2. **Database Level:** Use try-catch blocks around DML operations
3. **Integration Level:** Retry logic for SailPoint callbacks (3 retries with exponential backoff)
4. **Audit Level:** Log all actions to `SailPoint_Provisioning_Log__c`

### Error Codes

| Error Code | Description | HTTP Status | Retry? |
|------------|-------------|-------------|---------|
| INVALID_REQUEST | Request body is invalid or missing required fields | 400 | No |
| INVALID_ACTION | Action type is not recognized | 400 | No |
| DUPLICATE_USERNAME | User with username already exists | 400 | No |
| USER_NOT_FOUND | User does not exist in Salesforce | 404 | No |
| ROLE_NOT_FOUND | Specified role does not exist | 400 | No |
| PSG_NOT_FOUND | Permission set group not found for role | 500 | Yes |
| PROVISION_FAILED | User provisioning failed | 500 | Yes |
| UPDATE_FAILED | User update failed | 500 | Yes |
| DEPROVISION_FAILED | User deprovisioning failed | 500 | Yes |
| EXCEPTION | Unexpected exception occurred | 500 | Yes |
| CALLBACK_FAILED | Callback to SailPoint failed | N/A | Yes (auto-retry) |

### Logging Requirements

All provisioning actions must be logged to `SailPoint_Provisioning_Log__c` with:
- Transaction ID from SailPoint
- User ID (if applicable)
- Action type
- Status (Success/Failed)
- Request and response payloads
- Error messages (if failed)
- Processing time in milliseconds

---

## Security and Authentication

### Authentication Methods

#### Option 1: OAuth 2.0 JWT Bearer Flow (Recommended)

1. **SailPoint** obtains JWT token from Salesforce
2. **SailPoint** includes token in Authorization header: `Bearer {token}`
3. **Salesforce** validates token and processes request

**Setup:**
- Create Connected App in Salesforce
- Configure OAuth policies and certificates
- Provide Connected App details to SailPoint team

#### Option 2: Named Credential with External Credential

1. **SailPoint** uses API key/token
2. **Salesforce** validates via Named Credential
3. Named Credential stores authentication details securely

**Setup:**
- Create Named Credential in Salesforce
- Configure authentication protocol (OAuth 2.0, Password, Custom)
- SailPoint provides credentials/certificates

### Permission Requirements

**Integration User Requirements:**
- Profile: System Administrator or custom integration profile
- Permission Sets:
  - `PS_Integration_Admin`
  - API Enabled
  - Modify All Data (for user provisioning)
  - View All Users

**API Endpoint Security:**
- IP Restrictions: Configure trusted IP ranges in Connected App
- Session Settings: Enforce timeout and idle session settings
- Audit: Enable Event Monitoring for API usage

---

## Testing Strategy

### Unit Testing Requirements

**Target Coverage:** 90%+ for all classes

**Test Classes to Create:**

1. **SailPointUserProvisioningServiceTest.cls**
   - Test POST /provision with valid request
   - Test POST /provision with duplicate username
   - Test POST /update with role change
   - Test POST /deprovision
   - Test GET /status/{username}
   - Test error handling for invalid requests

2. **SailPointProvisioningHelperTest.cls**
   - Test getRoleBySailPointName()
   - Test assignPermissionSetGroupsByRole()
   - Test removeAllPermissionSetGroups()
   - Test createProvisioningLog()
   - Test sendCallback() (with mock callout)

3. **UserTriggerHandlerTest.cls**
   - Test user insert with role (PSG assignment)
   - Test user update with role change (PSG reassignment)
   - Test user update without role change (no action)

### Integration Testing

**Test Scenarios:**

| Scenario | Expected Result |
|----------|----------------|
| SailPoint provisions new user with CS role | User created, PSG_Customer_Service_Representative assigned |
| SailPoint updates user from CS to Sales role | PSG removed and PSG_Sales_Team_Member assigned |
| SailPoint deprovisions user | User deactivated, all PSGs removed |
| SailPoint queries user status | Returns user details with assigned PSGs |
| Invalid authentication token | Returns 401 Unauthorized |
| Duplicate username | Returns 400 with DUPLICATE_USERNAME error |
| Non-existent role | Returns 400 with ROLE_NOT_FOUND error |

### UAT Testing

**UAT Scenarios:**

1. **End-to-End Provisioning:** SailPoint triggers new hire → Salesforce user created → PSG assigned → User can log in and access appropriate features
2. **Role Change:** User changes role in HR system → SailPoint updates Salesforce → New PSG assigned → User has correct access
3. **Termination:** User terminated in HR system → SailPoint deprovisions → User deactivated → Cannot log in

---

## Deployment Guide

### Pre-Deployment Checklist

- [ ] All 35 permission sets created in target org
- [ ] All 8 permission set groups created in target org
- [ ] Custom objects deployed (SailPoint_Provisioning_Log__c)
- [ ] Custom metadata types deployed
- [ ] Custom metadata records created for role mappings
- [ ] Salesforce roles exist with correct developer names
- [ ] Minimal Access profile created and tested

### Deployment Steps

#### Phase 1: Data Model and Configuration (Week 1)

1. Deploy custom objects:
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/objects/SailPoint_Provisioning_Log__c
   ```

2. Deploy custom metadata types:
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/customMetadata
   ```

3. Create custom metadata records (manual or via API):
   - 8 Role_Permission_Set_Group_Mapping__mdt records
   - SailPoint_Integration_Setting__mdt records

#### Phase 2: Permission Sets and Groups (Weeks 2-4)

4. Deploy all 35 permission sets:
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/permissionsets
   ```

5. Create all 8 permission set groups via Setup UI or metadata

6. Test each permission set group with pilot user

#### Phase 3: Code Deployment (Week 5)

7. Deploy Apex classes:
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/classes/SailPointUserProvisioningService.cls
   sfdx force:source:deploy --sourcepath force-app/main/default/classes/SailPointProvisioningHelper.cls
   sfdx force:source:deploy --sourcepath force-app/main/default/classes/UserTriggerHandler.cls
   ```

8. Deploy User trigger:
   ```bash
   sfdx force:source:deploy --sourcepath force-app/main/default/triggers/UserTrigger.trigger
   ```

9. Deploy test classes and run tests:
   ```bash
   sfdx force:apex:test:run --classnames SailPointUserProvisioningServiceTest,SailPointProvisioningHelperTest,UserTriggerHandlerTest --codecoverage
   ```

#### Phase 4: Integration Setup (Week 6)

10. Create Connected App for SailPoint
11. Configure OAuth policies and certificates
12. Create Named Credential for SailPoint callbacks
13. Configure Remote Site Settings
14. Test API endpoints using Postman/cURL

#### Phase 5: SailPoint Configuration (Week 7)

15. Provide SailPoint team with:
    - Salesforce API endpoints
    - Connected App credentials
    - Role mapping documentation
    - API request/response formats
16. SailPoint team configures Salesforce connector
17. Test end-to-end integration in sandbox

#### Phase 6: Production Deployment (Week 8)

18. Deploy to production following change management process
19. Monitor initial provisioning actions
20. Validate logging and audit trails
21. Perform UAT with real users

### Post-Deployment Validation

**Validation Checklist:**

- [ ] API endpoints accessible from SailPoint
- [ ] Test user provisioned successfully via SailPoint
- [ ] Permission set groups assigned automatically
- [ ] Provisioning logs created for all actions
- [ ] Callbacks to SailPoint working (if enabled)
- [ ] Error handling working as expected
- [ ] Integration user has correct permissions

---

## Appendices

### Appendix A: SailPoint to Salesforce Role Mapping

| SailPoint Role Name | Salesforce UserRole Developer Name | Permission Set Group | User Count |
|---------------------|-------------------------------------|----------------------|------------|
| CS_Representative | Customer_Service_Representative | PSG_Customer_Service_Representative | ~50 |
| Sales_Team_Member | Sales_Team_Member | PSG_Sales_Team_Member | ~15 |
| Fulfillment_Specialist | Fulfillment_Specialist | PSG_Fulfillment_Specialist | ~10 |
| IT_Support_Member | IT_Support_Member | PSG_IT_Support_Member | ~5 |
| Compliance_Team_Member | Compliance_Team_Member | PSG_Compliance_Team_Member | 3-5 |
| System_Administrator | System_Administrator | PSG_System_Administrator | 2-3 |
| Reporting_Analyst | Reporting_Analyst | PSG_Reporting_Analyst | 5-10 |
| QA_Tester | Quality_Assurance_Tester | PSG_Quality_Assurance_Tester | 3-5 |

### Appendix B: API Request/Response Examples

*Refer to API Specifications section for complete examples*

### Appendix C: Troubleshooting Guide

**Issue:** User provisioned but PSG not assigned

**Resolution:**
1. Check User trigger is active
2. Verify Role_Permission_Set_Group_Mapping__mdt record exists and is active
3. Check UserRoleId was set correctly
4. Review SailPoint_Provisioning_Log__c for errors

**Issue:** API returns "USER_NOT_FOUND"

**Resolution:**
1. Verify username format matches Salesforce (usually email)
2. Check if user exists but is in different org (sandbox vs production)

**Issue:** Callback to SailPoint fails

**Resolution:**
1. Verify SAILPOINT_CALLBACK_URL setting is correct
2. Check Named Credential is configured
3. Review Remote Site Settings
4. Check SailPoint endpoint is accessible from Salesforce

---

## Document Metadata

**Document Title:** SailPoint Integration Technical Design Document
**Version:** 1.0
**Date Created:** January 19, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT - Ready for Development
**Next Review Date:** TBD

**Related Documents:**
- Permission-Strategy-Analysis.md
- User-Group-Reference.md
- Claude.md (Architecture Documentation)

---

**END OF SAILPOINT INTEGRATION TECHNICAL DESIGN DOCUMENT**
