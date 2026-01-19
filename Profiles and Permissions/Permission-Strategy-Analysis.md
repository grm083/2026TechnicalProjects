# Salesforce Permission Strategy Analysis

**Document Author:** Claude (AI Assistant)
**Document Version:** 1.0
**Date:** January 19, 2026
**Purpose:** Comprehensive analysis and strategy for migrating to feature-based permission sets and persona-based permission set groups

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Assessment](#current-state-assessment)
3. [Feature Inventory](#feature-inventory)
4. [Gap Analysis](#gap-analysis)
5. [Recommended Permission Strategy](#recommended-permission-strategy)
6. [Role-Based Automation Strategy](#role-based-automation-strategy)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Appendices](#appendices)

---

## Executive Summary

### Purpose

This document provides a comprehensive analysis of the current Salesforce permission structure and proposes a strategic migration to a modern, scalable permission model based on Salesforce best practices for 2026 and beyond.

### Current State

- **Profiles:** 17 active profiles with embedded permissions
- **Permission Sets:** 31 existing permission sets (limited functional organization)
- **User Groups:** 5 primary personas (~83 total users)
- **Custom Objects:** 65 custom objects across 20 functional areas
- **Architecture:** 699 Apex classes, 247 UI components, 95 flows

### Strategic Goals

1. **Create a single minimal-access profile** for the entire organization that provides read-only access to core platform features
2. **Develop feature-based permission sets** for each major capability (Case Management, CPQ/Quoting, Work Orders, etc.)
3. **Establish persona-based permission set groups** aligned to the 5 user groups (Customer Service, Sales, Fulfillment, IT Support, Compliance)
4. **Implement automated permission assignment** that correlates UserRoleId to permission set groups via custom metadata

### Business Value

- **Simplified Administration:** Reduce maintenance from 17 profiles to 1 profile + modular permission sets
- **Improved Security:** Principle of least privilege with granular feature access
- **Enhanced Scalability:** Easy to add new features or personas without profile proliferation
- **Future-Proof:** Aligns with Salesforce's strategic direction away from profile-based permissions
- **Audit Compliance:** Clear visibility into who has access to what features

---

## Current State Assessment

### Existing Profiles Analysis

The organization currently maintains 17 distinct profiles:

| Profile Name | Primary User Group | Current Purpose | Users (Est.) |
|-------------|-------------------|-----------------|--------------|
| **Customer Service** | Customer Service Representatives | Front-line case/quote management | ~50 |
| **Customer Account Team** | Sales Team Members | Sales operations and escalations | ~15 |
| **SSM** | Fulfillment Team Members | Service Supply Management | ~5 |
| **Vendor Relations** | Fulfillment Team Members | Vendor management | ~5 |
| **Digital Transformation Team** | IT Support Members | Read-only production access | ~5 |
| **Compliance** | Compliance Team Members | Audit and entitlement governance | 3-5 |
| **Admin** | System Administrators | Full system administration | 2-3 |
| **ReadOnly** | External/Audit Users | Read-only system access | Variable |
| **Audit Read Only** | External Auditors | Compliance audit access | Variable |
| **Customer Digital Engagement Team** | Customer Service (specialized) | Digital channel management | ~10 |
| **Quality-Assurance** | QA Team | Testing and validation | 3-5 |
| **Quality-Billing** | Billing Operations | Billing and invoicing | 3-5 |
| **Reporting** | Business Analysts | Reporting and analytics | 5-10 |
| **Launch Team** | Project/Implementation Team | New feature deployment | 3-5 |
| **Integration Administrator** | Integration/API Users | System integration management | 1-2 |
| **Analytics Cloud Integration User** | Analytics/BI Platform | Analytics integration | System |
| **Account Team** | Account Management | Account-level operations | Variable |

**Key Findings:**
- Significant overlap in permissions across profiles
- Profile-based approach creates maintenance burden (17 separate configurations)
- Difficult to identify which features are controlled by which profile
- New user onboarding requires careful profile selection
- Changes to feature access require updating multiple profiles

### Existing Permission Sets Analysis

The organization has 31 permission sets with varying levels of organization:

#### Administrative Permission Sets
- Modify_All_Data
- View_Setup_and_Configuration
- Manage_Flows
- Password_Never_Expires

#### Feature-Specific Permission Sets
- **Quote/Pricing:**
  - CPQReadOnly
  - Pricing_Access
  - Pricing_Read_Only
  - QuoteOrdersUser
  - Price_Accessibility_Permission_Set
  - Cost_Accessibility_Permission_Set

- **Reporting:**
  - Reports_and_Dashboards_Administrator
  - Reports_and_Dashboards_Super_User
  - Customer_Service_Reporting_User

- **Asset Management:**
  - AAV_Availability_Stand_Alone_Tool
  - Asset_Availability_User_Permission_Set

- **Task/Case Management:**
  - Task_Genesys_Routing_Permission
  - Merge_Access_for_Non_Admin_Users

- **Specialized Functions:**
  - STP_Administration (Straight-Through Processing)
  - Business_Rule_Notification
  - Escalation_Maintenance_Permissions
  - Account_Notification_Maintenance
  - Contact_Notification_Maintenance
  - MAA_Admin_Panel_Team (Market Area Alerts)
  - MAS_Permissionset

- **Operational:**
  - SBS_Account_Management
  - Manage_Premium_Deliveries
  - Launch_Fast
  - Digital_Transformation_Time_Tacking
  - Governance_Team
  - Knowledge_Manager_User
  - Project_Services_Project_Management

**Key Findings:**
- Some feature-based organization exists (Pricing, Reporting, Asset Management)
- No persona-based permission set groups currently exist
- Inconsistent naming conventions (some use underscores, others use spaces)
- Limited documentation on when to assign which permission sets
- No automated assignment mechanism

### User Group Analysis

Based on the User-Group-Reference.md documentation, there are 5 primary user personas:

| Persona | Volume | Profile(s) | Primary Functions |
|---------|--------|------------|-------------------|
| **Customer Service Representatives** | ~50 | Customer Service, Customer Digital Engagement Team | Case management, Work Orders, Standard Quotes, Task management |
| **Sales Team Members** | ~15 | Customer Account Team, Account Team | Escalation, Complex quotes, Quote approvals, Account strategy |
| **Fulfillment Team Members** | ~10 | SSM, Vendor Relations | Quote fulfillment, Vendor management, Data quality |
| **IT Support Members** | ~5 | Digital Transformation Team | Read-only troubleshooting, Exception log analysis |
| **Compliance Team Members** | 3-5 | Compliance | Entitlement governance, SLA management, SOX audit |

**Additional Personas (Supporting):**
- System Administrators (~2-3)
- Quality Assurance Team (3-5)
- Billing Operations (3-5)
- Reporting/Analytics (5-10)
- Launch/Implementation Team (3-5)

---

## Feature Inventory

Based on comprehensive codebase analysis, the platform delivers the following major business capabilities through 65 custom objects, 699 Apex classes, and 95 flows:

### 1. Quote and Pricing Management (CPQ)

**Business Capability:** Configure-Price-Quote functionality with multi-vendor pricing

**Custom Objects (10):**
- SBQQ__Quote__c - CPQ quotes
- SBQQ__QuoteLine__c - Quote line items
- SBQQ__ConfigurationAttribute__c - Product configuration
- SBQQ__ProductFeature__c - Product features
- SBQQ__ProductOption__c - Product bundles
- SBQQ__ErrorCondition__c - Validation rules
- QuoteApproval__c - Approval tracking
- Quote_Order__c - Quote-to-order conversion
- Quote_Line_History_Tracking__c - Audit trail
- Pricing_Request__c - External pricing integration

**Key Components:**
- 42 Lightning Web Components (many pricing-related)
- Multi-vendor pricing engine
- Quote approval workflows
- Request for Bid (RFB) automation

**User Access:**
- Create: Customer Service, Sales, Fulfillment (edit)
- Approve: Sales Team
- Fulfill: Fulfillment Team
- Audit: Compliance Team (read-only)

**Recommended Permission Set:** `PS_CPQ_Quote_Management`

---

### 2. Case Management

**Business Capability:** Customer service case lifecycle management

**Custom Objects (4):**
- Case (Standard - heavily customized)
- Case_Asset_Header__c - Asset relationships
- Case_History_Tracker__c - Audit trail
- Case_Process_Manager__c - Process control
- Case_Task_Tracker__c - Task tracking

**Key Components:**
- 50+ email templates
- Case highlight panels
- Case quick actions
- Custom case layouts (10+)

**User Access:**
- Create/Edit: Customer Service, Sales
- View: All personas
- Process Control: Administrators

**Recommended Permission Set:** `PS_Case_Management`

---

### 3. Work Order Management

**Business Capability:** Field service work order processing and dispatch

**Standard Objects (Extended):**
- WorkOrder (50+ custom fields)
- WorkOrderLineItem
- ServiceAppointment

**Key Components:**
- WorkOrderTrigger and handlers
- Acorn Field Service integration
- Work order email templates

**User Access:**
- Create/Edit: Customer Service
- View/Coordinate: Fulfillment Team
- Monitor: Compliance (SLA tracking)

**Recommended Permission Set:** `PS_Work_Order_Management`

---

### 4. Asset Management

**Business Capability:** Asset lifecycle tracking and availability management

**Custom Objects (2):**
- Asset (Standard - extended)
- AAV_Asset_Availability__c - Availability tracking
- SBS_Case_Asset__c - Case relationships

**Key Components:**
- Asset Availability Views (AAV) Lightning components
- Asset tracking automation
- Asset availability API integrations

**User Access:**
- View: All personas
- Edit: Customer Service, Fulfillment
- Availability Management: Specialized users

**Recommended Permission Set:** `PS_Asset_Management`

---

### 5. Approval Management

**Business Capability:** Multi-level approval workflows for quotes and services

**Custom Objects (3):**
- Approval_Log__c - Approval audit trail
- ApprovalImages__c - Supporting documentation
- Service_Approver__c - Approver routing

**Key Components:**
- Approval flows (10+)
- Approval email notifications
- Approval routing logic

**User Access:**
- View: All personas
- Approve: Sales Team (quotes), Compliance (services)
- Admin: System Administrators

**Recommended Permission Set:** `PS_Approval_Management`

---

### 6. Task Management

**Business Capability:** Task creation, assignment, and lifecycle management

**Custom Objects (2):**
- Task (Standard - extended)
- Complete_Task__c - Completion tracking
- Task_Genesys_Routing_Control__c - CTI routing

**Key Components:**
- Task Framework (Task_Framework__mdt configuration)
- Automated task assignment
- Out-of-office task reassignment
- Genesys CTI integration

**User Access:**
- Create/Edit: Customer Service, Sales, Fulfillment
- Route/Assign: System (automated via Genesys)
- View: All personas

**Recommended Permission Set:** `PS_Task_Management`

---

### 7. Business Rules Engine

**Business Capability:** Configurable business rules for automation

**Custom Objects (2):**
- Business_Rule__c - Rule definitions
- STP_Criteria__c - Straight-through processing rules

**Key Components:**
- BusinessRuleTrigger and helper classes
- Business Rule Selection flow
- Custom metadata field mappings (Business_Rule_Field_Mapping__mdt)

**User Access:**
- View: Customer Service, Sales
- Configure: System Administrators
- Audit: Compliance Team

**Recommended Permission Set:** `PS_Business_Rules_User` (view)
**Recommended Permission Set:** `PS_Business_Rules_Admin` (configure)

---

### 8. Vendor and Supplier Management

**Business Capability:** Vendor relationship and performance management

**Custom Objects (1):**
- Account (Vendor record types)
- SBS_Supplier_Scorecard__c - Performance tracking

**Key Components:**
- Vendor escalation contacts
- Supplier scorecarding
- Vendor pricing integration

**User Access:**
- Manage: Fulfillment Team
- View: Sales, Customer Service
- Performance Review: Management

**Recommended Permission Set:** `PS_Vendor_Management`

---

### 9. Entitlement and SLA Management

**Business Capability:** Service level agreement tracking and compliance

**Standard Objects (Extended):**
- Entitlement
- ServiceContract
- sla_calculation__c (custom)

**Key Components:**
- SLA tracking automation
- Entitlement validation
- SLA breach alerts

**User Access:**
- Manage: Compliance Team
- View: All personas
- Monitor: Customer Service (case SLAs)

**Recommended Permission Set:** `PS_Entitlement_Management`

---

### 10. Integration and Routing

**Business Capability:** External system integrations and contact center routing

**Custom Objects (3):**
- Integration_Process_Manager__c
- Genesys_Routing__c - CTI routing
- Genesys_Reporting__c - Call center metrics

**Key Components:**
- REST/SOAP web services
- Genesys CTI integration
- Acorn Field Service integration
- IVR service status integration
- Platform event handlers (96+ events)

**User Access:**
- Configure: Integration Administrators
- Monitor: IT Support Members
- View Routing: Customer Service

**Recommended Permission Set:** `PS_Integration_User` (view/monitor)
**Recommended Permission Set:** `PS_Integration_Admin` (configure)

---

### 11. Communication and Notifications

**Business Capability:** Multi-channel communication preferences and notification management

**Custom Objects (7):**
- Account_Notification_Preference__c
- Contact_Notification_Preference__c
- Notification_Asset__c
- Notification_Contact__c
- Communication_Channel__c
- Comment__c
- SFDCEmailMessage__c

**Key Components:**
- 381 email templates across 16 functional domains
- Email-to-case processing
- Chat transcript archival
- Notification automation

**User Access:**
- Manage Preferences: Customer Service
- Configure Templates: Administrators
- View: All personas

**Recommended Permission Set:** `PS_Communication_Management`

---

### 12. Reporting and Analytics

**Business Capability:** Business intelligence, dashboards, and ad-hoc reporting

**Standard Objects:**
- Report (14 standard reports)
- Dashboard (1+ dashboards)
- Analytics integration

**Key Components:**
- Work Order Reports folder
- System Administrator Reports
- Customer Service metrics
- Quote/pricing analytics

**User Access:**
- Create Reports: Reporting Team, Management
- View Reports: All personas (based on data access)
- Dashboard Design: Administrators

**Recommended Permission Set:** `PS_Reporting_User` (view/run)
**Recommended Permission Set:** `PS_Reporting_Admin` (create/edit)

---

### 13. Logging and Exception Handling

**Business Capability:** System logging, error tracking, and debugging

**Custom Objects (5):**
- ExceptionLog__c - Error logging
- ExceptionLog_Settings__c - Configuration
- System_Log__c - System-wide logging
- Logging_Framework_Control__c - Framework configuration
- FAST_Activity_Log__c - Activity tracking

**Key Components:**
- System_Log_Event__e platform event
- Centralized logging infrastructure
- Error notification workflows

**User Access:**
- View: IT Support Members
- Configure: System Administrators
- Monitor: Operations team

**Recommended Permission Set:** `PS_Exception_Log_User` (view)
**Recommended Permission Set:** `PS_Exception_Log_Admin` (configure)

---

### 14. Project and Time Tracking

**Business Capability:** Project management and time tracking for internal teams

**Custom Objects (2):**
- Project_Code__c
- Digital_Transformation_Time_Tracking__c

**Key Components:**
- Time tracking automation
- Project code management
- Resource allocation tracking

**User Access:**
- Track Time: Digital Transformation Team, Project Team
- View: Management
- Configure: Project Managers

**Recommended Permission Set:** `PS_Project_Time_Tracking`

---

### 15. Knowledge Management

**Business Capability:** Internal knowledge base and article management

**Standard Objects:**
- Knowledge__kav
- Knowledge articles

**Key Components:**
- Knowledge article creation/publishing
- Article search and recommendations
- Knowledge base integration

**User Access:**
- Author: Customer Service (power users), Subject Matter Experts
- Publish: Knowledge Managers
- View: All personas

**Recommended Permission Set:** `PS_Knowledge_User` (view)
**Recommended Permission Set:** `PS_Knowledge_Author` (create/edit)
**Recommended Permission Set:** `PS_Knowledge_Publisher` (publish)

---

### 16. Administrative Functions

**Business Capability:** System administration, configuration, and governance

**Configuration Objects (11):**
- Code_Switch__c - Feature toggles
- Config_PO__c - Purchase order settings
- Data_Store__c - Generic data storage
- EmailTemplateLogoId__c - Email branding
- Max_RecursiveCall__c - Recursion control
- Object_Save_Mode__c - Save behavior
- Origin__c - Origin tracking
- VRBatchSetting__c - Batch settings
- MAA_Admin_Settings__c - Market area alerts
- MAS_Setup_Detail__c - Setup configuration
- Market_Area_Alerts_Settings__c - Alert settings

**Key Components:**
- 3,034 custom metadata records
- Feature toggle framework
- System configuration management

**User Access:**
- Configure: System Administrators only
- View: IT Support (read-only)

**Recommended Permission Set:** `PS_System_Configuration` (admin only)

---

### 17. Market Area Alerts

**Business Capability:** Geographic market area alert management and notifications

**Custom Objects:**
- Market area alert related objects
- MAA_Admin_Settings__c

**Key Components:**
- MarketAreaAlertController
- Market area alert automation
- Geographic notification routing

**User Access:**
- Configure: MAA Admin Panel Team
- View: Customer Service, Sales
- Receive Alerts: All relevant personas

**Recommended Permission Set:** `PS_Market_Area_Alerts_User` (view/receive)
**Recommended Permission Set:** `PS_Market_Area_Alerts_Admin` (configure)

---

### 18. Categorization and Classification

**Business Capability:** Data categorization, classification, and disposition management

**Custom Objects (3):**
- Categorization__c
- Category__c
- Disposition__c

**Key Components:**
- Classification workflows
- Category assignment automation

**User Access:**
- Classify: Customer Service
- Manage Categories: Administrators
- Report: Management

**Recommended Permission Set:** `PS_Categorization_Management`

---

### 19. Survey and Feedback

**Business Capability:** Customer survey management and feedback collection

**Custom Objects (1):**
- Survey__c

**Key Components:**
- Survey automation
- Feedback collection workflows

**User Access:**
- View Results: Customer Service, Sales, Management
- Configure: Marketing/Operations
- Respond: Customers (external)

**Recommended Permission Set:** `PS_Survey_Management`

---

### 20. Organizational Management

**Business Capability:** Department structure, user availability, and queue management

**Custom Objects (3):**
- Department__c
- Out_of_Office__c
- Personal_Queue_Info__c

**Key Components:**
- Out-of-office task reassignment
- Queue management
- Department hierarchy

**User Access:**
- Manage Own: All users (Out_of_Office)
- View: Managers, Customer Service
- Configure: Administrators

**Recommended Permission Set:** `PS_Organizational_Management`

---

## Gap Analysis

### Current Challenges

#### 1. Profile Proliferation
- **Issue:** 17 different profiles create maintenance overhead
- **Impact:** Changes to feature access require updating multiple profiles
- **Risk:** Inconsistent permissions across similar roles

#### 2. Lack of Feature-Based Organization
- **Issue:** Permissions embedded in profiles rather than organized by feature
- **Impact:** Difficult to identify which users have access to specific features
- **Risk:** Over-permissioned users, security vulnerabilities

#### 3. No Persona-Based Permission Set Groups
- **Issue:** No logical grouping of permissions by job function
- **Impact:** Manual assignment of multiple permission sets per user
- **Risk:** Human error in permission assignment, incomplete access

#### 4. No Automated Permission Assignment
- **Issue:** Permission assignment is manual based on profile selection
- **Impact:** Time-consuming onboarding, potential for misconfiguration
- **Risk:** Users with incorrect access, compliance violations

#### 5. Inconsistent Naming Conventions
- **Issue:** Permission sets use mixed naming conventions (spaces vs underscores)
- **Impact:** Difficult to identify related permission sets
- **Risk:** Confusion during assignment, duplicate creation

#### 6. Limited Documentation
- **Issue:** No central documentation on when to assign which permission sets
- **Impact:** Tribal knowledge, inconsistent decisions
- **Risk:** Knowledge loss when team members leave

### Recommended Solutions

| Challenge | Solution | Priority |
|-----------|----------|----------|
| Profile Proliferation | Migrate to single minimal-access profile | High |
| Lack of Feature Organization | Create 30+ feature-based permission sets | High |
| No Persona Groups | Create 5 permission set groups aligned to user personas | High |
| No Automation | Implement role-based permission set group assignment via custom metadata | Medium |
| Inconsistent Naming | Establish naming convention standard (PS_Feature_Name) | High |
| Limited Documentation | Create permission matrix and decision tree | Medium |

---

## Recommended Permission Strategy

### Overview

The recommended strategy follows Salesforce best practices for 2026 and implements a three-tier permission model:

1. **Minimal-Access Profile** - Single organizational profile with read-only base access
2. **Feature-Based Permission Sets** - Modular permission sets for each business capability (~35 permission sets)
3. **Persona-Based Permission Set Groups** - Logical grouping of permission sets by job function (8 groups)

### Strategy Diagram

```
User → Assigned to → Minimal Access Profile (Read-Only Base)
                           ↓
User → Assigned to → Permission Set Group (Persona)
                           ↓
Permission Set Group → Contains → Multiple Feature Permission Sets
                           ↓
Feature Permission Sets → Grant → Specific Business Capabilities
```

---

### 1. Minimal-Access Profile

#### Profile Name: `Minimal Access - Organization Standard`

**Purpose:** Provide baseline read-only access to all users in the organization

**Base Permissions:**
- Read access to: Account, Contact, Case (public cases only), Task (owned tasks only)
- View dashboards and reports (based on record access)
- Access to standard Chatter features
- Login hours: 24/7 (or as per organizational policy)
- IP restrictions: As per organizational policy

**Object Permissions (CRUDV):**
- Account: Read only
- Contact: Read only
- Case: Read only (record access controlled by sharing)
- Task: Read/Create (own tasks only)
- Event: Read/Create (own events only)

**System Permissions:**
- API Enabled: FALSE (enabled via permission set if needed)
- View Setup and Configuration: FALSE
- Modify All Data: FALSE
- View All Data: FALSE

**Application Access:**
- Default App: Standard Lightning Service
- All custom apps: Visible (but functionality controlled by permission sets)

**Page Layouts:**
- Default page layouts for all objects
- Specialized layouts assigned via permission sets

**Record Types:**
- Default record types assigned
- Specialized record types granted via permission sets

**Benefits:**
- Single profile to maintain
- Easy to understand baseline
- Principle of least privilege
- Future-proof for Salesforce's direction

---

### 2. Feature-Based Permission Sets

Create 35 modular permission sets organized by business capability. Each permission set grants access to a specific feature area.

#### Naming Convention

All permission sets follow this format: `PS_[Feature_Area]_[Access_Level]`

- **PS** = Permission Set prefix
- **Feature_Area** = Business capability (no spaces, use underscores)
- **Access_Level** = User, Admin, Manager (optional)

Examples:
- `PS_Case_Management`
- `PS_CPQ_Quote_Management`
- `PS_Business_Rules_Admin`
- `PS_Exception_Log_User`

#### Recommended Permission Sets

##### Core Service Delivery (7)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_Case_Management` | Case (CRUD), Case_History_Tracker__c (RU), Case_Asset_Header__c (RU), Case_Task_Tracker__c (RU) | Full case lifecycle management | Customer Service, Sales |
| `PS_Work_Order_Management` | WorkOrder (CRU), WorkOrderLineItem (CRU), ServiceAppointment (RU) | Work order creation and tracking | Customer Service |
| `PS_Task_Management` | Task (CRUD), Complete_Task__c (RU), Task_Genesys_Routing_Control__c (R) | Task assignment and completion | All service personas |
| `PS_Asset_Management` | Asset (RU), AAV_Asset_Availability__c (R), SBS_Case_Asset__c (RU) | Asset tracking and availability | Customer Service, Fulfillment |
| `PS_Entitlement_Management` | Entitlement (CRUD), ServiceContract (RU), sla_calculation__c (CRUD) | SLA and entitlement governance | Compliance Team |
| `PS_Communication_Management` | Account_Notification_Preference__c (CRUD), Contact_Notification_Preference__c (CRUD), Communication_Channel__c (RU) | Notification preferences | Customer Service |
| `PS_Categorization_Management` | Categorization__c (CRUD), Category__c (R), Disposition__c (CRUD) | Case/issue categorization | Customer Service |

##### Quote and Pricing (5)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_CPQ_Quote_Management` | SBQQ__Quote__c (CRUD), SBQQ__QuoteLine__c (CRUD), QuoteApproval__c (RU) | Full quote lifecycle | Customer Service, Sales, Fulfillment |
| `PS_CPQ_Quote_Approval` | SBQQ__Quote__c (RU), QuoteApproval__c (CRUD), Approval_Log__c (CRUD) | Quote approval authority | Sales Team, Management |
| `PS_CPQ_Read_Only` | SBQQ__Quote__c (R), SBQQ__QuoteLine__c (R) | View quotes only | IT Support, Compliance |
| `PS_Pricing_Access` | Pricing_Request__c (CRUD), Quote_Line_History_Tracking__c (R) | Pricing request and calculation | Customer Service, Fulfillment |
| `PS_Multi_Vendor_Pricing` | Pricing_Request__c (RU), Vendor accounts (RU) | Multi-vendor pricing workflows | Fulfillment Team |

##### Operational Management (6)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_Vendor_Management` | Account (vendor RT) (CRUD), SBS_Supplier_Scorecard__c (CRUD) | Vendor relationship management | Fulfillment Team |
| `PS_Approval_Management` | Approval_Log__c (RU), ApprovalImages__c (RU), Service_Approver__c (R) | Approval workflow participation | Sales, Management |
| `PS_Approval_Administration` | Approval_Log__c (CRUD), Service_Approver__c (CRUD), ApprovalImages__c (CRUD) | Approval routing configuration | Administrators |
| `PS_Business_Rules_User` | Business_Rule__c (R), STP_Criteria__c (R) | View business rules | Customer Service, Sales |
| `PS_Business_Rules_Admin` | Business_Rule__c (CRUD), STP_Criteria__c (CRUD) | Configure business rules | Administrators |
| `PS_STP_Administration` | STP_Criteria__c (CRUD), Code_Switch__c (R) | Straight-through processing admin | Administrators |

##### Reporting and Analytics (3)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_Reporting_User` | Report (R), Dashboard (R) | View and run reports | All personas |
| `PS_Reporting_Creator` | Report (CRUD), Dashboard (RU), Folder access | Create custom reports | Reporting Team, Management |
| `PS_Reporting_Admin` | Report (CRUD), Dashboard (CRUD), All folders | Full reporting administration | Reporting Team, Administrators |

##### System and Integration (5)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_Exception_Log_User` | ExceptionLog__c (R), System_Log__c (R), FAST_Activity_Log__c (R) | View error logs for troubleshooting | IT Support |
| `PS_Exception_Log_Admin` | ExceptionLog__c (CRUD), System_Log__c (CRUD), Logging_Framework_Control__c (CRUD) | Configure logging framework | Administrators |
| `PS_Integration_User` | Integration_Process_Manager__c (R), Genesys_Routing__c (R), Genesys_Reporting__c (R) | View integration status | Customer Service, IT Support |
| `PS_Integration_Admin` | Integration_Process_Manager__c (CRUD), API Enabled | Configure integrations | Integration Administrators |
| `PS_Genesys_CTI_User` | Task_Genesys_Routing_Control__c (R), Genesys_Routing__c (R), Genesys_Reporting__c (R) | Genesys contact center access | Customer Service |

##### Administrative (5)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_System_Configuration` | All Config objects (CRUD), Code_Switch__c (CRUD), View Setup | System configuration | Administrators only |
| `PS_Market_Area_Alerts_User` | Market area alert objects (R), notification settings | View and receive alerts | Customer Service, Sales |
| `PS_Market_Area_Alerts_Admin` | MAA_Admin_Settings__c (CRUD), Market_Area_Alerts_Settings__c (CRUD) | Configure market alerts | MAA Admin Team |
| `PS_Knowledge_Author` | Knowledge__kav (CRUD), article types (CRUD) | Create/edit knowledge articles | Subject Matter Experts |
| `PS_Knowledge_Publisher` | Knowledge__kav (CRUD + Publish), article management | Publish knowledge articles | Knowledge Managers |

##### Specialized Functions (4)

| Permission Set Name | Objects Granted | Use Case | Users |
|---------------------|-----------------|----------|-------|
| `PS_Project_Time_Tracking` | Project_Code__c (R), Digital_Transformation_Time_Tracking__c (CRUD) | Time tracking for projects | Project Team, IT Support |
| `PS_Survey_Management` | Survey__c (CRUD) | Survey administration | Marketing, Operations |
| `PS_Organizational_Management` | Department__c (R), Out_of_Office__c (CRUD own), Personal_Queue_Info__c (CRUD own) | Manage personal settings | All users |
| `PS_Premium_Deliveries` | Premium delivery objects (CRUD) | Manage premium service delivery | Operations Team |

**Total Recommended Permission Sets:** 35

---

### 3. Persona-Based Permission Set Groups

Create 8 permission set groups that align to organizational job functions. Each group bundles multiple feature-based permission sets.

#### Naming Convention

All permission set groups follow this format: `PSG_[Persona_Name]`

Examples:
- `PSG_Customer_Service_Representative`
- `PSG_Sales_Team_Member`
- `PSG_Fulfillment_Specialist`

#### Recommended Permission Set Groups

##### PSG_Customer_Service_Representative

**Target Users:** Customer Service Representatives (~50 users)

**Business Functions:**
- Create and manage Cases
- Create and manage Work Orders
- Generate standard Quotes (CPQ)
- Manage Tasks and customer follow-ups
- View Asset availability
- Receive Market Area Alerts

**Included Permission Sets:**
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

**Total Permission Sets:** 13

---

##### PSG_Sales_Team_Member

**Target Users:** Sales Team Members (~15 users)

**Business Functions:**
- Manage escalated Cases
- Create and approve complex Quotes
- Quote approval authority
- Account and relationship management
- Task and opportunity management

**Included Permission Sets:**
1. `PS_Case_Management`
2. `PS_Task_Management`
3. `PS_CPQ_Quote_Management`
4. `PS_CPQ_Quote_Approval` ⭐ (Approval authority)
5. `PS_Pricing_Access`
6. `PS_Asset_Management` (view only via base object access)
7. `PS_Approval_Management`
8. `PS_Communication_Management`
9. `PS_Business_Rules_User`
10. `PS_Market_Area_Alerts_User`
11. `PS_Reporting_User`
12. `PS_Organizational_Management`

**Total Permission Sets:** 12

---

##### PSG_Fulfillment_Specialist

**Target Users:** Fulfillment Team Members (~10 users)

**Business Functions:**
- Quote fulfillment and vendor selection
- Vendor management and scorecarding
- Multi-vendor pricing coordination
- Data quality management
- Timeline and delivery tracking

**Included Permission Sets:**
1. `PS_CPQ_Quote_Management` (fulfillment focus)
2. `PS_Pricing_Access`
3. `PS_Multi_Vendor_Pricing` ⭐ (Vendor pricing)
4. `PS_Vendor_Management` ⭐ (Vendor CRUD)
5. `PS_Task_Management`
6. `PS_Asset_Management`
7. `PS_Work_Order_Management` (view/coordinate)
8. `PS_Communication_Management`
9. `PS_Business_Rules_User`
10. `PS_Reporting_User`
11. `PS_Organizational_Management`

**Total Permission Sets:** 11

---

##### PSG_IT_Support_Member

**Target Users:** IT Support Members (~5 users)

**Business Functions:**
- Read-only troubleshooting in production
- Exception log analysis
- Integration monitoring
- System performance analysis

**Included Permission Sets:**
1. `PS_Exception_Log_User` ⭐ (Primary function)
2. `PS_Integration_User` ⭐ (Monitor integrations)
3. `PS_CPQ_Read_Only`
4. `PS_Reporting_User`
5. `PS_Project_Time_Tracking` (if applicable)
6. `PS_Organizational_Management`

**Note:** Base profile provides read-only access to all objects for troubleshooting. Permission sets grant access to specialized logging and integration objects.

**Total Permission Sets:** 6

---

##### PSG_Compliance_Team_Member

**Target Users:** Compliance Team Members (3-5 users)

**Business Functions:**
- Entitlement and SLA governance
- SOX audit compliance
- Pricing validation and review
- Contract compliance monitoring

**Included Permission Sets:**
1. `PS_Entitlement_Management` ⭐ (Primary function)
2. `PS_CPQ_Read_Only` (Pricing audit)
3. `PS_Approval_Management` (Service approvals)
4. `PS_Business_Rules_User`
5. `PS_Reporting_Creator` ⭐ (Compliance reports)
6. `PS_Organizational_Management`

**Total Permission Sets:** 6

---

##### PSG_System_Administrator

**Target Users:** System Administrators (2-3 users)

**Business Functions:**
- Full system administration
- Configuration management
- User management
- Security administration

**Included Permission Sets:**
1. `PS_System_Configuration` ⭐
2. `PS_Business_Rules_Admin` ⭐
3. `PS_STP_Administration` ⭐
4. `PS_Approval_Administration` ⭐
5. `PS_Exception_Log_Admin` ⭐
6. `PS_Integration_Admin` ⭐
7. `PS_Market_Area_Alerts_Admin`
8. `PS_Knowledge_Publisher`
9. `PS_Reporting_Admin`
10. All user-level permission sets as needed

**Note:** Consider using System Administrator profile for these users instead of minimal access profile.

**Total Permission Sets:** 10+ (or use System Administrator profile)

---

##### PSG_Reporting_Analyst

**Target Users:** Business Analysts and Reporting Team (5-10 users)

**Business Functions:**
- Create custom reports and dashboards
- Data analysis and insights
- Ad-hoc reporting for business units

**Included Permission Sets:**
1. `PS_Reporting_Creator` ⭐
2. `PS_CPQ_Read_Only`
3. `PS_Business_Rules_User`
4. `PS_Organizational_Management`

**Total Permission Sets:** 4

---

##### PSG_Quality_Assurance_Tester

**Target Users:** QA Team (3-5 users)

**Business Functions:**
- UAT testing across all features
- Test data creation
- Defect validation

**Included Permission Sets:**
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

**Note:** QA teams may need temporary access to additional permission sets during specific testing cycles.

**Total Permission Sets:** 10

---

### Permission Set Group Summary

| Permission Set Group | Target Persona | User Count | Permission Sets Included |
|---------------------|----------------|------------|--------------------------|
| `PSG_Customer_Service_Representative` | Customer Service Representatives | ~50 | 13 |
| `PSG_Sales_Team_Member` | Sales Team Members | ~15 | 12 |
| `PSG_Fulfillment_Specialist` | Fulfillment Team Members | ~10 | 11 |
| `PSG_IT_Support_Member` | IT Support Members | ~5 | 6 |
| `PSG_Compliance_Team_Member` | Compliance Team Members | 3-5 | 6 |
| `PSG_System_Administrator` | System Administrators | 2-3 | 10+ |
| `PSG_Reporting_Analyst` | Business Analysts | 5-10 | 4 |
| `PSG_Quality_Assurance_Tester` | QA Team | 3-5 | 10 |

**Total Permission Set Groups:** 8

---

## Role-Based Automation Strategy

### Objective

Automatically assign the appropriate permission set group when a user is assigned a UserRoleId, eliminating manual permission set group assignment and reducing onboarding errors.

### Implementation Approach

Use **Custom Metadata Types** to create a mapping between Salesforce Roles and Permission Set Groups, then implement a **User Trigger** to automatically assign permission set groups based on role selection.

---

### Step 1: Create Custom Metadata Type

**Metadata Type Name:** `Role_Permission_Set_Group_Mapping__mdt`

**Purpose:** Map UserRoleId to Permission Set Group assignments

**Custom Fields:**

| Field Name | Data Type | Description |
|-----------|-----------|-------------|
| Role_Developer_Name__c | Text(255) | Developer Name of the Salesforce Role |
| Permission_Set_Group_Name__c | Text(255) | API name of the Permission Set Group to assign |
| Active__c | Checkbox | Whether this mapping is active |
| Priority__c | Number(2,0) | Priority order if multiple mappings exist (1 = highest) |
| Description__c | Long Text Area | Business description of the mapping |

---

### Step 2: Create Metadata Records

Create metadata records that map each role to the appropriate permission set group:

**Example Metadata Records:**

| Label | Role_Developer_Name__c | Permission_Set_Group_Name__c | Active__c | Priority__c |
|-------|------------------------|------------------------------|-----------|-------------|
| Customer Service Role Mapping | Customer_Service_Representative | PSG_Customer_Service_Representative | ✓ | 1 |
| Sales Team Role Mapping | Sales_Team_Member | PSG_Sales_Team_Member | ✓ | 1 |
| Fulfillment Role Mapping | Fulfillment_Specialist | PSG_Fulfillment_Specialist | ✓ | 1 |
| IT Support Role Mapping | IT_Support_Member | PSG_IT_Support_Member | ✓ | 1 |
| Compliance Role Mapping | Compliance_Team_Member | PSG_Compliance_Team_Member | ✓ | 1 |
| Reporting Analyst Mapping | Reporting_Analyst | PSG_Reporting_Analyst | ✓ | 1 |
| QA Tester Mapping | Quality_Assurance_Tester | PSG_Quality_Assurance_Tester | ✓ | 1 |

---

### Step 3: Create User Trigger and Handler

**File:** `UserTrigger.trigger`

```apex
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

**File:** `UserTriggerHandler.cls`

```apex
public class UserTriggerHandler {

    /**
     * Handle after insert - assign permission set groups based on role
     */
    public static void handleAfterInsert(List<User> newUsers) {
        List<User> usersWithRoles = new List<User>();

        for (User u : newUsers) {
            if (u.UserRoleId != null) {
                usersWithRoles.add(u);
            }
        }

        if (!usersWithRoles.isEmpty()) {
            assignPermissionSetGroups(usersWithRoles);
        }
    }

    /**
     * Handle after update - reassign permission set groups if role changed
     */
    public static void handleAfterUpdate(List<User> newUsers, Map<Id, User> oldMap) {
        List<User> usersWithChangedRoles = new List<User>();

        for (User u : newUsers) {
            User oldUser = oldMap.get(u.Id);
            if (u.UserRoleId != oldUser.UserRoleId) {
                usersWithChangedRoles.add(u);
            }
        }

        if (!usersWithChangedRoles.isEmpty()) {
            // Remove old assignments first
            removePermissionSetGroups(usersWithChangedRoles);
            // Assign new permission set groups
            assignPermissionSetGroups(usersWithChangedRoles);
        }
    }

    /**
     * Assign permission set groups based on role mapping
     */
    @future
    public static void assignPermissionSetGroups(List<User> users) {
        // Get role information for users
        Map<Id, String> userRoleMap = new Map<Id, String>();
        Set<Id> roleIds = new Set<Id>();

        for (User u : users) {
            if (u.UserRoleId != null) {
                roleIds.add(u.UserRoleId);
            }
        }

        if (roleIds.isEmpty()) return;

        // Query roles to get developer names
        Map<Id, UserRole> rolesMap = new Map<Id, UserRole>(
            [SELECT Id, DeveloperName FROM UserRole WHERE Id IN :roleIds]
        );

        // Get metadata mappings
        Map<String, Role_Permission_Set_Group_Mapping__mdt> mappings =
            new Map<String, Role_Permission_Set_Group_Mapping__mdt>();

        for (Role_Permission_Set_Group_Mapping__mdt mapping : [
            SELECT Role_Developer_Name__c, Permission_Set_Group_Name__c, Active__c
            FROM Role_Permission_Set_Group_Mapping__mdt
            WHERE Active__c = true
        ]) {
            mappings.put(mapping.Role_Developer_Name__c, mapping);
        }

        // Get permission set group IDs
        Set<String> psgNames = new Set<String>();
        for (Role_Permission_Set_Group_Mapping__mdt mapping : mappings.values()) {
            psgNames.add(mapping.Permission_Set_Group_Name__c);
        }

        Map<String, Id> psgMap = new Map<String, Id>();
        for (PermissionSetGroup psg : [
            SELECT Id, DeveloperName
            FROM PermissionSetGroup
            WHERE DeveloperName IN :psgNames
        ]) {
            psgMap.put(psg.DeveloperName, psg.Id);
        }

        // Create permission set group assignments
        List<PermissionSetAssignment> assignments = new List<PermissionSetAssignment>();

        for (User u : users) {
            if (u.UserRoleId != null && rolesMap.containsKey(u.UserRoleId)) {
                String roleDeveloperName = rolesMap.get(u.UserRoleId).DeveloperName;

                if (mappings.containsKey(roleDeveloperName)) {
                    String psgName = mappings.get(roleDeveloperName).Permission_Set_Group_Name__c;

                    if (psgMap.containsKey(psgName)) {
                        assignments.add(new PermissionSetAssignment(
                            AssigneeId = u.Id,
                            PermissionSetGroupId = psgMap.get(psgName)
                        ));
                    }
                }
            }
        }

        // Insert assignments if any
        if (!assignments.isEmpty()) {
            try {
                insert assignments;
                System.debug('Successfully assigned ' + assignments.size() + ' permission set groups');
            } catch (DmlException e) {
                System.debug('Error assigning permission set groups: ' + e.getMessage());
                // Log to ExceptionLog__c
            }
        }
    }

    /**
     * Remove permission set group assignments
     */
    @future
    public static void removePermissionSetGroups(List<User> users) {
        Set<Id> userIds = new Set<Id>();
        for (User u : users) {
            userIds.add(u.Id);
        }

        // Query existing permission set assignments for these users
        List<PermissionSetAssignment> existingAssignments = [
            SELECT Id
            FROM PermissionSetAssignment
            WHERE AssigneeId IN :userIds
            AND PermissionSetGroupId != null
        ];

        if (!existingAssignments.isEmpty()) {
            try {
                delete existingAssignments;
                System.debug('Removed ' + existingAssignments.size() + ' permission set group assignments');
            } catch (DmlException e) {
                System.debug('Error removing permission set groups: ' + e.getMessage());
            }
        }
    }
}
```

---

### Step 4: Create Helper Class for Manual Assignment

**File:** `RolePermissionSetGroupHelper.cls`

```apex
public class RolePermissionSetGroupHelper {

    /**
     * Manually assign permission set group based on user role
     * Can be called from Flow or Process Builder
     */
    @InvocableMethod(label='Assign Permission Set Group by Role'
                     description='Assigns permission set group based on user role mapping')
    public static void assignPermissionSetGroupsByRole(List<Id> userIds) {
        List<User> users = [SELECT Id, UserRoleId FROM User WHERE Id IN :userIds];
        UserTriggerHandler.assignPermissionSetGroups(users);
    }

    /**
     * Get recommended permission set group for a role
     */
    public static String getRecommendedPermissionSetGroup(Id roleId) {
        if (roleId == null) return null;

        UserRole role = [SELECT DeveloperName FROM UserRole WHERE Id = :roleId LIMIT 1];

        Role_Permission_Set_Group_Mapping__mdt mapping = [
            SELECT Permission_Set_Group_Name__c
            FROM Role_Permission_Set_Group_Mapping__mdt
            WHERE Role_Developer_Name__c = :role.DeveloperName
            AND Active__c = true
            LIMIT 1
        ];

        return mapping != null ? mapping.Permission_Set_Group_Name__c : null;
    }
}
```

---

### Step 5: Create Flow for Manual Assignment (Optional)

**Flow Name:** `Assign_Permission_Set_Group_by_Role`

**Flow Type:** Screen Flow

**Purpose:** Allow administrators to manually trigger permission set group assignment

**Flow Steps:**
1. Screen: Select Users (multi-select picklist)
2. Action: Call `RolePermissionSetGroupHelper.assignPermissionSetGroupsByRole`
3. Screen: Confirmation message

---

### Alternative Approach: Process Builder or Flow

Instead of a trigger, you can use a **Record-Triggered Flow** on the User object:

**Flow Trigger:**
- Object: User
- Trigger: A record is created or updated
- Condition: UserRoleId is changed

**Flow Actions:**
1. Get Records: Query Role_Permission_Set_Group_Mapping__mdt based on role
2. Get Records: Query PermissionSetGroup based on mapping
3. Create Records: Create PermissionSetAssignment records

**Pros:**
- Declarative approach (clicks not code)
- Easier for administrators to maintain

**Cons:**
- Cannot use @future context (may hit governor limits)
- More complex flow logic required

**Recommendation:** Use Apex trigger approach for production-grade implementation with error handling and logging.

---

### Step 6: Testing Strategy

**Test Class:** `UserTriggerHandlerTest.cls`

```apex
@isTest
private class UserTriggerHandlerTest {

    @testSetup
    static void setup() {
        // Create test role
        UserRole testRole = new UserRole(
            Name = 'Test Customer Service Role',
            DeveloperName = 'Customer_Service_Representative'
        );
        insert testRole;

        // Note: Custom metadata must be created manually or via deployment
        // Cannot create custom metadata in tests
    }

    @isTest
    static void testUserInsertWithRole() {
        UserRole role = [SELECT Id FROM UserRole WHERE DeveloperName = 'Customer_Service_Representative' LIMIT 1];

        // Create test user with role
        Profile p = [SELECT Id FROM Profile WHERE Name='Minimal Access - Organization Standard' LIMIT 1];
        User testUser = new User(
            FirstName = 'Test',
            LastName = 'User',
            Email = 'testuser@example.com',
            Username = 'testuser' + DateTime.now().getTime() + '@example.com',
            Alias = 'tuser',
            TimeZoneSidKey = 'America/Los_Angeles',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US',
            ProfileId = p.Id,
            UserRoleId = role.Id
        );

        Test.startTest();
        insert testUser;
        Test.stopTest();

        // Verify permission set group assignment
        // Note: This will only work if custom metadata records exist
        List<PermissionSetAssignment> assignments = [
            SELECT Id, PermissionSetGroupId
            FROM PermissionSetAssignment
            WHERE AssigneeId = :testUser.Id
            AND PermissionSetGroupId != null
        ];

        // Assert assignment was created
        System.assertNotEquals(0, assignments.size(), 'Permission set group should be assigned');
    }

    @isTest
    static void testUserRoleUpdate() {
        // Create user without role
        Profile p = [SELECT Id FROM Profile WHERE Name='Minimal Access - Organization Standard' LIMIT 1];
        User testUser = new User(
            FirstName = 'Test',
            LastName = 'User',
            Email = 'testuser@example.com',
            Username = 'testuser' + DateTime.now().getTime() + '@example.com',
            Alias = 'tuser',
            TimeZoneSidKey = 'America/Los_Angeles',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US',
            ProfileId = p.Id
        );
        insert testUser;

        // Update user with role
        UserRole role = [SELECT Id FROM UserRole WHERE DeveloperName = 'Customer_Service_Representative' LIMIT 1];
        testUser.UserRoleId = role.Id;

        Test.startTest();
        update testUser;
        Test.stopTest();

        // Verify permission set group assignment
        List<PermissionSetAssignment> assignments = [
            SELECT Id, PermissionSetGroupId
            FROM PermissionSetAssignment
            WHERE AssigneeId = :testUser.Id
            AND PermissionSetGroupId != null
        ];

        System.assertNotEquals(0, assignments.size(), 'Permission set group should be assigned after role update');
    }
}
```

---

### Step 7: Logging and Monitoring

Create a custom object to log permission set group assignments for audit purposes:

**Custom Object:** `Permission_Set_Assignment_Log__c`

**Fields:**
- User__c (Lookup to User)
- Role__c (Lookup to UserRole)
- Permission_Set_Group_Name__c (Text)
- Assignment_Date__c (DateTime)
- Assignment_Type__c (Picklist: Automatic, Manual)
- Status__c (Picklist: Success, Failed)
- Error_Message__c (Long Text Area)

Update the trigger handler to log all assignment attempts.

---

### Benefits of Role-Based Automation

1. **Reduced Onboarding Time:** Automatic permission assignment eliminates manual steps
2. **Consistency:** Every user with the same role gets identical permissions
3. **Auditability:** Clear trail of who received which permissions and when
4. **Error Reduction:** Eliminates human error in permission assignment
5. **Scalability:** Easy to onboard 10 or 100 users with the same role
6. **Flexibility:** Change permissions by updating metadata, not code
7. **Self-Service:** Administrators can create new role mappings via custom metadata

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Objective:** Establish baseline and create minimal access profile

**Tasks:**
1. Document current profile usage and permissions
2. Create `Minimal Access - Organization Standard` profile
3. Define object-level permissions for minimal access profile
4. Test minimal access profile with pilot user
5. Create naming convention documentation

**Deliverables:**
- Current state documentation
- New minimal access profile (deployed to sandbox)
- Naming convention standards document

**Success Criteria:**
- Minimal access profile created and tested
- Baseline documentation complete

---

### Phase 2: Feature Permission Sets (Weeks 3-5)

**Objective:** Create all 35 feature-based permission sets

**Tasks:**
1. Create 7 Core Service Delivery permission sets
2. Create 5 Quote and Pricing permission sets
3. Create 6 Operational Management permission sets
4. Create 3 Reporting and Analytics permission sets
5. Create 5 System and Integration permission sets
6. Create 5 Administrative permission sets
7. Create 4 Specialized Functions permission sets
8. Test each permission set in isolation

**Deliverables:**
- 35 feature-based permission sets (deployed to sandbox)
- Permission set testing documentation
- Permission set assignment matrix

**Success Criteria:**
- All permission sets created and tested
- Each permission set grants exactly the intended access
- No over-permissioning identified

---

### Phase 3: Permission Set Groups (Weeks 6-7)

**Objective:** Create 8 persona-based permission set groups

**Tasks:**
1. Create `PSG_Customer_Service_Representative`
2. Create `PSG_Sales_Team_Member`
3. Create `PSG_Fulfillment_Specialist`
4. Create `PSG_IT_Support_Member`
5. Create `PSG_Compliance_Team_Member`
6. Create `PSG_System_Administrator`
7. Create `PSG_Reporting_Analyst`
8. Create `PSG_Quality_Assurance_Tester`
9. Test each permission set group with pilot users from each persona

**Deliverables:**
- 8 permission set groups (deployed to sandbox)
- Pilot user testing results
- Permission set group documentation

**Success Criteria:**
- All permission set groups created
- Each group tested by representative users
- Feedback incorporated and issues resolved

---

### Phase 4: Role-Based Automation (Weeks 8-9)

**Objective:** Implement automated permission set group assignment

**Tasks:**
1. Create `Role_Permission_Set_Group_Mapping__mdt` custom metadata type
2. Create metadata records for each role-to-permission-set-group mapping
3. Develop `UserTrigger` and `UserTriggerHandler`
4. Develop `RolePermissionSetGroupHelper` class
5. Create `Permission_Set_Assignment_Log__c` custom object
6. Write comprehensive test classes (>90% coverage)
7. Test automation with pilot users
8. Create optional manual assignment flow

**Deliverables:**
- Custom metadata type and records
- Apex trigger and handler classes
- Test classes with full coverage
- Assignment logging custom object
- Automation testing documentation

**Success Criteria:**
- Automation tested and working correctly
- Test coverage >90%
- All edge cases handled (role changes, role removal, etc.)

---

### Phase 5: Pilot Deployment (Weeks 10-11)

**Objective:** Deploy to production with pilot user group

**Tasks:**
1. Select 10-15 pilot users across all personas
2. Deploy minimal access profile to production
3. Deploy all permission sets to production
4. Deploy all permission set groups to production
5. Deploy automation (custom metadata, trigger, handler)
6. Migrate pilot users to new permission model
7. Monitor for 2 weeks
8. Gather feedback from pilot users
9. Address any issues identified

**Deliverables:**
- Production deployment completed
- Pilot user feedback report
- Issues log and resolutions
- Updated documentation based on feedback

**Success Criteria:**
- Pilot users successfully migrated
- No critical issues identified
- Positive feedback from pilot users
- All functionality working as expected

---

### Phase 6: Full Rollout (Weeks 12-14)

**Objective:** Migrate all users to new permission model

**Tasks:**
1. Create communication plan for all users
2. Schedule user migration in batches by persona
   - Week 12: Customer Service Representatives (50 users)
   - Week 13: Sales, Fulfillment, Reporting teams (40 users)
   - Week 14: IT Support, Compliance, QA teams (15 users)
3. Update each user:
   - Change profile to `Minimal Access - Organization Standard`
   - Assign appropriate UserRoleId (triggers automation)
   - Verify permission set group assignment
4. Provide support during migration
5. Monitor for issues

**Deliverables:**
- User communication materials
- Migration runbook
- Support documentation
- Migration completion report

**Success Criteria:**
- All users migrated successfully
- Less than 5% of users require manual intervention
- No critical business disruptions
- Support tickets resolved within 24 hours

---

### Phase 7: Cleanup and Optimization (Weeks 15-16)

**Objective:** Remove legacy profiles and optimize permissions

**Tasks:**
1. Review legacy profiles (17 existing profiles)
2. Archive/deactivate unused legacy profiles
3. Remove any redundant permission assignments
4. Optimize permission set definitions based on usage data
5. Create comprehensive documentation:
   - Administrator guide
   - User onboarding guide
   - Troubleshooting guide
   - Permission matrix reference
6. Deliver training to administrators
7. Establish ongoing governance process

**Deliverables:**
- Legacy profiles deactivated
- Final documentation package
- Administrator training materials
- Governance process document

**Success Criteria:**
- Only 2-3 profiles remain active (Minimal Access, System Administrator, potentially one legacy)
- All documentation complete and accessible
- Administrators trained on new model
- Governance process established

---

### Implementation Timeline Summary

| Phase | Duration | Key Milestone |
|-------|----------|---------------|
| Phase 1: Foundation | Weeks 1-2 | Minimal access profile created |
| Phase 2: Feature Permission Sets | Weeks 3-5 | 35 permission sets created |
| Phase 3: Permission Set Groups | Weeks 6-7 | 8 permission set groups created |
| Phase 4: Role-Based Automation | Weeks 8-9 | Automation implemented and tested |
| Phase 5: Pilot Deployment | Weeks 10-11 | Pilot users migrated successfully |
| Phase 6: Full Rollout | Weeks 12-14 | All users migrated |
| Phase 7: Cleanup and Optimization | Weeks 15-16 | Legacy profiles removed |

**Total Duration:** 16 weeks (approximately 4 months)

---

### Risk Assessment and Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Users lose access to critical functions during migration | High | Medium | Pilot deployment first, batch migration, rollback plan |
| Permission sets don't grant sufficient access | High | Low | Thorough testing in Phase 2-3, pilot user feedback |
| Automation fails to assign permissions | Medium | Low | Comprehensive testing, manual assignment backup |
| Business disruption during migration | High | Low | Migrate in batches by persona, provide support |
| Legacy profiles still referenced in automation | Medium | Medium | Audit all flows, triggers, processes before cleanup |
| Governor limits hit during bulk user migration | Low | Low | Batch migration, use @future methods |
| Resistance to change from users | Medium | Medium | Communication plan, training, support availability |

---

## Appendices

### Appendix A: Current vs. Future State Comparison

| Aspect | Current State | Future State |
|--------|---------------|--------------|
| **Profiles** | 17 profiles with embedded permissions | 1-2 profiles (Minimal Access + System Admin) |
| **Permission Sets** | 31 ad-hoc permission sets | 35 feature-based permission sets |
| **Permission Set Groups** | 0 | 8 persona-based groups |
| **Automation** | Manual assignment | Automatic via UserRoleId |
| **Maintenance** | Update 17 profiles for changes | Update modular permission sets |
| **Onboarding** | Manual profile selection + permission sets | Automatic via role assignment |
| **Audit Trail** | Difficult to trace permissions | Clear permission set group assignments |
| **Scalability** | Difficult to add new features/personas | Easy to add new permission sets/groups |

---

### Appendix B: Salesforce Best Practices References

This strategy is based on official Salesforce guidance and industry best practices:

**Salesforce Official Documentation:**
- [Guidelines for Creating Permission Sets](https://help.salesforce.com/s/articleView?id=platform.perm_sets_best_practices.htm&language=en_US&type=5)
- [Permission Set Group Considerations](https://help.salesforce.com/s/articleView?id=platform.perm_set_groups_considerations.htm&language=en_US&type=5)
- [Permission Set Groups](https://help.salesforce.com/s/articleView?language=en_US&id=sf.perm_set_groups.htm&type=5)
- [Manage Salesforce Object Access](https://trailhead.salesforce.com/content/learn/modules/data_security/data_security_objects)

**Industry Best Practices:**
- [Best Practices for Profile and Permission Set Management (Metazoa)](https://www.metazoa.com/best-practices-profile-permission-set/)
- [Spring '26 Transition from Profiles to Permission Sets (RSM Technology)](https://technologyblog.rsmus.com/technologies/salesforce/spring-26-transition-from-profiles-to-permission-sets-are-you-ready/)
- [Mastering Salesforce Permission Change Management (Blue Canvas)](https://bluecanvas.io/blog/mastering-salesforce-permission-change-management-best-practices-and-tools-for-2024)
- [Admin Best Practices for User Management (Salesforce Admins)](https://admin.salesforce.com/blog/2022/admin-best-practices-for-user-management)
- [Salesforce Permission Sets Guide (Inspire Planner)](https://inspireplanner.com/blog/salesforce-permission-sets-guide/)

**Key Takeaways from Salesforce:**
1. Use minimum access profiles and augment with permission sets
2. Organize permission sets by feature or business function
3. Use permission set groups to represent personas
4. Leverage custom metadata for configuration-driven assignments
5. Plan for the future: Salesforce is moving away from profile-based permissions

---

### Appendix C: Permission Matrix by Persona

Detailed matrix showing which permission sets each persona receives:

[Full matrix available in separate spreadsheet - see `Permission-Matrix-by-Persona.xlsx`]

---

### Appendix D: Glossary

**Profile:** A collection of settings and permissions that define what a user can do in Salesforce. Going forward, profiles should be minimal and augmented with permission sets.

**Permission Set:** A collection of settings and permissions that extend users' functional access without changing their profile.

**Permission Set Group:** A bundle of permission sets that can be assigned to users as a single unit. Represents a "persona" or job function.

**Minimal Access Profile:** A profile that provides only baseline read-only access to the platform. All additional access is granted via permission sets.

**Feature-Based Permission Set:** A permission set organized around a specific business capability (e.g., Case Management, CPQ Quotes).

**Persona-Based Permission Set Group:** A permission set group that represents a job function (e.g., Customer Service Representative) and contains all permission sets needed for that role.

**Custom Metadata Type:** A Salesforce metadata type that can be used to store configuration data that can be queried at runtime. Used for the role-to-permission-set-group mapping.

**UserRoleId:** The Salesforce Role assigned to a user. Used as the trigger for automated permission set group assignment.

**CRUD:** Create, Read, Update, Delete - the four basic operations for database records.

**FLS:** Field-Level Security - controls which fields users can view and edit.

**OWD:** Organization-Wide Defaults - the baseline record access level for each object.

---

### Appendix E: Quick Reference: Permission Set Naming

All permission sets follow this format: `PS_[Feature_Area]_[Access_Level]`

**Examples:**
- `PS_Case_Management` - Full case management
- `PS_CPQ_Quote_Management` - Full quote management
- `PS_Business_Rules_Admin` - Business rules administration
- `PS_Exception_Log_User` - View exception logs
- `PS_Reporting_Creator` - Create custom reports

**Permission Set Groups:** `PSG_[Persona_Name]`

**Examples:**
- `PSG_Customer_Service_Representative`
- `PSG_Sales_Team_Member`
- `PSG_Fulfillment_Specialist`

---

### Appendix F: Support and Escalation

**For Implementation Questions:**
- Primary Contact: George Martin, Salesforce Technical Architect
- Secondary Contact: Salesforce System Administrator team

**For Production Issues:**
- Tier 1: Internal Help Desk
- Tier 2: Salesforce Administrator
- Tier 3: Technical Architect

**For Permission Requests:**
- Submit request via [internal ticketing system]
- Include: User name, role, business justification
- SLA: 2 business days for standard requests

---

## Document Metadata

**Document Title:** Salesforce Permission Strategy Analysis
**Version:** 1.0
**Date Created:** January 19, 2026
**Author:** Claude (AI Assistant) in collaboration with George Martin
**Status:** DRAFT - Pending Review
**Next Review Date:** TBD
**Related Documents:**
- User-Group-Reference.md
- Claude.md (Architecture Documentation)
- Permission-Matrix-by-Persona.xlsx (to be created)

---

**END OF PERMISSION STRATEGY ANALYSIS**
