# System Architecture Documentation

## Executive Summary

This is a **mature, enterprise-scale Salesforce DX implementation** supporting comprehensive business operations across case management, work order processing, quoting/pricing, and service delivery. The system leverages a configuration-driven architecture with 699 Apex classes, 247 UI components (Aura and LWC), 95 automated flows, and 100+ custom objects to deliver complex business functionality.

**Project Details:**
- **Project Name:** SFDX2024Project (2026 Technical Projects)
- **Platform:** Salesforce DX with Lightning Experience
- **API Version:** 61.0 (Fall 2023)
- **Repository:** Git-based source control
- **Development Model:** Source-driven development with scratch org support

---

## Technology Stack

### Frontend Technologies

| Technology | Count | Purpose | Status |
|-----------|-------|---------|--------|
| **Lightning Web Components (LWC)** | 42 components | Modern component framework for Lightning Experience | Active Development |
| **Aura Components** | 205 components | Legacy component framework (pre-LWC) | Maintenance Mode |
| **Visualforce Pages** | 12 pages | Server-side rendered pages for specific use cases | Legacy Support |
| **Visualforce Components** | 42 components | Reusable Visualforce components | Legacy Support |

**Key Frontend Patterns:**
- Event-driven communication using `pubsub` utility (LWC)
- Custom date pickers and pagination components
- Reusable card-based UI components
- Domain-prefixed naming (aav*, pricing*, quote*, case*)

### Backend Technologies

| Technology | Count | Purpose |
|-----------|-------|---------|
| **Apex Classes** | 699 classes | Server-side business logic, API services, controllers |
| **Apex Triggers** | 32 triggers | Database event handlers across major objects |
| **Platform Events** | 96+ events | Event-driven asynchronous processing |
| **Batch Jobs** | 50+ classes | Asynchronous processing and data management |

### Automation & Configuration

| Type | Count | Description |
|-----|-------|-------------|
| **Cloud Flows** | 95 flows | Declarative automation and business processes |
| **Custom Metadata Types** | 3,034 records | Configuration-driven behavior and business rules |
| **Email Templates** | 381 templates | Organized across 16+ functional domains |
| **Page Layouts** | 178 layouts | UI field organization for various profiles |

### Data Model

| Type | Count | Notes |
|-----|-------|-------|
| **Custom Objects** | 100+ objects | Business-specific data entities |
| **Extended Standard Objects** | 30+ objects | Customizations to Account, Case, Asset, WorkOrder, etc. |
| **Custom Fields** | Thousands | Across all objects |

---

## Architecture Patterns

### 1. Configuration-Driven Architecture

The system heavily leverages Custom Metadata Types for runtime configuration, enabling business users to modify behavior without code changes:

**Key Metadata Types:**
- `Business_Rule_Field_Mapping__mdt` - Dynamic field mapping configurations
- `Task_Framework__mdt` - Task creation and assignment rules
- `WOCreation__mdt` - Work order creation configuration
- `Case_Highlight_Panel_Button__mdt` - UI button visibility and behavior
- `PricingJsonSetting__mdt` - Pricing engine configuration

**Benefits:**
- Reduced code deployment frequency
- Business-user empowerment for configuration changes
- Environment-agnostic settings (portable across orgs)
- Rapid feature toggles and A/B testing

### 2. Event-Driven Processing

Platform Events enable loosely-coupled, asynchronous communication between system components:

**Key Platform Events:**
- `STPProcessEvent__e` - Straight-through processing automation
- `Task_and_Genesys_Platform_Event__e` - CTI integration events
- `System_Log_Event__e` - Centralized logging infrastructure
- `CasetoQuoteAutomation__e` - Cross-domain automation

**Architecture Benefits:**
- Decoupled components
- Scalable processing
- Failure recovery mechanisms
- Audit trail generation

### 3. Trigger Framework Pattern

The system implements a structured trigger handler pattern to manage complex business logic:

**Pattern Structure:**
```
Trigger (AccountTrigger.trigger)
  → Handler (AccountTriggerHandler.cls)
    → Helper (AccountTriggerHelper.cls)
      → Business Logic Classes
```

**Identified Triggers:**
- `AccountContactRelationTrigger` - Relationship management
- `AssetTrigger` - Asset lifecycle events
- `BusinessRuleTrigger` - Business rule engine
- `CaseAssetTrigger` - Case-asset associations
- `CaseCommentTrigger` - Comment processing
- `WorkOrderTrigger` - Work order automation
- `PricingRequestTrigger` - Quote/pricing initiation

### 4. Service-Oriented Architecture (SOA)

The system exposes multiple integration points through web services:

**API Layers:**
- REST Resources (AcornCaseDetailsResource.cls)
- SOAP Web Services (IVRServiceStatusWebService.cls)
- Custom HTTP callouts (configured via remoteSiteSettings)

### 5. Multi-Tenant Data Isolation

Standard Salesforce sharing rules, profiles, and permission sets ensure:
- Role-based access control (RBAC)
- Field-level security (FLS)
- Record-level sharing rules
- Profile-specific page layouts

---

## Directory Structure

### Root Directory Layout

```
/2026TechnicalProjects/
├── .git/                          # Git repository metadata
├── .github/                        # GitHub workflows and CI/CD
├── .vscode/                        # VS Code project settings
│   ├── extensions.json            # Recommended extensions
│   └── settings.json              # Workspace configuration
├── config/                         # Salesforce configuration
│   └── project-scratch-def.json   # Scratch org definition
├── force-app/                      # Main application source (see below)
├── manifest/                       # Deployment manifests
│   └── package.xml                # Complete metadata inventory
├── scripts/                        # Utility scripts
│   ├── apex/                      # Anonymous Apex templates
│   └── soql/                      # SOQL query templates
├── package.json                    # Node.js dependencies and scripts
├── sfdx-project.json              # SFDX project configuration
├── README.md                       # Project documentation
├── Claude.md                       # This file - architecture documentation
├── .gitignore                      # Git exclusions
├── .eslintignore                   # ESLint exclusions
├── .forceignore                    # Force.com deployment exclusions
├── .prettierignore                 # Prettier formatter exclusions
└── .prettierrc                     # Prettier configuration
```

### Core Application Structure

The `force-app/main/default/` directory contains all Salesforce metadata organized by type:

#### User Interface Tier

```
force-app/main/default/
├── lwc/                           # Lightning Web Components (42)
│   ├── pubsub/                    # Event bus utility library
│   ├── aavAlternateContainers/    # Asset availability containers
│   ├── aavAppOutputPanel/         # Application output displays
│   ├── pricingOutputScreen/       # Quote pricing UI
│   ├── quoteSummaryComp/          # Quote summary displays
│   ├── multiVendorPricingResponse/# Multi-vendor pricing
│   ├── alertCard/                 # Alert management UI
│   └── [39 additional components]
├── aura/                          # Aura Components (205) - Legacy
│   ├── ShowTeamsOpenTask/
│   ├── QuoteOverview/
│   ├── CustomCaseTemplate/
│   └── [202 additional components]
├── pages/                         # Visualforce Pages (12)
│   ├── ChatTranscriptPdf.page
│   └── [11 additional pages]
└── components/                    # Visualforce Components (42)
```

#### Business Logic Tier

```
force-app/main/default/
├── classes/                       # Apex Classes (699)
│   ├── Controllers/
│   │   ├── MarketAreaAlertController.cls
│   │   ├── VendorEscalationContactController.cls
│   │   └── [100+ controllers]
│   ├── Helpers/
│   │   ├── BusinessRuleHelper.cls
│   │   ├── TaskTriggerHelper.cls
│   │   └── [100+ helpers]
│   ├── Handlers/
│   │   ├── AccountTriggerHandler.cls
│   │   ├── CaseTriggerHandler.cls
│   │   └── [30+ handlers]
│   ├── Batch Jobs/
│   │   ├── BATCH_PurgeOldException.cls
│   │   ├── BatchToDeleteCase.cls
│   │   └── [50+ batch jobs]
│   ├── Utilities/
│   │   ├── Logger.cls
│   │   ├── MapSortService.cls
│   │   └── [utility classes]
│   ├── Web Services/
│   │   ├── IVRServiceStatusWebService.cls
│   │   ├── ANIMatchWebservices.cls
│   │   └── [API endpoints]
│   └── Tests/
│       └── [*Test.cls files]
└── triggers/                      # Apex Triggers (32)
    ├── AccountContactRelationTrigger.trigger
    ├── AssetTrigger.trigger
    ├── BusinessRuleTrigger.trigger
    ├── CaseAssetTrigger.trigger
    ├── WorkOrderTrigger.trigger
    └── [27 additional triggers]
```

#### Automation & Configuration Tier

```
force-app/main/default/
├── flows/                         # Cloud Flows (95)
│   ├── Business_Rule_Selection.flow-meta.xml
│   ├── Create_Business_Task_Notification.flow-meta.xml
│   ├── Task_Framework_Process_To_Create_Case.flow-meta.xml
│   └── [92 additional flows]
├── customMetadata/                # Custom Metadata Types (3,034 records)
│   ├── Business_Rule_Field_Mapping__mdt/
│   ├── Task_Framework__mdt/
│   ├── WOCreation__mdt/
│   └── [additional metadata types]
├── workflows/                     # Legacy Workflow Rules
└── approvalProcesses/            # Approval processes
```

#### Data Model Tier

```
force-app/main/default/
└── objects/                       # Objects (219 total)
    ├── Account/                   # Standard object extensions
    │   ├── fields/
    │   ├── listViews/
    │   ├── compactLayouts/
    │   └── recordTypes/
    ├── Case/
    ├── WorkOrder/
    ├── Asset/
    ├── Business_Rule__c/          # Custom objects
    ├── Case_Task_Tracker__c/
    ├── Approval_Log__c/
    └── [100+ custom objects]
```

#### UI Configuration Tier

```
force-app/main/default/
├── layouts/                       # Page Layouts (178)
│   ├── Account-Account Layout.layout-meta.xml
│   ├── Case-Case Layout.layout-meta.xml
│   └── [176 additional layouts]
├── flexipages/                    # Lightning Pages
├── quickActions/                  # Quick Actions
├── homePageLayouts/               # Homepage configurations
└── pathAssistants/                # Sales/Service paths
```

#### Email & Communication

```
force-app/main/default/
└── email/                         # Email Templates (381)
    ├── Case_Email_Templates/
    ├── CE_Core_Email/
    ├── Quote_Request_for_Bid/
    ├── SSM_Change_Email_Templates/
    └── [16+ template folders]
```

#### Reporting & Analytics

```
force-app/main/default/
├── reports/                       # Reports (14)
│   ├── Work_Order_Reports/
│   └── System_Administrator_Reports/
└── dashboards/                    # Dashboards (1)
```

#### Security & Governance

```
force-app/main/default/
├── profiles/                      # User profiles
├── permissionsets/                # Permission sets
├── permissionsetgroups/           # Permission set groups
├── sharingRules/                  # Record sharing rules
└── roles/                         # Organizational roles
```

#### Integration & External Access

```
force-app/main/default/
├── remoteSiteSettings/            # HTTP callout endpoints
├── messageChannels/               # Lightning Message Service channels
└── notificationtypes/             # Custom notifications
```

#### Static Resources

```
force-app/main/default/
└── staticresources/
    ├── jquerydatepicker/          # jQuery UI components
    ├── slds/                      # Salesforce Lightning Design System
    │   ├── styles/
    │   ├── icons/
    │   └── assets/
    └── [design system assets]
```

---

## Key Components and Functionality

### Business Domains

The system supports multiple interconnected business domains:

#### 1. Case and Work Order Management
- **Primary Objects:** Case, WorkOrder, Asset, ServiceContract
- **Key Features:**
  - Case lifecycle automation
  - Work order creation and dispatch
  - Asset tracking and maintenance
  - Service contract management
  - SLA tracking and escalation

**Key Components:**
- `CaseTrigger`, `WorkOrderTrigger`, `AssetTrigger`
- `CaseTriggerHelper`, `WorkOrderTriggerHelper`
- Case email templates (50+ templates)
- Case highlight panels and quick actions

#### 2. Quote and Pricing Management
- **Primary Objects:** Quote, QuoteLine, PricingRequest, Order
- **Key Features:**
  - Multi-vendor pricing engine
  - Quote approval workflows
  - Automated pricing calculations
  - Quote-to-order conversion
  - Request for Bid (RFB) automation

**Key Components:**
- `PricingRequestTrigger`
- `pricingOutputScreen` (LWC)
- `multiVendorPricingResponse` (LWC)
- `quoteSummaryComp` (LWC)
- Quote email templates (30+ templates)

#### 3. Task and Assignment Management
- **Primary Objects:** Task, Case_Task_Tracker__c
- **Key Features:**
  - Configuration-driven task creation (`Task_Framework__mdt`)
  - Automated task assignment
  - Task lifecycle tracking
  - Out-of-office task reassignment
  - Task completion workflows

**Key Components:**
- `TaskTrigger`, `TaskTriggerHelper`
- `OutofOfficeTriggerHelper`
- Task Framework flows
- Task email notifications

#### 4. Business Rules Engine
- **Primary Objects:** Business_Rule__c, Business_Rule_Field_Mapping__mdt
- **Key Features:**
  - Dynamic rule evaluation
  - Field mapping configuration
  - Multi-criteria rule matching
  - Rule-based automation triggers

**Key Components:**
- `BusinessRuleTrigger`, `BusinessRuleHelper`
- Business Rule Selection flow
- Custom metadata-driven configuration

#### 5. Vendor and Asset Management
- **Primary Objects:** Account (Vendors), Asset, Contract
- **Key Features:**
  - Vendor qualification and management
  - Asset lifecycle tracking
  - Vendor escalation contacts
  - Multi-vendor coordination

**Key Components:**
- `VendorEscalationContactController`
- Asset Availability Views (AAV)
- Vendor pricing integration

#### 6. Service Approvals
- **Primary Objects:** Approval_Log__c, Service_Approver__c
- **Key Features:**
  - Multi-level approval workflows
  - Approval history tracking
  - Approval delegation
  - SLA-based escalation

**Key Components:**
- `Approval_Log` flow
- Approval email templates
- Custom approval UI components

#### 7. Email and Communication Management
- **Primary Objects:** EmailMessage, SFDCEmailMessage__c
- **Key Features:**
  - 381 email templates across domains
  - Email-to-case processing
  - Chat transcript archival
  - Email threading and tracking

**Key Components:**
- `ChatTranscriptPdf` Visualforce page
- Email template folders organized by domain
- Email message tracking custom object

---

## Data Model Overview

### Custom Objects (Primary Entities)

**Core Business Objects:**
- `Business_Rule__c` - Configurable business rules
- `Case_Task_Tracker__c` - Task tracking and metrics
- `Approval_Log__c` - Approval history
- `Service_Status__c` - Service delivery status
- `Service_Approver__c` - Approval workflow participants
- `SFDCEmailMessage__c` - Email message tracking
- `STP_Criteria__c` - Straight-through processing criteria

**Asset and Service Objects:**
- `AAV_*` prefix - Asset Availability Views
- `AC_*` prefix - Asset Configuration
- Various work order and service delivery objects

**Quote and Pricing Objects:**
- `SBQQ_*` prefix - Salesforce CPQ (Quote-to-Cash) extensions
- Custom pricing configuration objects
- Multi-vendor pricing objects

### Standard Objects (Extended)

**Heavily Customized Standard Objects:**
- **Account** - Customer and vendor management (50+ custom fields)
- **Case** - Service request and incident management (100+ fields)
- **WorkOrder** - Field service work orders (75+ fields)
- **Asset** - Equipment and product tracking (50+ fields)
- **Contact** - Person accounts and relationships (40+ fields)
- **Task** - Activities and assignments (30+ fields)
- **ServiceContract** - Service agreements (25+ fields)
- **Quote/Opportunity** - Quote and sales tracking

### Data Relationships

The system implements complex many-to-many relationships through junction objects:
- Case ↔ Asset (via CaseAsset junction)
- Account ↔ Contact (via AccountContactRelation)
- Case ↔ Task (via Case_Task_Tracker__c)
- Quote ↔ Products (via QuoteLine)

### Custom Metadata Types (Configuration Objects)

**Configuration-Driven Entities (3,034 records):**
- Business rule mappings
- Task framework configurations
- Work order creation settings
- UI component configurations
- Integration settings
- Email notification rules
- Pricing calculation parameters

---

## Integration Points

### External System Integrations

#### 1. Genesys CTI Integration
**Purpose:** Computer Telephony Integration for call center operations

**Components:**
- `Task_and_Genesys_Platform_Event__e` - Event-based integration
- `BatchToCreateGenesysForPITasks` - Batch processing for task creation
- `ANIMatchWebservices.cls` - Automatic Number Identification matching

**Data Flow:**
```
Genesys Call Center → Platform Event → Task Creation → Case Assignment
```

#### 2. Acorn Field Service Integration
**Purpose:** Field service management system integration

**Components:**
- `AcornCaseDetailsResource.cls` - REST API endpoint
- Work order synchronization
- Asset status updates

**Data Flow:**
```
Work Order Created → Acorn Dispatch → Field Technician → Status Update → Case Resolution
```

#### 3. IVR Service Status Integration
**Purpose:** Interactive Voice Response system for service status

**Components:**
- `IVRServiceStatusWebService.cls` - SOAP web service
- Service status lookup APIs

**Data Flow:**
```
Customer Call → IVR Query → Service Status Lookup → Automated Response
```

#### 4. Quote-to-Cash (SBQQ) Integration
**Purpose:** Salesforce CPQ (Configure, Price, Quote) integration

**Components:**
- 100+ custom fields on `SBQQ__QuoteLine__c`
- Multi-vendor pricing workflows
- Quote approval automation
- Order creation processes

**Data Flow:**
```
Case → RFB Creation → Vendor Pricing → Quote Generation → Approval → Order
```

### API Endpoints

**Exposed Web Services:**
- REST Resources for external system access
- SOAP Web Services for legacy integrations
- Platform Events for real-time event streaming
- Remote Site Settings configured for HTTP callouts

---

## Development Workflow

### Local Development Setup

**Prerequisites:**
1. Salesforce CLI (SFDX)
2. Node.js and npm
3. VS Code with Salesforce Extensions
4. Git

**Initial Setup:**
```bash
# Clone repository
git clone <repository-url>
cd 2026TechnicalProjects

# Install Node.js dependencies
npm install

# Authenticate to Dev Hub
sfdx auth:web:login --setdefaultdevhubusername --setalias DevHub

# Create scratch org
sfdx force:org:create -f config/project-scratch-def.json -a MyScratchOrg --setdefaultusername

# Push source to scratch org
sfdx force:source:push

# Open scratch org
sfdx force:org:open
```

### Code Quality Tools

#### ESLint Configuration
**Validates:** JavaScript, LWC, and Aura components

**Rules:**
- `@salesforce/eslint-config-lwc` - LWC-specific best practices
- `@salesforce/eslint-plugin-aura` - Aura component validation
- `eslint-plugin-import` - Import/export validation
- `eslint-plugin-jest` - Test file validation

**Run Linting:**
```bash
npm run lint
```

#### Prettier Configuration
**Formats:** JavaScript, Apex, XML, HTML, CSS, Markdown

**Settings:**
- No trailing commas (Apex convention)
- LWC HTML uses "lwc" parser
- Consistent code style across all file types

**Run Formatting:**
```bash
# Check formatting
npm run prettier:verify

# Auto-format all files
npm run prettier
```

#### Pre-commit Hooks (Husky)
**Automatically runs on `git commit`:**
- ESLint validation on staged files
- Prettier formatting check
- Optional: Jest test execution

**Configuration:** `.husky/` directory

### Testing Strategy

#### LWC Jest Testing
**Framework:** `@salesforce/sfdx-lwc-jest`

**Test Commands:**
```bash
# Run all tests
npm run test

# Run tests in watch mode (TDD)
npm run test:unit:watch

# Run tests with coverage
npm run test:unit:coverage

# Debug tests
npm run test:unit:debug
```

**Test Location:** `force-app/main/default/lwc/[component]/__tests__/`

#### Apex Testing
**Best Practices:**
- Test classes named `[ClassName]Test.cls`
- Minimum 75% code coverage required for deployment
- Test data factory patterns for reusable test data
- Use `@isTest` annotation on test classes

**Run Apex Tests:**
```bash
# Run all tests
sfdx force:apex:test:run --codecoverage --resultformat human

# Run specific test class
sfdx force:apex:test:run --classnames AccountTriggerHandlerTest --codecoverage
```

### Deployment Process

#### Source-Driven Deployment (Recommended)

**Deploy to Scratch Org:**
```bash
sfdx force:source:push
```

**Deploy to Sandbox/Production:**
```bash
# Deploy specific components
sfdx force:source:deploy --sourcepath force-app/main/default/classes

# Deploy using manifest
sfdx force:source:deploy --manifest manifest/package.xml

# Validate deployment (checkonly)
sfdx force:source:deploy --manifest manifest/package.xml --checkonly --testlevel RunLocalTests
```

#### Package-Based Deployment

**Using package.xml:**
```bash
# Retrieve metadata
sfdx force:mdapi:retrieve --retrievetargetdir mdapi --unpackaged manifest/package.xml

# Deploy metadata
sfdx force:mdapi:deploy --deploydir mdapi --testlevel RunLocalTests
```

### Version Control Strategy

**Branch Strategy:**
- `main` - Production-ready code
- `claude/[feature]-[id]` - Feature development branches
- Regular commits with descriptive messages

**Git Workflow:**
```bash
# Create feature branch
git checkout -b claude/my-feature-abc123

# Stage changes
git add .

# Commit changes
git commit -m "Add: description of changes"

# Push to remote
git push -u origin claude/my-feature-abc123
```

### Debugging Tools

**VS Code Extensions (Recommended):**
- Salesforce Extension Pack
- Salesforce CLI Integration
- FinancialForce LANA (advanced debugging)
- RedHat XML support
- ESLint and Prettier plugins

**Debug Logs:**
```bash
# Stream debug logs
sfdx force:apex:log:tail

# Get specific log
sfdx force:apex:log:get --logid <log-id>
```

---

## Code Quality and Standards

### Naming Conventions

#### Apex Classes
- **Controllers:** `[Name]Controller.cls` or `[Name]Ctrl.cls`
  - Example: `MarketAreaAlertController.cls`
- **Helpers:** `[Trigger/Object]Helper.cls`
  - Example: `TaskTriggerHelper.cls`
- **Handlers:** `[Trigger]Handler.cls`
  - Example: `AccountTriggerHandler.cls`
- **Batch Jobs:** `Batch[Description].cls` or `BATCH_[Description].cls`
  - Example: `BATCH_PurgeOldException.cls`
- **Test Classes:** `[ClassName]Test.cls`
  - Example: `AccountTriggerHandlerTest.cls`
- **Utilities:** `[Functional]Service.cls` or `[Functional]Utility.cls`
  - Example: `MapSortService.cls`

#### Lightning Web Components
- **Domain Prefixes:** `aav*`, `pricing*`, `quote*`, `case*`, `alert*`
  - Example: `aavAlternateContainers`, `pricingOutputScreen`
- **Naming Style:** camelCase
  - Example: `changeRTCard`, `multiAssetCaseCard`
- **Reusable Utilities:** Descriptive names
  - Example: `pubsub`, `aavUtilityMethods`, `aavReusablePagination`

#### Custom Objects
- **Custom Objects:** `[Name]__c`
  - Example: `Business_Rule__c`
- **Metadata Types:** `[Name]__mdt`
  - Example: `Task_Framework__mdt`
- **Platform Events:** `[Name]__e`
  - Example: `Task_and_Genesys_Platform_Event__e`
- **Domain Prefixes:** `AAV_`, `AC_`, `SBS_`, `SBQQ_`, `STP_`

#### Flows
- **Naming Style:** Snake_case with underscores
  - Example: `Create_Business_Task_Notification.flow`
- **Descriptive Names:** Include action and target
  - Example: `Task_Framework_Process_To_Create_Case`

### Best Practices

#### Apex Code
1. **Bulkification:** Always write bulkified code for triggers and batch operations
2. **Governor Limits:** Be mindful of SOQL queries (100), DML statements (150), heap size (6MB)
3. **Error Handling:** Use try-catch blocks and log exceptions appropriately
4. **Test Coverage:** Maintain >75% code coverage, aim for >85%
5. **Security:** Always check FLS and CRUD permissions
6. **Separation of Concerns:** Controllers should delegate to helper/service classes

#### Lightning Web Components
1. **Component Design:** Keep components small and focused on single responsibility
2. **Event Communication:** Use standard Lightning Message Service or custom events
3. **Property Decorators:** Use `@api`, `@track`, and `@wire` appropriately
4. **Error Handling:** Display user-friendly error messages with `lightning-toast`
5. **Accessibility:** Follow SLDS guidelines and ARIA standards
6. **Testing:** Write comprehensive Jest tests for all components

#### Configuration-Driven Development
1. **Custom Metadata:** Use custom metadata types for configurable business logic
2. **Hard-coding Avoidance:** Externalize configuration values
3. **Environment Portability:** Ensure configurations work across all orgs
4. **Documentation:** Document metadata type purpose and field usage

---

## Configuration Management

### Scratch Org Configuration

**File:** `config/project-scratch-def.json`

**Settings:**
- **Edition:** Developer
- **Features:** PasswordRequirementApi
- **Organization Name:** Demo company
- **Lightning Experience:** Enabled
- **Mobile Settings:** S1 encryption disabled for development

**Purpose:** Consistent scratch org creation for development and testing

### Deployment Manifest

**File:** `manifest/package.xml` (~515KB)

**Contents:**
- Complete inventory of all 10,000+ metadata components
- Organized by metadata type (ApexClass, ApexTrigger, LightningComponentBundle, etc.)
- Used for full org deployments and metadata tracking

**Usage:**
- Source control comparison
- Full org deployments
- Metadata dependency resolution

### Environment Variables

**Excluded Files (`.gitignore`):**
- `.env` - Environment-specific settings
- `.sf/` - Salesforce CLI cache
- `.sfdx/` - SFDX configuration cache

**Best Practice:** Use Custom Metadata Types instead of environment variables for Salesforce-specific configuration

### Remote Site Settings

**Purpose:** Configure HTTP callout endpoints for external integrations

**Configuration:** `force-app/main/default/remoteSiteSettings/`

**Security:** Ensure only trusted external endpoints are whitelisted

---

## System Performance Considerations

### Scalability Patterns

#### 1. Asynchronous Processing
- **Batch Jobs:** 50+ batch classes for large data processing
- **Queueable Apex:** Chained processing for complex workflows
- **Platform Events:** Event-driven asynchronous communication
- **Future Methods:** Simple asynchronous callouts

#### 2. Query Optimization
- Use selective filters in SOQL queries
- Leverage indexed fields (standard fields, external IDs, unique fields)
- Avoid SOQL in loops
- Use SOQL FOR loops for large data sets

#### 3. Caching Strategies
- Custom Metadata Types (cached by platform)
- Custom Settings for org-wide defaults
- Platform cache for frequently accessed data

#### 4. Governor Limit Management
- Bulkified trigger design
- Batch processing for large datasets
- Selective query patterns
- DML optimization

---

## Security Architecture

### Multi-Layer Security Model

#### 1. Object-Level Security
- **Profiles:** Define base object permissions (CRUD)
- **Permission Sets:** Grant additional permissions
- **Permission Set Groups:** Logical grouping of permission sets

#### 2. Field-Level Security
- Sensitive field access controlled per profile
- Field encryption for PII and sensitive data
- Field audit trail enabled on critical fields

#### 3. Record-Level Security
- Organization-Wide Defaults (OWD)
- Role hierarchy for data access
- Sharing rules for extended access
- Manual sharing for ad-hoc access

#### 4. Application Security
- Lightning Locker Service for component isolation
- CSP (Content Security Policy) for XSS protection
- CRUD/FLS checks in Apex code
- Input validation and sanitization

---

## Monitoring and Observability

### Logging Infrastructure

**System Log Events:** `System_Log_Event__e`
- Centralized logging via platform events
- Async processing of log entries
- Log retention and archival

**Debug Logs:**
- User-based trace flags for debugging
- Log filters for performance tuning
- Event Monitoring for production tracking

### Performance Monitoring

**Key Metrics:**
- API call volume and latency
- Apex execution time
- SOQL query performance
- Page load times (Lightning Experience)

**Tools:**
- Event Monitoring (requires add-on license)
- Developer Console for real-time debugging
- Setup Audit Trail for configuration changes

---

## Migration and Data Management

### Data Migration Patterns

1. **Bulk API:** For large-scale data loads (>50,000 records)
2. **REST API:** For real-time integrations
3. **Data Loader:** For scheduled imports/exports
4. **External Objects:** For real-time external data access (without import)

### Data Archival Strategy

- Batch jobs for purging old records (`BATCH_PurgeOldException`)
- Retention policies based on business requirements
- Big Objects for long-term data retention (if configured)

---

## Future Considerations

### Technical Debt and Modernization

#### 1. Aura to LWC Migration
**Current State:** 205 Aura components, 42 LWC components

**Recommendation:**
- Prioritize high-traffic components for migration
- Create LWC equivalents for shared Aura utilities
- Establish migration roadmap with business priorities
- Leverage LWC Local Development for faster iteration

#### 2. Flow Optimization
**Current State:** 95 Cloud Flows

**Recommendation:**
- Review flow performance (identify slow flows)
- Consolidate duplicate logic
- Implement flow testing framework
- Document flow dependencies and trigger orders

#### 3. Custom Metadata Expansion
**Opportunity:**
- Identify hard-coded values in Apex
- Extract configuration to custom metadata
- Enable business user self-service
- Improve deployment portability

#### 4. API Modernization
**Current State:** Mix of REST and SOAP web services

**Recommendation:**
- Standardize on REST APIs for new integrations
- Implement API versioning strategy
- Add comprehensive error handling
- Create API documentation (OpenAPI/Swagger)

### Observability Enhancements

1. **Centralized Logging Dashboard**
   - Build reports and dashboards on `System_Log_Event__e`
   - Alert on error thresholds
   - Track integration failures

2. **Performance Metrics**
   - Custom metrics for business-critical processes
   - End-to-end transaction tracing
   - Capacity planning analytics

3. **Integration Monitoring**
   - Health check endpoints for external systems
   - Automated integration testing
   - Failure notification and escalation

### Documentation Roadmap

**Recommended Documentation Additions:**

1. **Data Model ERD**
   - Entity-relationship diagram for custom objects
   - Relationship cardinality and dependencies
   - Key field descriptions

2. **Trigger and Flow Execution Order**
   - Document order of execution for each object
   - Identify potential recursion issues
   - Optimization opportunities

3. **LWC Component Dependency Graph**
   - Visual representation of component relationships
   - Shared utility usage
   - Parent-child component hierarchies

4. **Custom Metadata Configuration Schema**
   - Purpose of each metadata type
   - Field descriptions and valid values
   - Configuration examples by business scenario

5. **API Documentation**
   - REST API endpoints and contracts
   - Request/response examples
   - Authentication and authorization
   - Error codes and handling

6. **Deployment Runbooks**
   - Pre-deployment checklist
   - Deployment steps by environment
   - Rollback procedures
   - Post-deployment validation

7. **Business Process Documentation**
   - Case management workflow
   - Quote-to-cash process flow
   - Work order lifecycle
   - Approval routing logic

---

## Appendix

### Key Configuration Files Reference

| File | Purpose | Location |
|------|---------|----------|
| `sfdx-project.json` | SFDX project configuration | Root directory |
| `project-scratch-def.json` | Scratch org definition | `/config/` |
| `package.xml` | Deployment manifest | `/manifest/` |
| `package.json` | Node.js dependencies and scripts | Root directory |
| `.prettierrc` | Code formatting rules | Root directory |
| `.eslintignore` | Linter exclusions | Root directory |
| `.forceignore` | Deployment exclusions | Root directory |
| `.gitignore` | Git exclusions | Root directory |

### Useful Commands Reference

#### Salesforce CLI
```bash
# Org management
sfdx force:org:list
sfdx force:org:open
sfdx force:org:create -f config/project-scratch-def.json

# Source operations
sfdx force:source:push
sfdx force:source:pull
sfdx force:source:status
sfdx force:source:deploy --manifest manifest/package.xml

# Testing
sfdx force:apex:test:run --codecoverage
sfdx force:lightning:lwc:test:run

# Data operations
sfdx force:data:tree:import --sobjecttreefiles data/
sfdx force:data:soql:query --query "SELECT Id, Name FROM Account LIMIT 10"

# Debugging
sfdx force:apex:log:tail
sfdx force:apex:log:list
```

#### npm Scripts
```bash
# Code quality
npm run lint
npm run prettier
npm run prettier:verify

# Testing
npm run test
npm run test:unit:watch
npm run test:unit:coverage
npm run test:unit:debug
```

### Resource Links

- **Salesforce DX Developer Guide:** https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/
- **Lightning Web Components Guide:** https://developer.salesforce.com/docs/component-library/documentation/en/lwc
- **Apex Developer Guide:** https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/
- **Salesforce CLI Command Reference:** https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/

---

## Document Metadata

- **Created:** 2026-01-15
- **Author:** George Martin, Salesforce Technical Architect
- **Purpose:** Architecture documentation for 2026 Technical Projects
- **Target Audience:** Developers and Architects
- **Version:** 1.0
- **Repository:** 2026TechnicalProjects (SFDX2024Project)
- **Branch:** claude/document-architecture-u7zBM

---

**Document Status:** Complete and ready for review by development team.
