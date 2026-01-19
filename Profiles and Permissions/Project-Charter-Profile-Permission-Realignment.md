# Project Charter: Salesforce Profile and Permission Set Realignment with SailPoint Integration

**Project Name:** Salesforce Profile and Permission Set Realignment with SailPoint Integration

**Project Code:** SFDC-PSA-2026

**Document Type:** Project Charter

**Version:** 1.0

**Date:** January 19, 2026

**Author:** George Martin, Salesforce Technical Architect

**Status:** DRAFT - Pending Executive Approval

---

## Document Control

| Version | Date | Author | Approver | Changes |
|---------|------|--------|----------|---------|
| 1.0 | 2026-01-19 | George Martin | Pending | Initial project charter |

---

## Executive Summary

This project charter authorizes the Salesforce Profile and Permission Set Realignment project, which will modernize our Salesforce security model by migrating from a profile-based permission structure to a feature-based permission set architecture integrated with SailPoint IdentityIQ for centralized identity and access management.

The current environment maintains 17 distinct profiles with embedded permissions, creating significant maintenance overhead and limiting scalability. This project will reduce profiles to a single minimal-access baseline, create 35 feature-based permission sets organized into 8 persona-based permission set groups, and integrate with SailPoint IdentityIQ to enable automated user provisioning and role-based access control.

**Expected Benefits:**
- 94% reduction in profile maintenance (17 profiles → 1 profile)
- Automated user provisioning via SailPoint integration
- Enhanced security through principle of least privilege
- Improved compliance and audit capabilities
- Scalable architecture aligned with Salesforce 2026+ best practices
- Reduced onboarding time from days to minutes

**Total Project Duration:** 20 weeks (approximately 5 months)

**Total Estimated Effort:** 100 story points + SailPoint integration coordination

**Total Estimated Cost:** $125,000 - $175,000 (internal resources + SailPoint licensing)

---

## Table of Contents

1. [Project Background](#project-background)
2. [Business Case](#business-case)
3. [Project Objectives](#project-objectives)
4. [Project Scope](#project-scope)
5. [Success Criteria](#success-criteria)
6. [Stakeholder Analysis](#stakeholder-analysis)
7. [Project Organization](#project-organization)
8. [Project Timeline](#project-timeline)
9. [Budget and Resources](#budget-and-resources)
10. [Risk Assessment](#risk-assessment)
11. [Assumptions and Constraints](#assumptions-and-constraints)
12. [Deliverables](#deliverables)
13. [Approval and Sign-Off](#approval-and-sign-off)

---

## Project Background

### Current State

The Salesforce organization currently operates with:
- **17 distinct user profiles** with embedded permissions
- **31 ad-hoc permission sets** with inconsistent organization
- **0 permission set groups** for persona-based access
- **Manual user provisioning** and permission assignment
- **No automated role-based access control**
- **Limited integration** with enterprise identity management systems

This profile-centric approach creates several challenges:
- High maintenance burden when features require permission changes
- Difficult to track which users have access to which features
- Time-consuming user onboarding requiring manual profile selection and permission set assignment
- Inconsistent access control across similar roles
- Limited scalability for future growth
- Misalignment with Salesforce strategic direction toward permission sets

### Strategic Drivers

1. **Salesforce Platform Evolution:** Salesforce has announced its strategic direction away from profile-based permissions toward permission set-based access control, with enhanced permission set group capabilities introduced in recent releases.

2. **Enterprise IAM Initiative:** The organization is implementing SailPoint IdentityIQ as the centralized identity and access management (IAM) system across all enterprise applications, requiring Salesforce integration for automated user provisioning.

3. **Security and Compliance:** Growing regulatory requirements demand better visibility into user access, clear audit trails, and implementation of least-privilege access principles.

4. **Operational Efficiency:** Current manual provisioning processes create delays in user onboarding and increase administrative overhead.

5. **Scalability Requirements:** Organization growth projections indicate doubling of Salesforce user base within 2 years, making current manual processes unsustainable.

### Key Business Problems

| Problem | Current Impact | Proposed Solution |
|---------|---------------|-------------------|
| 17 profiles require updates for each new feature | 40+ hours per feature deployment | Single profile + modular permission sets reduces to 2-4 hours |
| Manual user onboarding takes 2-3 days | Delayed productivity, poor user experience | Automated provisioning via SailPoint reduces to minutes |
| Difficult to audit who has access to what | Compliance risk, failed audits | Permission set groups provide clear visibility |
| Over-permissioned users (granted access "just in case") | Security risk, data exposure | Least-privilege approach with feature-based permissions |
| Inconsistent permissions across similar roles | User confusion, support tickets | Standardized permission set groups per persona |

---

## Business Case

### Strategic Alignment

This project aligns with three key organizational strategic initiatives:

1. **Digital Transformation Initiative:** Modernizing core business systems for improved efficiency and scalability
2. **Zero Trust Security Framework:** Implementing least-privilege access control across all systems
3. **Enterprise IAM Program:** Centralizing identity management through SailPoint IdentityIQ

### Financial Justification

#### Cost Avoidance

| Category | Current Annual Cost | Projected Cost After | Annual Savings |
|----------|---------------------|----------------------|----------------|
| Profile maintenance (admin time) | $45,000 | $7,500 | $37,500 |
| Manual user provisioning | $30,000 | $5,000 | $25,000 |
| User access support tickets | $20,000 | $8,000 | $12,000 |
| Compliance audit preparation | $15,000 | $5,000 | $10,000 |
| Failed access issues (user productivity loss) | $25,000 | $5,000 | $20,000 |
| **TOTAL ANNUAL SAVINGS** | **$135,000** | **$30,500** | **$104,500** |

#### Investment Summary

| Category | Cost |
|----------|------|
| Internal development resources (10-12 weeks) | $80,000 - $100,000 |
| Project management and coordination | $15,000 - $20,000 |
| SailPoint connector licensing (annual) | $15,000 - $25,000 |
| Testing and UAT resources | $10,000 - $15,000 |
| Training and documentation | $5,000 - $15,000 |
| **TOTAL PROJECT COST** | **$125,000 - $175,000** |

#### Return on Investment (ROI)

- **Payback Period:** 15-20 months
- **3-Year ROI:** 127% - 150%
- **Net Present Value (NPV) at 3 years:** $175,000 - $225,000

#### Intangible Benefits

- Improved user satisfaction and reduced onboarding friction
- Enhanced security posture and reduced audit findings
- Better compliance with SOX and data privacy regulations
- Increased organizational agility for future Salesforce enhancements
- Reduced risk of security breaches due to over-permissioned users
- Improved employee productivity through faster access provisioning

---

## Project Objectives

### Primary Objectives

1. **Simplify Profile Architecture**
   - Reduce from 17 profiles to 1 minimal-access profile
   - Establish minimal-access baseline for all users
   - Retire legacy profiles upon successful migration

2. **Implement Feature-Based Permission Sets**
   - Create 35 permission sets organized by business capability
   - Document object, field, and system permissions for each set
   - Deploy permission sets to production environment

3. **Establish Persona-Based Permission Set Groups**
   - Create 8 permission set groups aligned to organizational roles
   - Map permission sets to each group based on job function
   - Document user personas and access requirements

4. **Integrate with SailPoint IdentityIQ**
   - Develop REST API endpoints for user provisioning
   - Implement automated role-based permission set group assignment
   - Enable bidirectional communication between SailPoint and Salesforce
   - Create comprehensive audit logging for all provisioning actions

5. **Migrate Existing Users**
   - Migrate all 105 existing users to new permission model
   - Validate user access post-migration
   - Provide support during transition period

### Secondary Objectives

6. **Enhance Audit and Compliance Capabilities**
   - Implement comprehensive logging for all permission changes
   - Create audit reports for SOX compliance
   - Document permission assignment rationale

7. **Improve User Onboarding Experience**
   - Reduce onboarding time from days to minutes
   - Eliminate manual permission assignment steps
   - Provide clear documentation on access levels

8. **Enable Future Scalability**
   - Create framework for adding new permission sets
   - Document process for creating new permission set groups
   - Establish governance model for permission management

### Measurable Goals

| Metric | Current State | Target State | Measurement Method |
|--------|---------------|--------------|-------------------|
| Number of profiles | 17 | 1-2 | Salesforce Setup audit |
| User onboarding time | 2-3 days | < 1 hour | Provisioning log timestamps |
| Permission assignment errors | 5-8 per quarter | < 2 per quarter | Support ticket analysis |
| Profile maintenance hours per feature | 40 hours | 2-4 hours | Project time tracking |
| Audit preparation time | 80 hours annually | 20 hours annually | Compliance team survey |
| Failed access support tickets | 15 per month | < 5 per month | Salesforce case analysis |
| User satisfaction score | 6.5/10 | 8.5/10 | Post-implementation survey |

---

## Project Scope

### In Scope

#### Phase 1: Foundation and Analysis (Weeks 1-2)
- Current state documentation and profile analysis
- User persona validation and requirements gathering
- Minimal-access profile design and creation
- Permission naming convention standards
- Risk assessment and mitigation planning

#### Phase 2: Permission Set Development (Weeks 3-8)
- Design and create 35 feature-based permission sets:
  - 7 Core Service Delivery permission sets
  - 5 Quote and Pricing permission sets
  - 6 Operational Management permission sets
  - 3 Reporting and Analytics permission sets
  - 5 System and Integration permission sets
  - 5 Administrative permission sets
  - 4 Specialized Functions permission sets
- Document object-level and field-level permissions
- Test each permission set in isolation
- Create permission set assignment matrix

#### Phase 3: Permission Set Group Creation (Weeks 9-10)
- Create 8 persona-based permission set groups:
  - PSG_Customer_Service_Representative
  - PSG_Sales_Team_Member
  - PSG_Fulfillment_Specialist
  - PSG_IT_Support_Member
  - PSG_Compliance_Team_Member
  - PSG_System_Administrator
  - PSG_Reporting_Analyst
  - PSG_Quality_Assurance_Tester
- Map permission sets to each group
- Pilot test with representative users from each persona

#### Phase 4: SailPoint Integration Development (Weeks 11-15)
- Design SailPoint integration architecture
- Create custom objects:
  - SailPoint_Provisioning_Log__c
- Create custom metadata types:
  - Role_Permission_Set_Group_Mapping__mdt
  - SailPoint_Integration_Setting__mdt
- Develop REST API endpoints:
  - POST /services/apexrest/sailpoint/provision
  - POST /services/apexrest/sailpoint/deprovision
  - GET /services/apexrest/sailpoint/status/{username}
- Implement automation (User trigger and handlers)
- Create error handling and logging framework
- Develop comprehensive test coverage (90%+)

#### Phase 5: Integration Testing and SailPoint Configuration (Weeks 16-17)
- Configure OAuth authentication (Connected App)
- Set up Named Credentials for callbacks
- Test API endpoints end-to-end
- SailPoint team configures Salesforce connector
- Integration testing in sandbox environment
- Performance testing and optimization

#### Phase 6: Pilot Deployment (Weeks 18)
- Deploy to production with pilot user group (15-20 users)
- Migrate pilot users to new permission model
- Monitor for issues and gather feedback
- Refine documentation based on pilot results

#### Phase 7: Full User Migration (Weeks 19-20)
- Migrate remaining users in batches by persona:
  - Week 19: Customer Service (50 users), Sales (15 users)
  - Week 20: Fulfillment (10 users), IT/Compliance/QA/Reporting (20 users)
- Validate permission set group assignments
- Provide user support during migration
- Monitor system performance and error logs

#### Phase 8: Legacy Cleanup and Documentation (Week 20)
- Archive/deactivate legacy profiles
- Remove redundant permission assignments
- Finalize comprehensive documentation:
  - Administrator guide
  - User onboarding guide
  - Troubleshooting guide
  - Permission matrix reference
- Conduct administrator training
- Establish ongoing governance process
- Project closeout and lessons learned

### Out of Scope

The following items are explicitly **not included** in this project:

1. **Other IAM Integrations:** Integration with identity providers beyond SailPoint (e.g., Okta, Azure AD) - separate project required
2. **Sharing Rules Redesign:** Changes to organization-wide defaults, sharing rules, or role hierarchy - addressed in separate security review project
3. **Data Migration:** Migration of historical data or records between environments
4. **External User Communities:** Permission model for Community or Experience Cloud users - separate community security project
5. **Custom Permission Framework:** Development of custom permission management framework beyond standard Salesforce capabilities
6. **Third-Party Applications:** Permission changes for AppExchange or third-party integrated applications
7. **Field-Level Security Review:** Comprehensive review and redesign of field-level security across all objects - ongoing initiative
8. **Mobile App Permissions:** Specific permission adjustments for Salesforce mobile app - addressed separately
9. **Einstein Analytics:** Permission sets for Einstein Analytics/Tableau CRM - separate analytics security project
10. **User License Changes:** Changes to user license types (e.g., Salesforce Platform to Sales Cloud) - handled through separate procurement process

### Boundaries and Interfaces

**Interfaces with Other Systems:**
- SailPoint IdentityIQ (primary integration)
- HR System (feeds SailPoint with role data)
- Active Directory / LDAP (authentication)
- Audit logging system (receives provisioning logs)

**Organizational Interfaces:**
- Human Resources (role definitions and organizational structure)
- Information Security (security policy compliance)
- Compliance Team (SOX audit requirements)
- IT Operations (infrastructure and integration support)

---

## Success Criteria

### Project Success Criteria

The project will be considered successful when all of the following criteria are met:

#### Technical Success Criteria

1. **Permission Architecture Implemented**
   - ✓ 1 minimal-access profile created and deployed
   - ✓ All 35 feature-based permission sets created, tested, and deployed
   - ✓ All 8 permission set groups created and deployed
   - ✓ All permission sets mapped correctly to permission set groups

2. **SailPoint Integration Operational**
   - ✓ All API endpoints functional and tested
   - ✓ User provisioning via SailPoint working end-to-end
   - ✓ Automated role-based permission set group assignment working
   - ✓ 100% of provisioning actions logged to SailPoint_Provisioning_Log__c
   - ✓ 90%+ code coverage achieved on all custom Apex classes

3. **User Migration Complete**
   - ✓ 100% of users (105 total) migrated to new permission model
   - ✓ < 5% of users required manual intervention during migration
   - ✓ All users assigned to appropriate permission set groups
   - ✓ No users over-permissioned (principle of least privilege maintained)

4. **Legacy Cleanup**
   - ✓ 15+ legacy profiles deactivated or archived
   - ✓ Only 1-2 profiles remain active (Minimal Access + System Administrator)

#### Business Success Criteria

5. **Operational Performance**
   - ✓ User onboarding time reduced to < 1 hour (from 2-3 days)
   - ✓ Permission assignment errors reduced to < 2 per quarter (from 5-8)
   - ✓ Failed access support tickets reduced to < 5 per month (from 15)

6. **User Acceptance**
   - ✓ User satisfaction score of 8.0/10 or higher on post-implementation survey
   - ✓ < 10 critical user impact issues during migration
   - ✓ All critical issues resolved within 24 hours

7. **Compliance and Audit**
   - ✓ Audit preparation time reduced by 50%+ (from 80 hours to < 40 hours annually)
   - ✓ All permission assignments traceable to business justification
   - ✓ Comprehensive audit logs available for all provisioning actions
   - ✓ SOX compliance requirements met

#### Documentation and Training

8. **Knowledge Transfer**
   - ✓ Administrator guide completed and approved
   - ✓ User onboarding guide completed
   - ✓ Troubleshooting guide completed
   - ✓ Permission matrix reference completed
   - ✓ Administrator training conducted (minimum 2 sessions)
   - ✓ Knowledge base articles created for common scenarios

#### Quality and Stability

9. **System Stability**
   - ✓ No critical production incidents caused by permission changes
   - ✓ < 0.5% error rate in automated provisioning
   - ✓ API response time < 2 seconds (95th percentile)
   - ✓ No performance degradation in Salesforce platform

---

## Stakeholder Analysis

### Key Stakeholders

#### Executive Stakeholders

| Stakeholder | Role | Interest | Influence | Engagement Strategy |
|------------|------|----------|-----------|---------------------|
| **Director of IT** | Executive Sponsor | Strategic alignment, ROI, risk management | High | Monthly executive briefings, decision escalation |
| **Sales Director** | Business Sponsor | Sales team productivity, minimal disruption | High | Bi-weekly updates, pilot participation |
| **VP of SBS** | Business Sponsor | Customer service efficiency, compliance | High | Bi-weekly updates, pilot participation |
| **Principal Architect** | Security Oversight | Security posture, compliance, audit readiness | High | Weekly security reviews, architecture approval |
| **Senior Manager of IT** | Technical Oversight | Integration success, resource allocation | High | Weekly project status, technical decision approval |

#### Primary Stakeholders

| Stakeholder Group | Size | Primary Concern | Engagement Strategy |
|-------------------|------|-----------------|---------------------|
| **Customer Service Representatives** | ~50 users | Maintaining access to critical features, no disruption | User representatives in pilot, training sessions, support hotline |
| **Sales Team Members** | ~15 users | Quote approval capabilities, customer data access | Sales leadership briefings, early pilot participation |
| **Fulfillment Team** | ~10 users | Vendor management access, quote fulfillment | Process walkthrough, dedicated support during migration |
| **IT Support Team** | ~5 users | Exception log access, troubleshooting capabilities | Technical preview, early access to new logging features |
| **Compliance Team** | 3-5 users | Audit capabilities, SOX compliance | Compliance review sessions, audit report preview |
| **Salesforce Administrators** | 2-3 users | New administration model, training needs | Deep technical training, documentation review |
| **SailPoint Team** | 3-5 people | Integration requirements, API specifications | Weekly integration sync, joint testing sessions |
| **Information Security Team** | 3-5 people | Security model review, vulnerability assessment | Security architecture review, penetration testing |

#### Supporting Stakeholders

| Stakeholder | Role | Involvement |
|------------|------|-------------|
| **Human Resources** | Role definition authority | Validate user personas and organizational roles |
| **Legal/Compliance** | Regulatory compliance | Review audit and compliance capabilities |
| **Change Management** | Organizational change | Communication plan, training coordination |
| **Vendor Management** | SailPoint relationship | SailPoint contract and licensing |
| **Enterprise Architecture** | Technical standards | Architecture review and approval |

### Stakeholder Communication Plan

| Audience | Communication Method | Frequency | Owner |
|----------|---------------------|-----------|-------|
| Executive Sponsors | Executive briefing (email + meeting) | Monthly or as needed | Project Manager |
| Business Sponsors | Status report + demo | Bi-weekly | Project Manager |
| Primary Users | Email updates + town halls | Weekly during migration | Project Manager + Change Management |
| Salesforce Administrators | Technical sync meetings | Weekly | Technical Lead |
| SailPoint Team | Integration working session | 2x per week during Phase 4-5 | Integration Lead |
| All Stakeholders | Project newsletter | Bi-weekly | Project Manager |

---

## Project Organization

### Project Team Structure

#### Core Project Team

| Role | Name | Responsibilities | Time Commitment |
|------|------|------------------|-----------------|
| **Project Sponsor** | [Senior Manager of IT] | Executive oversight, budget approval, escalation resolution | 5% (2 hours/week) |
| **Project Manager** | [TBD] | Overall project coordination, timeline management, stakeholder communication, risk management | 100% (40 hours/week) |
| **Technical Lead / Architect** | George Martin | Technical architecture, permission set design, code review, integration architecture | 75% (30 hours/week) |
| **Lead Salesforce Developer** | [TBD] | Apex development, API implementation, trigger development, testing | 100% (40 hours/week) |
| **Salesforce Developer** | [TBD] | Permission set creation, testing, documentation, migration support | 75% (30 hours/week) |
| **Integration Specialist** | [TBD] | SailPoint integration, API testing, authentication setup | 50% (20 hours/week) during Phases 4-5 |
| **Salesforce Administrator** | [TBD] | Permission set configuration, user migration, production support | 50% (20 hours/week) |
| **QA Lead** | [TBD] | Test strategy, UAT coordination, defect management | 50% (20 hours/week) |
| **Business Analyst** | [TBD] | Requirements gathering, user persona validation, documentation | 50% (20 hours/week) during Phases 1-3 |

#### Extended Team

| Role | Name | Responsibilities | Time Commitment |
|------|------|------------------|-----------------|
| **SailPoint Lead** | [SailPoint Contact] | SailPoint connector configuration, integration testing | 25% (10 hours/week) during Phases 4-5 |
| **Security Architect** | [InfoSec Team] | Security review, vulnerability assessment, OAuth configuration | 10% (4 hours/week) |
| **Compliance Manager** | [Compliance Team] | SOX requirements validation, audit report review | 10% (4 hours/week) |
| **Change Manager** | [Change Management Team] | Communication plan, training coordination, adoption metrics | 25% (10 hours/week) |
| **User Representatives (8)** | [One per persona] | Requirements validation, pilot testing, feedback | 5% (2 hours/week) during pilot |

### Governance Structure

#### Steering Committee

**Purpose:** Provide executive oversight, approve major decisions, resolve escalated issues

**Members:**
- Director of IT (Chair)
- Sales Director
- VP of SBS
- Principal Architect
- Senior Manager of IT
- Project Manager (non-voting)

**Meeting Cadence:** Monthly (or as needed for urgent decisions)

**Decision Authority:**
- Budget changes > $10,000
- Timeline changes > 2 weeks
- Scope changes (any)
- Risk mitigation strategies for high-impact risks

#### Project Management Office (PMO)

**Purpose:** Provide project management support, methodology guidance, portfolio alignment

**Responsibilities:**
- Project plan review and approval
- Resource allocation coordination
- Risk and issue escalation
- Project portfolio reporting

**Engagement:** Weekly touchpoints with Project Manager

### Decision-Making Authority

| Decision Type | Authority | Escalation Path |
|--------------|-----------|-----------------|
| Technical design decisions | Technical Lead | Project Manager → Steering Committee |
| Permission set design | Technical Lead + Business Analyst | Project Manager → Business Sponsors |
| Timeline/schedule adjustments < 1 week | Project Manager | Steering Committee |
| Timeline/schedule adjustments > 1 week | Steering Committee | N/A |
| Budget changes < $5,000 | Project Manager | Project Sponsor |
| Budget changes $5,000-$10,000 | Project Sponsor | Steering Committee |
| Budget changes > $10,000 | Steering Committee | N/A |
| Scope changes (any) | Steering Committee | N/A |
| User migration approach | Project Manager + Technical Lead | Business Sponsors |
| Risk acceptance decisions | Project Manager (low/medium), Steering Committee (high) | N/A |

---

## Project Timeline

### Project Schedule Overview

**Total Duration:** 20 weeks (approximately 5 months)

**Planned Start Date:** February 1, 2026

**Planned End Date:** June 20, 2026

### Detailed Phase Breakdown

#### Phase 1: Foundation and Analysis
**Duration:** 2 weeks (Weeks 1-2)
**Dates:** Feb 1 - Feb 14, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Project kickoff and team onboarding | 2 days | - | Project Manager |
| Current state documentation | 3 days | Kickoff | Business Analyst |
| Profile and permission set analysis | 3 days | Current state | Technical Lead |
| User persona validation workshops | 2 days | - | Business Analyst |
| Minimal-access profile design | 3 days | Analysis complete | Technical Lead |
| Risk assessment and mitigation planning | 2 days | - | Project Manager |
| Project plan finalization | 1 day | All tasks | Project Manager |

**Key Milestone:** Phase 1 Complete - Foundation Established (Feb 14, 2026)

---

#### Phase 2: Permission Set Development
**Duration:** 6 weeks (Weeks 3-8)
**Dates:** Feb 15 - Mar 28, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Create naming convention standards | 1 day | Phase 1 | Technical Lead |
| Create Core Service Delivery permission sets (7) | 1.5 weeks | Standards | Developer |
| Create Quote and Pricing permission sets (5) | 1 week | Standards | Developer |
| Create Operational Management permission sets (6) | 1 week | Standards | Developer |
| Create Reporting permission sets (3) | 0.5 week | Standards | Administrator |
| Create System and Integration permission sets (5) | 1 week | Standards | Developer |
| Create Administrative permission sets (5) | 0.5 week | Standards | Technical Lead |
| Create Specialized Functions permission sets (4) | 0.5 week | Standards | Developer |
| Test each permission set in isolation | 1 week | All PSs created | QA Lead |
| Document permission set matrix | 0.5 week | Testing | Business Analyst |

**Key Milestone:** Phase 2 Complete - All Permission Sets Created (Mar 28, 2026)

---

#### Phase 3: Permission Set Group Creation
**Duration:** 2 weeks (Weeks 9-10)
**Dates:** Mar 29 - Apr 11, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Create 8 permission set groups | 3 days | Phase 2 | Administrator |
| Map permission sets to each group | 2 days | PSGs created | Technical Lead |
| Document permission set group matrix | 2 days | Mapping | Business Analyst |
| Select pilot users (15-20 across all personas) | 1 day | - | Project Manager |
| Conduct pilot user testing | 1 week | PSGs created | QA Lead |
| Gather and incorporate pilot feedback | 2 days | Pilot complete | Project Manager |

**Key Milestone:** Phase 3 Complete - Permission Set Groups Validated (Apr 11, 2026)

---

#### Phase 4: SailPoint Integration Development
**Duration:** 5 weeks (Weeks 11-15)
**Dates:** Apr 12 - May 16, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Design integration architecture | 3 days | Phase 3 | Technical Lead |
| Create custom objects and metadata types | 3 days | Design | Developer |
| Create custom metadata records (role mappings) | 2 days | Custom metadata types | Technical Lead |
| Develop REST API service class | 1 week | Custom objects | Lead Developer |
| Develop provisioning helper class | 1 week | REST API | Lead Developer |
| Develop User trigger and handler | 0.5 week | Helper class | Developer |
| Implement error handling and logging | 0.5 week | Core logic | Developer |
| Create test classes (90%+ coverage) | 1 week | All development | QA Lead + Developers |
| Code review and refactoring | 3 days | Testing | Technical Lead |
| Deploy to integration sandbox | 1 day | Code review | Developer |

**Key Milestone:** Phase 4 Complete - SailPoint Integration Developed (May 16, 2026)

---

#### Phase 5: Integration Testing and SailPoint Configuration
**Duration:** 2 weeks (Weeks 16-17)
**Dates:** May 17 - May 30, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Configure Connected App for OAuth | 2 days | Phase 4 | Administrator |
| Set up Named Credentials | 1 day | Connected App | Integration Specialist |
| Configure Remote Site Settings | 1 day | - | Administrator |
| Test API endpoints with Postman | 2 days | OAuth setup | Integration Specialist |
| SailPoint team configures Salesforce connector | 1 week | API ready | SailPoint Lead |
| End-to-end integration testing | 1 week | SailPoint config | QA Lead |
| Performance testing and optimization | 2 days | Integration testing | Technical Lead |
| Security review and penetration testing | 2 days | - | Security Architect |
| Document API specifications | 2 days | Testing complete | Business Analyst |

**Key Milestone:** Phase 5 Complete - Integration Tested and Validated (May 30, 2026)

---

#### Phase 6: Pilot Deployment
**Duration:** 1 week (Week 18)
**Dates:** May 31 - Jun 6, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Deploy to production (permission sets, PSGs, code) | 1 day | Phase 5 | Technical Lead |
| Migrate pilot users (15-20) to new model | 2 days | Production deploy | Administrator |
| Monitor pilot users for issues | 1 week | Migration | Project Manager |
| Conduct pilot user feedback sessions | 2 days | 3 days of monitoring | Business Analyst |
| Address critical issues identified in pilot | 2 days | Feedback | Developer |
| Refine documentation based on pilot | 1 day | Feedback | Business Analyst |
| Steering Committee go/no-go decision | 1 day | Pilot complete | Project Manager |

**Key Milestone:** Pilot Successful - Production Go-Ahead Approved (Jun 6, 2026)

---

#### Phase 7: Full User Migration
**Duration:** 2 weeks (Weeks 19-20)
**Dates:** Jun 7 - Jun 20, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Communicate migration plan to all users | 1 day | Go-ahead | Change Manager |
| Week 1: Migrate Customer Service (50) and Sales (15) | 1 week | Communication | Administrator |
| Week 1: Provide dedicated support hotline | 1 week | Migration start | Support Team |
| Week 2: Migrate Fulfillment, IT, Compliance, QA, Reporting (25) | 1 week | Week 1 complete | Administrator |
| Week 2: Continue support hotline | 1 week | - | Support Team |
| Validate all permission set group assignments | 2 days | All migrations | QA Lead |
| Monitor error logs and provisioning logs | 2 weeks | Migration start | Technical Lead |
| Address migration issues (ongoing) | 2 weeks | Migration start | Developer |

**Key Milestone:** All Users Migrated Successfully (Jun 20, 2026)

---

#### Phase 8: Legacy Cleanup and Documentation
**Duration:** Concurrent with Week 20
**Dates:** Jun 14 - Jun 20, 2026

| Task | Duration | Dependencies | Owner |
|------|----------|--------------|-------|
| Archive/deactivate legacy profiles | 2 days | All users migrated | Administrator |
| Remove redundant permission assignments | 2 days | Profiles deactivated | Administrator |
| Finalize administrator guide | 2 days | - | Business Analyst |
| Finalize user onboarding guide | 2 days | - | Business Analyst |
| Finalize troubleshooting guide | 2 days | - | Technical Lead |
| Create knowledge base articles | 2 days | - | Business Analyst |
| Conduct administrator training (2 sessions) | 2 days | Documentation | Technical Lead |
| Establish governance process | 1 day | - | Project Manager |
| Project closeout and lessons learned | 1 day | All complete | Project Manager |

**Key Milestone:** Project Complete - Handoff to Operations (Jun 20, 2026)

---

### Critical Path

The critical path includes the following sequential tasks:

1. Phase 1: Foundation and Analysis (2 weeks)
2. Phase 2: Permission Set Development (6 weeks)
3. Phase 3: Permission Set Group Creation (2 weeks)
4. Phase 4: SailPoint Integration Development (5 weeks)
5. Phase 5: Integration Testing (2 weeks)
6. Phase 6: Pilot Deployment (1 week)
7. Phase 7: Full User Migration (2 weeks)

**Total Critical Path Duration:** 20 weeks

### Key Milestones

| Milestone | Target Date | Success Criteria |
|-----------|-------------|------------------|
| Project Kickoff | Feb 1, 2026 | Team assembled, charter approved |
| Foundation Established | Feb 14, 2026 | Current state documented, design complete |
| All Permission Sets Created | Mar 28, 2026 | 35 PSs deployed and tested |
| Permission Set Groups Validated | Apr 11, 2026 | 8 PSGs tested with pilot users |
| SailPoint Integration Developed | May 16, 2026 | Code complete with 90%+ test coverage |
| Integration Tested and Validated | May 30, 2026 | End-to-end testing successful |
| Pilot Successful | Jun 6, 2026 | Pilot users migrated, go-ahead approved |
| All Users Migrated | Jun 20, 2026 | 105 users on new model |
| Project Complete | Jun 20, 2026 | Legacy cleanup done, documentation complete |

---

## Budget and Resources

### Budget Summary

| Category | Estimated Cost | Budget Contingency (15%) | Total Allocated |
|----------|---------------|-------------------------|-----------------|
| **Internal Labor** | $135,334 | $20,300 | $155,634 |
| **SailPoint Licensing** | $20,000 | $3,000 | $23,000 |
| **Third-Party Services** | $5,000 | $750 | $5,750 |
| **Training and Documentation** | $5,000 | $750 | $5,750 |
| **TOTAL PROJECT BUDGET** | **$165,334** | **$24,800** | **$190,134** |

### Detailed Budget Breakdown

#### Internal Labor Costs

**Cost Rate Structure:**
- **Development (Offshore):** $20/hour
- **Technical Architecture (Onshore):** $120,000/year ($57.69/hour)
- **Project Management (Onshore):** $120,000/year ($57.69/hour)
- **QA Testing (Offshore):** $20/hour
- **User Acceptance Testing (Onshore):** $50,000/year ($24.04/hour)

| Role | Hours | Hourly Rate | Total Cost |
|------|-------|-------------|------------|
| Project Manager (100%, 20 weeks) | 800 | $57.69 | $46,152 |
| Technical Lead / Architect (75%, 20 weeks) | 600 | $57.69 | $34,614 |
| Lead Salesforce Developer (100%, 15 weeks) | 600 | $20.00 | $12,000 |
| Salesforce Developer (75%, 15 weeks) | 450 | $20.00 | $9,000 |
| Integration Specialist (50%, 4 weeks) | 80 | $20.00 | $1,600 |
| Salesforce Administrator (50%, 12 weeks) | 240 | $20.00 | $4,800 |
| QA Lead (50%, 16 weeks) | 320 | $20.00 | $6,400 |
| Business Analyst (50%, 10 weeks) | 200 | $57.69 | $11,538 |
| Change Manager (25%, 8 weeks) | 80 | $57.69 | $4,615 |
| Security Architect (10%, 20 weeks) | 80 | $57.69 | $4,615 |
| **Subtotal Internal Labor** | **3,450 hours** | **Blended: $39.23** | **$135,334** |

#### SailPoint Licensing and Services

| Item | Cost | Notes |
|------|------|-------|
| SailPoint Salesforce Connector License (Year 1) | $15,000 | Annual subscription |
| SailPoint Professional Services (integration support) | $5,000 | 20 hours @ $250/hr |
| **Subtotal SailPoint** | **$20,000** | |

#### Third-Party Services

| Item | Cost | Notes |
|------|------|-------|
| Security penetration testing | $3,000 | External security firm |
| OAuth/SSL certificate renewal | $500 | If needed for Connected App |
| Postman Pro licenses (3 users, 6 months) | $500 | API testing |
| Documentation tools/templates | $1,000 | Confluence, Lucidchart, etc. |
| **Subtotal Third-Party** | **$5,000** | |

#### Training and Documentation

| Item | Cost | Notes |
|------|------|-------|
| Training materials development | $2,000 | Slide decks, videos |
| User training sessions (facilitation) | $1,500 | 6 sessions @ $250 |
| Knowledge base article creation | $1,000 | 20 articles @ $50 |
| Administrator certification prep (if needed) | $500 | Study materials |
| **Subtotal Training** | **$5,000** | |

### Resource Requirements

#### Full-Time Equivalents (FTE)

| Resource Type | FTE Allocation | Duration |
|--------------|----------------|----------|
| Project Manager | 1.0 FTE | 20 weeks |
| Technical/Development | 2.5 FTE | 15 weeks avg |
| Testing/QA | 0.5 FTE | 16 weeks |
| Administration | 0.5 FTE | 12 weeks |
| Business Analysis | 0.5 FTE | 10 weeks |
| Change Management | 0.25 FTE | 8 weeks |
| Security/Compliance | 0.1 FTE | 20 weeks |

**Peak Resource Requirement:** Weeks 11-15 (Phase 4) = 4.5 FTE

#### Infrastructure Requirements

| Resource | Requirement | Cost |
|----------|------------|------|
| Salesforce Sandbox (Full Copy) | 1 dedicated sandbox for integration testing | Included in license |
| Development Environments | 3 developer sandboxes | Included in license |
| SailPoint Test Environment | Access to SailPoint sandbox | Included in SailPoint license |
| Version Control (GitHub/GitLab) | Repository for code | Existing organizational license |
| Project Management Tools | Jira/Confluence/MS Project | Existing organizational license |

---

## Risk Assessment

### Risk Management Approach

The project will employ a proactive risk management approach:
1. **Identify:** Risks identified during planning and throughout project lifecycle
2. **Assess:** Risks assessed for probability and impact
3. **Plan:** Mitigation strategies developed for high and medium risks
4. **Monitor:** Risks reviewed weekly in project team meetings
5. **Control:** Risk response plans executed as needed

### Risk Matrix

**Probability Scale:**
- **High (H):** > 50% likelihood
- **Medium (M):** 20-50% likelihood
- **Low (L):** < 20% likelihood

**Impact Scale:**
- **High (H):** Significant impact on timeline (>2 weeks), budget (>$20K), or scope
- **Medium (M):** Moderate impact on timeline (1-2 weeks), budget ($5-20K), or quality
- **Low (L):** Minimal impact, manageable within project tolerances

### Top 15 Project Risks

| # | Risk Description | Prob. | Impact | Risk Score | Mitigation Strategy | Owner |
|---|------------------|-------|--------|-----------|---------------------|-------|
| 1 | **Users lose access to critical features during migration** | M | H | **HIGH** | - Pilot deployment with 15-20 users first<br>- Batch migration approach with immediate rollback capability<br>- Dedicated support hotline during migration<br>- Comprehensive testing of each permission set | Project Manager |
| 2 | **SailPoint integration fails or performs poorly** | M | H | **HIGH** | - Early integration testing (Phase 5)<br>- SailPoint team embedded in project<br>- Fallback to manual provisioning if needed<br>- Performance testing before production | Technical Lead |
| 3 | **Permission sets don't grant sufficient access for job functions** | M | H | **HIGH** | - User persona validation workshops in Phase 1<br>- Pilot testing with representatives from each persona<br>- Feedback loops throughout development<br>- Quick permission adjustment process | Technical Lead |
| 4 | **Inadequate testing leads to production issues** | M | M | **MEDIUM** | - 90%+ code coverage requirement<br>- Dedicated QA lead<br>- End-to-end integration testing<br>- UAT with real users before full rollout | QA Lead |
| 5 | **Key resources unavailable during critical project phases** | M | M | **MEDIUM** | - Cross-training team members<br>- Documentation of all technical decisions<br>- Identification of backup resources<br>- Phase-based resource planning | Project Manager |
| 6 | **Scope creep from additional permission requirements** | H | M | **MEDIUM** | - Formal change control process<br>- Steering Committee approval for scope changes<br>- Out-of-scope items documented for Phase 2<br>- Focus on core 8 personas only | Project Manager |
| 7 | **SailPoint licensing costs exceed budget** | L | H | **MEDIUM** | - Obtain formal quote from SailPoint before project start<br>- Include 15% contingency in budget<br>- Negotiate multi-year pricing | Project Sponsor |
| 8 | **OAuth/authentication configuration issues delay integration** | M | M | **MEDIUM** | - Security architect involved early (Phase 4)<br>- Connected App testing in sandbox first<br>- External security consultant if needed<br>- Alternative authentication method (Named Credential) as backup | Integration Specialist |
| 9 | **Legacy profiles still referenced in automation (flows, triggers)** | M | M | **MEDIUM** | - Audit all flows, Process Builder, and triggers in Phase 1<br>- Update automations to be profile-agnostic<br>- Testing with new profiles before migration | Technical Lead |
| 10 | **Resistance to change from users** | M | L | **MEDIUM** | - Change management plan with clear communication<br>- User representatives involved in design<br>- Training provided before migration<br>- Emphasize benefits (faster access, better experience) | Change Manager |
| 11 | **Governor limits hit during bulk user migration** | L | M | **LOW** | - Batch migration approach (max 25 users at a time)<br>- @future methods for async processing<br>- Monitor API limits during migration<br>- Schedule migrations during off-peak hours | Developer |
| 12 | **Custom metadata type deployment issues** | L | M | **LOW** | - Test custom metadata deployment in sandbox first<br>- Use changeset or SFDX for deployment<br>- Have JSON files ready for manual creation if needed | Administrator |
| 13 | **Documentation incomplete or outdated** | M | L | **LOW** | - Dedicated business analyst for documentation<br>- Documentation review gate at each phase<br>- User feedback on documentation during pilot | Business Analyst |
| 14 | **SailPoint and Salesforce teams misaligned on requirements** | M | M | **MEDIUM** | - Weekly integration working sessions<br>- Clear API specifications documented early<br>- Joint testing sessions in Phase 5<br>- Single point of contact on each team | Technical Lead |
| 15 | **Production deployment fails or requires rollback** | L | H | **MEDIUM** | - Comprehensive deployment checklist<br>- Pilot deployment validates process<br>- Rollback plan documented and tested<br>- Deploy during maintenance window<br>- Full backup before deployment | Technical Lead |

### Risk Response Plans

#### HIGH RISK #1: Users Lose Access to Critical Features

**Response Plan if Risk Occurs:**
1. **Immediate Actions (0-4 hours):**
   - Activate incident response team
   - Identify affected users and features
   - Implement emergency permission set assignment to restore access
   - Notify business stakeholders

2. **Short-Term Resolution (4-24 hours):**
   - Analyze root cause (missing permission, incorrect mapping, etc.)
   - Create corrective permission set or modify existing
   - Deploy fix to production
   - Validate with affected users

3. **Long-Term Prevention:**
   - Update permission set documentation
   - Add test case to prevent recurrence
   - Review all similar permission sets for same issue

**Rollback Criteria:**
- If >20% of migrated users report critical access issues
- If access cannot be restored within 4 hours
- If business operations are significantly disrupted

**Rollback Process:**
1. Stop all further migrations
2. Reassign affected users to original profiles
3. Remove permission set group assignments
4. Reactivate legacy profiles
5. Conduct root cause analysis before resuming

---

#### HIGH RISK #2: SailPoint Integration Fails

**Response Plan if Risk Occurs:**
1. **Immediate Actions:**
   - Activate technical escalation team
   - Diagnose failure point (authentication, API, automation)
   - Check SailPoint logs and Salesforce provisioning logs
   - Engage SailPoint support if needed

2. **Fallback Option:**
   - Temporarily disable SailPoint integration
   - Use manual user provisioning process
   - Leverage User trigger for automatic PSG assignment based on manual role updates
   - Continue with project timeline

3. **Resolution Path:**
   - Fix integration issues in sandbox environment
   - Conduct thorough integration testing
   - Re-enable SailPoint integration when stable

**Contingency:**
- Budget includes $5,000 for SailPoint professional services
- Security architect available for OAuth troubleshooting
- Can operate without SailPoint integration initially using manual provisioning

---

## Assumptions and Constraints

### Project Assumptions

The following assumptions underpin the project plan. If any assumption proves false, the project plan will need to be re-evaluated:

#### Technical Assumptions

1. **Salesforce Platform:**
   - Current Salesforce API version (61.0) supports all required functionality
   - No major Salesforce platform upgrades required during project timeline
   - Sandbox environments available with sufficient data for testing
   - Permission set groups feature is enabled and licensed

2. **SailPoint Integration:**
   - SailPoint IdentityIQ is already implemented and operational in the organization
   - SailPoint Salesforce connector is available and licensed
   - SailPoint team has 10-20 hours per week available for integration work during Phases 4-5
   - SailPoint connector supports REST API-based provisioning

3. **Development Environment:**
   - Development team has necessary Salesforce development tools (VS Code, Salesforce Extensions, SFDX CLI)
   - Version control system (Git) is available
   - Development team has appropriate Salesforce licenses and permissions

4. **Data and Configuration:**
   - User role hierarchy is stable and won't undergo major restructuring during project
   - Existing user data is clean and accurate (no duplicate users, correct email addresses)
   - Federation identifiers (for SSO) are already populated for all users

#### Organizational Assumptions

5. **Resources:**
   - All identified resources will be available for their allocated time commitments
   - No major organizational changes (restructuring, layoffs) during project timeline
   - IT budget approved and available for project expenditures

6. **Business Operations:**
   - Business operations can tolerate brief service disruptions (< 1 hour) during production deployments
   - Users are willing to participate in pilot testing and provide feedback
   - User roles and job functions are clearly defined and stable

7. **Governance:**
   - Steering Committee will be available for monthly meetings and urgent decisions
   - Change control process is established and will be followed
   - Approval cycles for decisions will not exceed 1 week

8. **Training and Adoption:**
   - Users have basic Salesforce knowledge and don't require remedial training
   - Organization has change management resources available
   - Training can be delivered virtually (no travel required)

### Project Constraints

The project operates under the following constraints:

#### Schedule Constraints

1. **Fixed Deadline:** Project must be complete by June 30, 2026 due to:
   - SailPoint enterprise rollout timeline dependency
   - Fiscal year planning cycle
   - Competing projects starting Q3 2026

2. **Blackout Periods:**
   - No production deployments during fiscal year-end (March 25-31, 2026)
   - No major changes during sales quota period close (end of each month)
   - Limited resource availability during corporate holiday shutdown (if applicable)

3. **Dependency Timelines:**
   - SailPoint team availability limited to specific windows (Phases 4-5)
   - Security team penetration testing requires 2-week lead time
   - Steering Committee meetings scheduled monthly (no ad-hoc meetings)

#### Resource Constraints

4. **Team Size:**
   - Limited to available internal Salesforce development team (2 developers)
   - Cannot hire external contractors due to budget constraints
   - Technical Lead (George Martin) available at 75% capacity maximum

5. **Budget:**
   - Total approved budget: $190,134 (including 15% contingency)
   - No additional budget available for overruns
   - Budget must cover internal labor, licensing, and all services

6. **Infrastructure:**
   - Limited to 1 Full Copy sandbox for integration testing
   - Developer sandboxes refresh on monthly schedule (cannot be accelerated)
   - API call limits must be respected (no additional API capacity purchased)

#### Technical Constraints

7. **Platform Limitations:**
   - Salesforce governor limits apply (SOQL queries, DML operations, API calls)
   - Permission set maximum capacity: 1,000 assignments per user (well within limits)
   - Custom metadata types: 100 records per type (within limits)
   - API rate limits: 15,000 calls per 24 hours for integration user

8. **Security Requirements:**
   - All code must pass security review before production deployment
   - OAuth/authentication must comply with corporate security standards
   - No storage of SailPoint credentials in Salesforce (must use Named Credentials)
   - All API traffic must use HTTPS with TLS 1.2+

9. **Compatibility Requirements:**
   - Must maintain compatibility with existing Salesforce customizations (699 Apex classes, 247 UI components)
   - Cannot break existing integrations (Genesys, Acorn, IVR)
   - Must support existing user profiles during transition period

#### Organizational Constraints

10. **Change Management:**
    - Maximum 25 users can be migrated per day (support capacity constraint)
    - All user-facing changes require 1-week advance notice
    - Training sessions limited to 2 hours maximum per session
    - Support hotline available business hours only (8am-6pm ET)

11. **Testing:**
    - UAT limited to 15-20 pilot users (user availability constraint)
    - Production testing window limited to weekends or after-hours
    - Rollback must be completable within 4-hour window

12. **Compliance:**
    - All changes must be documented for SOX compliance
    - Audit logs must be retained for 7 years
    - Separation of duties must be maintained (developer cannot deploy own code to production)

---

## Deliverables

### Project Deliverables

The following deliverables will be produced during the project:

#### Phase 1: Foundation and Analysis

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **Current State Assessment Report** | Documentation of existing profiles, permission sets, and user assignments | PDF/Word (30-50 pages) | Business Analyst | Week 2 |
| **User Persona Validation Document** | Validated user personas with role definitions and access requirements | PDF/Word (15-20 pages) | Business Analyst | Week 2 |
| **Minimal Access Profile Design** | Specification for baseline minimal access profile | PDF/Word (10 pages) | Technical Lead | Week 2 |
| **Risk Assessment and Mitigation Plan** | Identified risks with mitigation strategies | PDF/Word (10-15 pages) | Project Manager | Week 2 |
| **Detailed Project Plan** | MS Project or similar with tasks, dependencies, resources | MPP/PDF | Project Manager | Week 2 |

#### Phase 2: Permission Set Development

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **35 Permission Sets** | All feature-based permission sets deployed to sandbox | Salesforce Metadata | Developer | Week 8 |
| **Permission Set Specifications** | Detailed documentation of each permission set (objects, fields, Apex classes) | PDF/Word (50-75 pages) | Technical Lead | Week 8 |
| **Permission Set Testing Report** | Test results for each permission set in isolation | Excel/PDF | QA Lead | Week 8 |
| **Permission Set Assignment Matrix** | Matrix showing which permission sets grant access to which features | Excel | Business Analyst | Week 8 |

#### Phase 3: Permission Set Group Creation

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **8 Permission Set Groups** | Persona-based permission set groups deployed to sandbox | Salesforce Metadata | Administrator | Week 10 |
| **Permission Set Group Specifications** | Documentation of each PSG with included permission sets | PDF/Word (25-30 pages) | Technical Lead | Week 10 |
| **Pilot Testing Report** | Results from pilot user testing with feedback and resolutions | PDF/Word (15-20 pages) | QA Lead | Week 10 |

#### Phase 4: SailPoint Integration Development

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **Integration Architecture Document** | Technical design for SailPoint integration | PDF/Word (30-40 pages) | Technical Lead | Week 11 |
| **Custom Objects and Metadata** | SailPoint_Provisioning_Log__c, custom metadata types | Salesforce Metadata | Developer | Week 13 |
| **Apex Code Package** | All Apex classes, triggers, and test classes | Salesforce Code | Lead Developer | Week 15 |
| **API Specification Document** | REST API endpoint specifications with request/response schemas | PDF/Word (20-25 pages) | Technical Lead | Week 15 |
| **Unit Test Results** | Test coverage report (90%+ requirement) | HTML/PDF | QA Lead | Week 15 |
| **Code Review Report** | Technical review findings and resolutions | PDF/Word (10 pages) | Technical Lead | Week 15 |

#### Phase 5: Integration Testing and SailPoint Configuration

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **Connected App Configuration** | OAuth Connected App for SailPoint authentication | Salesforce Metadata | Administrator | Week 16 |
| **Named Credentials** | Secure credentials for SailPoint callbacks | Salesforce Metadata | Integration Specialist | Week 16 |
| **Integration Test Plan** | Detailed test scenarios for end-to-end integration | PDF/Word (15-20 pages) | QA Lead | Week 16 |
| **Integration Test Results** | Results from end-to-end integration testing | Excel/PDF | QA Lead | Week 17 |
| **Performance Test Results** | API performance metrics and optimization recommendations | PDF/Word (10 pages) | Technical Lead | Week 17 |
| **Security Review Report** | Security assessment and penetration test results | PDF/Word (10-15 pages) | Security Architect | Week 17 |

#### Phase 6: Pilot Deployment

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **Production Deployment Package** | All permission sets, PSGs, code, and configuration for production | Salesforce Metadata | Technical Lead | Week 18 |
| **Pilot User Migration Report** | Results from pilot user migration with issues and resolutions | PDF/Word (10 pages) | Project Manager | Week 18 |
| **Pilot User Feedback Report** | Consolidated feedback from pilot users | PDF/Word (10-15 pages) | Business Analyst | Week 18 |
| **Go/No-Go Decision Document** | Steering Committee decision on full rollout | PDF/Word (5 pages) | Project Manager | Week 18 |

#### Phase 7: Full User Migration

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **User Migration Plan** | Detailed plan for migrating all users in batches | PDF/Word (15 pages) | Project Manager | Week 19 |
| **User Communication Materials** | Emails, FAQs, quick reference guides for users | PDF/Email | Change Manager | Week 19 |
| **Daily Migration Reports** | Daily status reports during migration period | Email/PDF | Administrator | Weeks 19-20 |
| **Final Migration Report** | Complete migration results with metrics and issues | PDF/Word (15-20 pages) | Project Manager | Week 20 |

#### Phase 8: Legacy Cleanup and Documentation

| Deliverable | Description | Format | Owner | Due Date |
|------------|-------------|--------|-------|----------|
| **Administrator Guide** | Comprehensive guide for Salesforce administrators | PDF/Word (40-50 pages) | Business Analyst | Week 20 |
| **User Onboarding Guide** | Step-by-step guide for new user provisioning | PDF/Word (10-15 pages) | Business Analyst | Week 20 |
| **Troubleshooting Guide** | Common issues and resolutions | PDF/Word (15-20 pages) | Technical Lead | Week 20 |
| **Permission Matrix Reference** | Complete matrix of all permission sets and PSGs | Excel | Business Analyst | Week 20 |
| **Knowledge Base Articles** | 20+ articles for common scenarios and questions | HTML (Salesforce Knowledge) | Business Analyst | Week 20 |
| **Administrator Training Materials** | Slide decks and hands-on exercises | PPT/PDF | Technical Lead | Week 20 |
| **Governance Process Document** | Ongoing governance process for permission management | PDF/Word (10-15 pages) | Project Manager | Week 20 |
| **Project Closeout Report** | Final project summary with lessons learned | PDF/Word (20-25 pages) | Project Manager | Week 20 |
| **As-Built Documentation** | Technical documentation of final implementation | PDF/Word (50-75 pages) | Technical Lead | Week 20 |

### Total Deliverable Count: 45+ documents and artifacts

---

## Approval and Sign-Off

### Project Charter Approval

This project charter requires approval from the following stakeholders before project initiation:

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Project Sponsor** | [Senior Manager of IT] | _________________ | _______ |
| **Executive Sponsor** | [Director of IT] | _________________ | _______ |
| **Business Sponsor - Sales** | [Sales Director] | _________________ | _______ |
| **Business Sponsor - Operations** | [VP of SBS] | _________________ | _______ |
| **Security Oversight** | [Principal Architect] | _________________ | _______ |
| **Project Manager** | [TBD] | _________________ | _______ |
| **Technical Lead** | George Martin, Salesforce Technical Architect | _________________ | _______ |

### Approval Criteria

The approvers above confirm:

- ✓ The business case is sound and benefits justify the investment
- ✓ The project objectives align with organizational strategy
- ✓ The scope is clearly defined and achievable
- ✓ Resources and budget are allocated and available
- ✓ Risks have been identified and mitigation strategies are reasonable
- ✓ Timeline is realistic and acceptable to the organization
- ✓ Success criteria are clear and measurable
- ✓ Stakeholder engagement plan is appropriate
- ✓ Deliverables meet organizational quality standards

### Project Authorization

By signing this project charter, the approvers authorize:

1. **Resource Allocation:** Use of named resources at specified time commitments
2. **Budget Authorization:** Expenditure up to $190,134 (including contingency)
3. **Organizational Impact:** Temporary disruption during migration periods with proper communication
4. **Decision Authority:** Project Manager and Technical Lead empowered to make day-to-day decisions within defined boundaries
5. **Governance:** Steering Committee established with monthly meeting cadence

### Change Control

Any changes to the following require Steering Committee approval:
- Project scope (any additions or removals)
- Timeline changes exceeding 1 week
- Budget increases exceeding $5,000
- Resource changes affecting critical path
- Risk acceptance decisions for high-impact risks

Changes will be managed through formal change request process documented in project plan.

---

## Appendices

### Appendix A: Acronyms and Definitions

| Term | Definition |
|------|------------|
| **CPQ** | Configure, Price, Quote - Salesforce CPQ product |
| **CRUD** | Create, Read, Update, Delete - database operations |
| **CSR** | Customer Service Representative |
| **FLS** | Field-Level Security |
| **FTE** | Full-Time Equivalent |
| **IAM** | Identity and Access Management |
| **IVR** | Interactive Voice Response |
| **OWD** | Organization-Wide Defaults |
| **PS** | Permission Set |
| **PSG** | Permission Set Group |
| **REST** | Representational State Transfer - API architecture |
| **ROI** | Return on Investment |
| **SBQQ** | Salesforce CPQ object prefix |
| **SFDX** | Salesforce DX (Developer Experience) |
| **SLA** | Service Level Agreement |
| **SOX** | Sarbanes-Oxley Act (compliance regulation) |
| **SSO** | Single Sign-On |
| **STP** | Straight-Through Processing |
| **TDD** | Technical Design Document |
| **UAT** | User Acceptance Testing |

### Appendix B: Reference Documents

The following documents provide additional context and detail for this project:

1. **Permission Strategy Analysis** (`Permission-Strategy-Analysis.md`)
   - Current state assessment
   - Complete feature inventory
   - Recommended permission strategy
   - 16-week implementation roadmap

2. **SailPoint Integration Technical Design** (`SailPoint-Integration-Technical-Design.md`)
   - Integration architecture
   - Complete permission set inventory with object permissions
   - API specifications
   - Production-ready code
   - Deployment guide

3. **User Group Reference** (`User-Group-Reference.md`)
   - Detailed user persona definitions
   - User volume by persona
   - Object usage matrix
   - UAT and training requirements

4. **Salesforce Architecture Documentation** (`Claude.md`)
   - Complete Salesforce platform architecture
   - Technology stack inventory
   - Integration points
   - Security architecture

### Appendix C: Stakeholder Contact Information

| Stakeholder | Email | Phone | Role |
|------------|-------|-------|------|
| **George Martin** | [email protected] | [phone] | Technical Lead / Architect |
| [Project Manager] | [email] | [phone] | Project Manager |
| [Director of IT] | [email] | [phone] | Executive Sponsor |
| [Senior Manager of IT] | [email] | [phone] | Project Sponsor |
| [Sales Director] | [email] | [phone] | Business Sponsor |
| [VP of SBS] | [email] | [phone] | Business Sponsor |
| [Principal Architect] | [email] | [phone] | Security Oversight |
| [SailPoint Lead] | [email] | [phone] | SailPoint Team Lead |

### Appendix D: Project Charter Revision History

| Version | Date | Author | Description of Changes |
|---------|------|--------|----------------------|
| 0.1 | 2026-01-15 | George Martin | Initial draft for internal review |
| 0.5 | 2026-01-17 | George Martin | Incorporated feedback from technical team |
| 1.0 | 2026-01-19 | George Martin | Final version for executive approval |
| 1.1 | 2026-01-19 | George Martin | Updated budget with corrected organizational cost rates |

---

## Document Metadata

**Document Title:** Project Charter: Salesforce Profile and Permission Set Realignment with SailPoint Integration

**Document Code:** SFDC-PSA-2026

**Version:** 1.1

**Date:** January 19, 2026

**Author:** George Martin, Salesforce Technical Architect

**Classification:** Internal - Confidential

**Distribution List:**
- Steering Committee Members
- Project Team Members
- Key Stakeholders

**Review Cycle:** This charter will be reviewed and updated if significant changes occur in:
- Project scope
- Timeline (> 2 weeks)
- Budget (> 10%)
- Key resources
- Organizational priorities

**Related Projects:**
- Enterprise SailPoint IdentityIQ Implementation
- Salesforce API Version Upgrade
- Zero Trust Security Framework Implementation

---

**END OF PROJECT CHARTER**

---

**Prepared by:**

George Martin
Salesforce Technical Architect
Date: January 19, 2026

**Awaiting Approval from:**
- Executive Sponsor (Director of IT)
- Project Sponsor (Senior Manager of IT)
- Business Sponsors (Sales Director, VP of SBS)
- Security Oversight (Principal Architect)
