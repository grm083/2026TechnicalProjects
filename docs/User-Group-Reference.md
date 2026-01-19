# User Group Reference Documentation

**Document Author:** George Martin, Salesforce Technical Architect
**Document Version:** 1.0
**Date:** January 19, 2026
**Purpose:** Central reference for user groups, profiles, and roles across all Salesforce technical projects

---

## Overview

This document provides a standardized reference for all user groups within our Salesforce organization. This information should be used consistently across all project charters, technical design documents, UAT planning, and training materials.

---

## User Group Definitions

### 1. Customer Service Representatives

**Primary Salesforce Profile:** Customer Service Profile

**Role Description:**
Customer Service Representatives (CSRs) are the primary users of the Salesforce platform and serve as the front-line interface between our organization and customers.

**Primary Responsibilities:**
- Create and manage Cases for customer inquiries and issues
- Create and manage Work Orders for service requests
- Generate and manage CPQ Quotes (SBQQ__Quote__c) for customer pricing requests
- Interact with customers primarily through Tasks and activity management
- Document customer interactions and maintain case histories
- Follow up on open cases and ensure timely resolution

**Key Objects Used:**
- Case
- Work Order
- SBQQ__Quote__c (CPQ Quotes)
- Task
- Contact
- Account

**Volume:** Approximately 50+ active users

---

### 2. Sales Team Members

**Primary Salesforce Profile:** Customer Account Team Profile

**Role Description:**
Sales Team members serve as the primary point of escalation for both customers and Customer Service Representatives. They act as intermediaries and decision-makers in complex customer situations.

**Primary Responsibilities:**
- Act as escalation point for CSRs and customers
- Enter and manage Cases for escalated customer issues
- Create and manage CPQ Quotes (SBQQ__Quote__c) for complex pricing scenarios
- Arbitrate pricing inquiries and quote approvals
- Make deciding factors to move work ahead when issues arise
- Manage customer relationships and account strategy
- Resolve conflicts between customers and service teams

**Key Objects Used:**
- SBQQ__Quote__c (CPQ Quotes) - with approval authority
- Case - escalated cases
- Account - account management
- Contact - relationship management
- Task - follow-up activities

**Volume:** Approximately 15 active users

---

### 3. Fulfillment Team Members

**Primary Salesforce Profile:** SSM and Vendor Relations Profile

**Role Description:**
Fulfillment Team members are the primary users of CPQ Quote solutions and are responsible for the operational execution of quotes, vendor management, and data quality.

**Primary Responsibilities:**
- Work with SBQQ__Quote__c solutions to procure vendors and services
- Identify vendor costs and negotiate pricing
- Ensure timelines are being met for quote fulfillment
- Perform comprehensive data management within the system
- Ensure highest data fidelity exists across all fulfillment-related objects
- Manage vendor relationships and service location codes
- Coordinate between sales, customers, and vendors

**Key Objects Used:**
- SBQQ__Quote__c (CPQ Quotes) - fulfillment and vendor selection
- Vendor (Custom Object)
- Supplier (Custom Object)
- Vendor_Service_Location_Code__c
- Account - vendor accounts
- Work Order - fulfillment coordination

**Volume:** Approximately 10 active users

---

### 4. IT Support Members

**Primary Salesforce Profile:** Digital Transformation Team Profile

**Role Description:**
IT Support members are read-only users of the platform who are engaged in production environments when technical issues require digital intervention and debugging.

**Primary Responsibilities:**
- Read-only access to production environment for troubleshooting
- Debugging and querying of ExceptionLog__c for root cause analysis
- Performance monitoring and issue identification
- Support escalation for system-level problems
- Limited data querying for diagnostic purposes
- Documentation of technical issues and resolutions

**Key Objects Used:**
- ExceptionLog__c - primary debugging object
- Integration_Error_Log__c - integration troubleshooting
- All standard and custom objects - read-only access
- System logs and debug logs

**Access Level:** Read-only in production

**Volume:** Approximately 5 active users

---

### 5. Compliance Team Members

**Primary Salesforce Profile:** Compliance Profile

**Role Description:**
Compliance team members are the arbiters of Entitlement data and ensure organizational compliance with Service Level Agreements (SLAs), pricing calculations, and SOX audit requirements.

**Primary Responsibilities:**
- Govern and maintain Entitlement data across all accounts
- Ensure contractual compliance with SLAs and service agreements
- Validate pricing calculations and quote accuracy
- Serve as governors of SOX Audits at the organization
- Audit trail review and compliance reporting
- Maintain data integrity for compliance-related fields
- Coordinate with external auditors

**Key Objects Used:**
- Entitlement - primary object for SLA management
- Account - account-level entitlement settings
- SBQQ__Quote__c - pricing compliance review
- Case - SLA tracking and compliance
- Business_Rule__c - compliance rule management
- Audit logs and field history tracking

**Volume:** Approximately 3-5 active users

---

## User Group Matrix

| User Group | Profile | Primary Role | Access Level | Volume |
|------------|---------|--------------|--------------|--------|
| Customer Service Representatives | Customer Service Profile | Front-line customer interaction | Create/Edit Cases, Tasks, Quotes | ~50 users |
| Sales Team Members | Customer Account Team Profile | Escalation and arbitration | Full Quote management, Case escalation | ~15 users |
| Fulfillment Team Members | SSM and Vendor Relations Profile | Operational execution | CPQ fulfillment, Vendor management | ~10 users |
| IT Support Members | Digital Transformation Team Profile | Technical support | Read-only (production) | ~5 users |
| Compliance Team Members | Compliance Profile | Audit and governance | Entitlement management, Compliance review | 3-5 users |

---

## Common Object Usage by User Group

### Case Object

| User Group | Create | Edit | View | Primary Use Case |
|------------|--------|------|------|------------------|
| Customer Service Representatives | ✅ | ✅ | ✅ | Primary case management |
| Sales Team Members | ✅ | ✅ | ✅ | Escalated cases |
| Fulfillment Team Members | ❌ | Limited | ✅ | View for context |
| IT Support Members | ❌ | ❌ | ✅ | Troubleshooting |
| Compliance Team Members | ❌ | Limited | ✅ | SLA compliance review |

### SBQQ__Quote__c (CPQ Quotes)

| User Group | Create | Edit | View | Primary Use Case |
|------------|--------|------|------|------------------|
| Customer Service Representatives | ✅ | ✅ | ✅ | Standard quote creation |
| Sales Team Members | ✅ | ✅ | ✅ | Complex quotes, approvals |
| Fulfillment Team Members | ❌ | ✅ | ✅ | Vendor selection, fulfillment |
| IT Support Members | ❌ | ❌ | ✅ | Technical troubleshooting |
| Compliance Team Members | ❌ | ❌ | ✅ | Pricing compliance |

### Work Order

| User Group | Create | Edit | View | Primary Use Case |
|------------|--------|------|------|------------------|
| Customer Service Representatives | ✅ | ✅ | ✅ | Service request management |
| Sales Team Members | ❌ | Limited | ✅ | View for customer context |
| Fulfillment Team Members | ❌ | ✅ | ✅ | Coordinate fulfillment |
| IT Support Members | ❌ | ❌ | ✅ | Integration troubleshooting |
| Compliance Team Members | ❌ | ❌ | ✅ | SLA monitoring |

### Task

| User Group | Create | Edit | View | Primary Use Case |
|------------|--------|------|------|------------------|
| Customer Service Representatives | ✅ | ✅ | ✅ | Customer follow-ups |
| Sales Team Members | ✅ | ✅ | ✅ | Sales activities |
| Fulfillment Team Members | ✅ | ✅ | ✅ | Vendor coordination |
| IT Support Members | ❌ | ❌ | ✅ | View only |
| Compliance Team Members | ❌ | ❌ | ✅ | Audit review |

### Entitlement

| User Group | Create | Edit | View | Primary Use Case |
|------------|--------|------|------|------------------|
| Customer Service Representatives | ❌ | ❌ | ✅ | SLA reference |
| Sales Team Members | ❌ | ❌ | ✅ | Customer SLA information |
| Fulfillment Team Members | ❌ | ❌ | ✅ | Service level reference |
| IT Support Members | ❌ | ❌ | ✅ | Read-only access |
| Compliance Team Members | ✅ | ✅ | ✅ | SLA governance and management |

---

## UAT Testing by User Group

### User Acceptance Testing Requirements

For all technical projects requiring UAT, the following user group representation is required:

**Minimum UAT Participants:**
- Customer Service Representatives: 8-10 users (primary users)
- Sales Team Members: 3-5 users (secondary users/escalation path)
- Fulfillment Team Members: 2-3 users (if CPQ/vendor functionality affected)
- Compliance Team Members: 1-2 users (if Entitlement/SLA functionality affected)
- IT Support Members: 1 user (technical validation)

**Total UAT Participants:** Minimum 15-20 users for comprehensive projects

**UAT Duration:**
- Simple projects (field updates, minor enhancements): 1 week
- Medium projects (new components, automation changes): 2 weeks
- Large projects (major feature implementations): 2-3 weeks
- Critical projects (integrations, platform upgrades): 3-4 weeks

---

## Training Requirements by User Group

### Customer Service Representatives
- **Training Type:** Hands-on, scenario-based
- **Duration:** 2-4 hours for major changes
- **Delivery:** In-person or video tutorials
- **Materials:** Quick reference guides, video walkthroughs
- **Timing:** 1 week before deployment

### Sales Team Members
- **Training Type:** Executive briefing + hands-on
- **Duration:** 1-2 hours
- **Delivery:** Group training sessions
- **Materials:** One-page summaries, video tutorials
- **Timing:** 1 week before deployment

### Fulfillment Team Members
- **Training Type:** Detailed workflow training
- **Duration:** 2-3 hours for CPQ changes
- **Delivery:** Hands-on workshop
- **Materials:** Process documentation, step-by-step guides
- **Timing:** 1 week before deployment

### IT Support Members
- **Training Type:** Technical briefing
- **Duration:** 1 hour
- **Delivery:** Technical documentation review
- **Materials:** Architecture diagrams, troubleshooting guides
- **Timing:** Before deployment

### Compliance Team Members
- **Training Type:** Policy and procedure briefing
- **Duration:** 1-2 hours
- **Delivery:** Documentation review + Q&A
- **Materials:** Compliance checklists, audit trail documentation
- **Timing:** 1 week before deployment

---

## Support Escalation Path

**Tier 1: Self-Service**
- All user groups can access Help documentation, knowledge base articles, and video tutorials

**Tier 2: Help Desk**
- Customer Service Representatives → Internal Help Desk
- Sales Team Members → Sales Operations Team
- Fulfillment Team Members → Fulfillment Operations Lead

**Tier 3: IT Support**
- Complex technical issues escalated to IT Support Members (Digital Transformation Team)

**Tier 4: Technical Architect**
- System-level issues, architectural decisions, integration failures
- Escalation to George Martin, Salesforce Technical Architect

---

## References

This document should be referenced in all project charters, technical design documents, UAT planning documents, and training materials created for Salesforce projects.

**Related Documents:**
- Project Charter templates
- Technical Design Document templates
- UAT Checklist templates
- Training Plan templates

---

**Document Status:** APPROVED
**Next Review Date:** June 1, 2026
**Document Owner:** George Martin, Salesforce Technical Architect
**Contact:** [email]

---

**END OF USER GROUP REFERENCE DOCUMENTATION**
