# 2026 Technical Projects Portfolio Summary

**Document Date:** January 19, 2026
**Author:** George Martin, Salesforce Technical Architect
**Status:** Consolidated Portfolio View

---

## Executive Summary

This document consolidates all active and proposed technical projects for the 2026 planning cycle, providing a comprehensive view of scope, financial benefits, timelines, and resource requirements across the Salesforce technical portfolio.

### Portfolio Overview

| # | Project Name | Duration | Total Cost | Annual ROI | Priority |
|---|--------------|----------|------------|------------|----------|
| 1 | Contact Search Apex Refactoring | 6 weeks | $21,093 | $218,980/yr | **HIGH** |
| 2 | Contact Search As-Is LWC Migration | 8 weeks | $27,542 | $37,040/yr | MEDIUM |
| 3 | Contact Search Redesigned LWC | 14 weeks | $124,614 | $472,750/yr | MEDIUM |
| 4 | Salesforce API Version Upgrade | 18 weeks | $73,055 | $140,000/yr (Y1) | **CRITICAL** |
| 5 | Platform Event Volume Reduction | 5 weeks | $52,080 | Risk Avoidance | **HIGH** |
| 6 | Workflow/Process Builder Migration | 16 weeks | $39,666 | $80,000/yr (Y1) | **CRITICAL** |

**Total Portfolio Investment:** $338,050
**Total Annual Benefits (Year 1):** $948,770+
**Combined Portfolio ROI:** 181% (first year)

---

## Project Prioritization Analysis

### Priority 1: CRITICAL - Mandatory Compliance Projects

#### 1A. Workflow Rule and Process Builder Migration
**Must Complete By:** December 31, 2025 (Salesforce End of Support)
**Duration:** 16 weeks
**Cost:** $39,666
**Status:** MANDATORY

**Why Critical:**
- Salesforce End of Support deadline passed (December 31, 2025)
- Unsupported technology creates compliance risk
- Integration failures will occur when partners upgrade
- No bug fixes or support available after deadline

**Financial Impact:**
- 3-Year Avoided Costs: $345,000
- ROI: 770%
- Payback Period: 6.0 months

**Recommendation:** **START IMMEDIATELY** - Already past End of Support deadline

---

#### 1B. Salesforce API Version Upgrade
**Must Complete By:** Q2 2026 (Before Breaking Changes Impact Production)
**Duration:** 18 weeks
**Cost:** $73,055
**Status:** MANDATORY

**Why Critical:**
- Breaking changes in API 65.0 will cause compilation failures
- SOAP authentication deprecated - integration failures imminent
- 1,046 components span 10 years of API versions (38.0-64.0)
- Technical debt creates security and stability risks

**Financial Impact:**
- 3-Year Cost Avoidance: $655,000
- ROI: 797%
- Payback Period: 3.8 months

**Recommendation:** **START IMMEDIATELY** - Critical breaking changes must be addressed

---

### Priority 2: HIGH - Performance & Reliability

#### 2A. Contact Search Apex Refactoring (Phase 1)
**Prerequisite For:** All Contact Search LWC migrations
**Duration:** 6 weeks
**Cost:** $21,093
**Status:** Foundation Project

**Why High Priority:**
- 70% search performance improvement (1-2 seconds → <500ms)
- Eliminates critical performance bottleneck
- Prerequisite for LWC migration options
- High ROI with rapid payback

**Financial Impact:**
- Annual Productivity Savings: $216,580
- ROI: 3,016% (3-year)
- Payback Period: 0.4 months (less than 2 weeks)

**Recommendation:** **START AFTER** Priority 1 projects complete OR run in parallel with separate team

---

#### 2B. Platform Event Volume Reduction
**Impact:** System Stability & Data Integrity
**Duration:** 5 weeks
**Cost:** $52,080
**Status:** High Risk Mitigation

**Why High Priority:**
- 97.8% reduction in API calls (450/hour → <25/hour)
- Currently losing data in CasetoQuote automation (98% drop rate)
- Governor limit risks threaten production stability
- Missing audit trail creates compliance gaps

**Financial Impact:**
- Immediate Risk Avoidance: Prevented outages ($50,000+ per incident)
- ROI: 200-400% over 3 years
- Payback Period: Immediate

**Recommendation:** **START AFTER** Priority 1 projects OR run in parallel - addresses data loss

---

### Priority 3: MEDIUM - Strategic Improvements

#### 3A. Contact Search As-Is LWC Migration (Phase 2 - Option A)
**Prerequisite:** Phase 1 Apex Refactoring Complete
**Duration:** 8 weeks
**Cost:** $27,542
**Status:** Framework Modernization

**Why Medium Priority:**
- Aura framework in maintenance mode (deprecated)
- 30-40% performance improvement
- Lower cost option ($27K vs $125K for redesign)
- Minimal user retraining required

**Financial Impact:**
- Annual Savings: $37,040
- ROI: 304% (3-year)
- Payback Period: 11 months

**Decision Point:** Choose between Option A (As-Is) or Option B (Redesign) - mutually exclusive

---

#### 3B. Contact Search Redesigned LWC (Phase 3 - Option B)
**Prerequisite:** Phase 1 Apex Refactoring Complete
**Duration:** 14 weeks
**Cost:** $124,614
**Status:** UX Transformation

**Why Medium Priority:**
- 67% task completion time reduction (3 min → 1 min)
- 75% error rate reduction
- Modern progressive disclosure UX
- Higher upfront investment with higher long-term returns

**Financial Impact:**
- Annual Productivity Savings: $208,250
- Annual Error Reduction Savings: $234,500
- Annual Support Cost Savings: $30,000
- **Total Annual Value: $472,750**
- ROI: 1,038% (3-year)
- Payback Period: 3.2 months

**Decision Point:** Choose between Option A (As-Is) or Option B (Redesign) - mutually exclusive

---

## Detailed Project Breakdowns

---

## PROJECT 1: Contact Search Apex Refactoring (Phase 1)

### Scope
**In Scope:**
- Refactor ContactSearchandCreate Apex class
- Replace SOSL with optimized SOQL queries
- Implement Platform Cache for frequently accessed data
- Consolidate DML operations (bulkification)
- Split monolithic class into focused service classes
- Move hard-coded vendor list to Custom Metadata Type
- Achieve 80%+ test coverage

**Out of Scope:**
- UI changes (handled in Phase 2 or 3)
- Database schema modifications
- New functionality or features

### Financial Benefits
**Cost Savings:**
- **Productivity:** $216,580/year (1,000 min/day saved × $50/hr user cost)
- **Performance:** Reduced Apex CPU time saves $2,400/year in platform fees

**Total Annual Benefits:** $218,980

**Investment:**
- **Total Cost:** $21,093
- **3-Year ROI:** 3,016%
- **Payback Period:** 0.4 months

### Timeline
**Duration:** 6 weeks

| Week | Phase | Key Deliverables |
|------|-------|------------------|
| 1 | Analysis & Design | Technical design document, ADRs, test strategy |
| 2-3 | Core Refactoring | Service layer classes, SOQL optimization, caching |
| 3-4 | Testing & QA | Unit tests (80%+ coverage), performance tests |
| 5 | UAT & Documentation | UAT testing, documentation finalized |
| 6 | Deployment | Production deployment, monitoring |

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Senior Apex Developer (Offshore) | 1.0 | 6 weeks | 240 hrs | $4,800 |
| Apex Developer (Offshore) | 1.0 | 4 weeks | 160 hrs | $3,200 |
| Technical Lead/Architect (Onshore) | 0.25 | 6 weeks | 60 hrs | $3,461 |
| QA Engineer (Offshore) | 1.0 | 3 weeks | 120 hrs | $2,400 |
| Performance Specialist (Offshore) | 0.5 | 1 week | 20 hrs | $400 |
| Salesforce Administrator (Offshore) | 0.25 | 6 weeks | 60 hrs | $1,200 |
| Business Analyst (Onshore) | 0.25 | 2 weeks | 20 hrs | $1,154 |
| Security Specialist (Onshore) | 0.1 | 1 week | 4 hrs | $231 |
| **Total** | | | **684 hours** | **$16,846** |

**Additional Costs:**
- Infrastructure & Tools: $800
- Contingency (15%): $3,447
- **Grand Total:** $21,093

**Key Dependencies:**
- Full copy sandbox access
- No conflicting Salesforce releases during deployment

---

## PROJECT 2: Contact Search As-Is LWC Migration (Phase 2 - Option A)

### Scope
**In Scope:**
- Convert SearchExistingContact Aura component to LWC
- Maintain exact same UI layout and styling
- Preserve 100% of existing functionality
- Implement wire services and LWC custom events
- Jest unit tests (85%+ coverage)
- Minimal user training required

**Out of Scope:**
- UX redesign or improvements
- Additional features
- Process improvements

**Note:** Mutually exclusive with Project 3 (Redesign option)

### Financial Benefits
**Cost Savings:**
- **Performance:** 30% faster page loads = 125 min/day saved = $27,040/year
- **Maintenance:** Reduced costs vs keeping Aura = $10,000/year

**Total Annual Benefits:** $37,040

**Investment:**
- **Total Cost:** $27,542
- **3-Year ROI:** 304%
- **Payback Period:** 11 months

### Timeline
**Duration:** 8 weeks

| Week | Phase | Key Deliverables |
|------|-------|------------------|
| 1 | Planning & Architecture | Aura analysis, LWC architecture, development environment |
| 2-3 | Core Component Development | Main container, search functionality, results display |
| 4-5 | Forms & Modals | Contact creation forms, duplicate detection modal |
| 6 | Testing & QA | Jest tests (85%+), integration tests, performance tests |
| 7 | UAT & Bug Fixes | UAT testing, defect resolution, documentation |
| 8 | Deployment | Production deployment, smoke tests, monitoring |

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Senior LWC Developer (Offshore) | 1.0 | 8 weeks | 320 hrs | $6,400 |
| LWC Developer (Offshore) | 1.0 | 6 weeks | 240 hrs | $4,800 |
| Technical Lead/Architect (Onshore) | 0.25 | 8 weeks | 80 hrs | $4,615 |
| QA Engineer (Offshore) | 1.0 | 3 weeks | 120 hrs | $2,400 |
| Accessibility Specialist (Onshore) | 0.5 | 1 week | 20 hrs | $1,154 |
| Salesforce Administrator (Offshore) | 0.25 | 8 weeks | 80 hrs | $1,600 |
| Business Analyst (Onshore) | 0.25 | 2 weeks | 20 hrs | $1,154 |
| UX Designer (Onshore) | 0.1 | 1 week | 4 hrs | $231 |
| **Total** | | | **884 hours** | **$22,354** |

**Additional Costs:**
- Infrastructure & Tools: $900
- Contingency (15%): $4,288
- **Grand Total:** $27,542

**Prerequisites:**
- Project 1 (Apex Refactoring) completed and deployed

---

## PROJECT 3: Contact Search Redesigned LWC (Phase 3 - Option B)

### Scope
**In Scope:**
- Completely redesigned UX with progressive disclosure pattern
- Smart search bar with pattern detection
- Inline contact preview on hover
- Contextual new contact creation (slide-out panel)
- Mobile-first responsive design
- 8-10 LWC components (vs 3-4 in As-Is)
- Comprehensive user training (videos, guides, hands-on)
- Usability testing with 20+ participants

**Out of Scope:**
- AI-powered search suggestions (future phase)
- Integration with external contact databases
- Multi-language support
- Offline mobile capability

**Note:** Mutually exclusive with Project 2 (As-Is option)

### Financial Benefits
**Productivity Gains:**
- Task completion time: 67% reduction (3 min → 1 min) = $208,250/year

**Error Reduction:**
- 75% reduction in user errors = $234,500/year

**Support Cost Reduction:**
- 50% reduction in tickets = $30,000/year

**Total Annual Benefits:** $472,750

**Investment:**
- **Total Cost:** $124,614
- **3-Year ROI:** 1,038%
- **Payback Period:** 3.2 months

### Timeline
**Duration:** 14 weeks

| Weeks | Phase | Key Deliverables |
|-------|-------|------------------|
| 1-3 | Discovery & Design | User research, UX design, technical architecture |
| 4-7 | Core Development | Search interface, results & preview, component interactions |
| 8-9 | Advanced Features | Contact forms, keyboard shortcuts, mobile responsiveness |
| 10-11 | Testing & Refinement | Jest tests (85%+), usability testing (20+ users), A/B testing |
| 12-13 | UAT | UAT with 30-50 users, training materials, defect resolution |
| 14 | Deployment | Production deployment, training delivery, monitoring |

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Senior UX Designer (Onshore) | 0.75 | 14 weeks | 420 hrs | $24,230 |
| UI Designer (Offshore) | 0.5 | 8 weeks | 160 hrs | $3,200 |
| UX Researcher (Onshore) | 0.5 | 3 weeks | 60 hrs | $3,461 |
| Senior LWC Developer (Offshore) | 1.0 | 14 weeks | 560 hrs | $11,200 |
| LWC Developer (Offshore) | 1.0 | 12 weeks | 480 hrs | $9,600 |
| LWC Developer Part-time (Offshore) | 0.5 | 8 weeks | 160 hrs | $3,200 |
| Technical Lead/Architect (Onshore) | 0.25 | 14 weeks | 140 hrs | $8,077 |
| QA Engineer (Offshore) | 1.0 | 6 weeks | 240 hrs | $4,800 |
| Accessibility Specialist (Onshore) | 0.5 | 2 weeks | 80 hrs | $4,615 |
| Performance Specialist (Offshore) | 0.25 | 1 week | 10 hrs | $200 |
| Salesforce Administrator (Offshore) | 0.25 | 14 weeks | 140 hrs | $2,800 |
| Business Analyst (Onshore) | 0.5 | 6 weeks | 120 hrs | $6,923 |
| Technical Writer (Offshore) | 0.5 | 4 weeks | 80 hrs | $1,600 |
| Instructional Designer (Onshore) | 0.25 | 2 weeks | 20 hrs | $1,154 |
| **Total** | | | **2,670 hours** | **$85,060** |

**Additional Costs:**
- Infrastructure & Tools: $5,300
- Research & Testing: $3,300
- Training & Change Management: $9,500
- Contingency (15%): $21,454
- **Grand Total:** $124,614

**Prerequisites:**
- Project 1 (Apex Refactoring) completed and deployed

---

## PROJECT 4: Salesforce API Version Upgrade

### Scope
**In Scope:**
- Upgrade 1,046 components from API versions 38.0-64.0 to 65.0
  - 699 Apex classes
  - 42 Lightning Web Components
  - 206 Aura Components
  - 99 Flows
- Fix breaking changes (access modifiers, flow record references)
- Migrate 3 SOAP web services to OAuth 2.0
- Comprehensive testing (unit, integration, regression, UAT)

**Out of Scope:**
- Aura to LWC migration (separate initiative)
- Code refactoring beyond API requirements
- New feature development

### Financial Benefits
**Cost Avoidance (3-Year Projection):**

| Benefit Category | Year 1 | Year 2 | Year 3 | Total |
|------------------|--------|--------|--------|-------|
| Integration Failure Prevention | $50,000 | $75,000 | $100,000 | $225,000 |
| Reduced Maintenance Costs | $30,000 | $45,000 | $60,000 | $135,000 |
| Productivity Gains | $20,000 | $30,000 | $40,000 | $90,000 |
| Feature Adoption Value | $15,000 | $25,000 | $40,000 | $80,000 |
| Emergency Fix Avoidance | $25,000 | $40,000 | $60,000 | $125,000 |
| **Total** | **$140,000** | **$215,000** | **$300,000** | **$655,000** |

**Investment:**
- **Total Cost:** $73,055
- **3-Year ROI:** 797%
- **Payback Period:** 3.8 months

### Timeline
**Duration:** 18 weeks

| Weeks | Phase | Components Upgraded |
|-------|-------|---------------------|
| 1 | Critical Classes (API 38.0) | 4 classes (0.4%) |
| 2-3 | Trigger Handlers | 30+ classes (14%) |
| 4-10 | Remaining Apex | 665 classes (80% total) |
| 11 | Lightning Web Components | 42 components (84% total) |
| 12-14 | Aura Components | 206 components (94% total) |
| 15-16 | Flows | 99 flows (100% total) |
| 17 | Integration & Testing | All components validated |
| 18 | UAT & Production | Deployment and stabilization |

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Technical Architect (Onshore) | 0.25 | 18 weeks | 180 hrs | $10,384 |
| Lead Developer (Offshore) | 1.0 | 18 weeks | 720 hrs | $14,400 |
| Supporting Developer (Offshore) | 0.5 | 16 weeks | 320 hrs | $6,400 |
| QA Engineer (Offshore) | 0.5 | 10 weeks | 356 hrs | $7,120 |
| Project Manager (Onshore) | 0.25 | 18 weeks | 168 hrs | $9,692 |
| Salesforce Admin (Offshore) | 0.1 | 18 weeks | 72 hrs | $1,440 |
| Integration Specialist (Offshore) | 0.1 | 4 weeks | 16 hrs | $320 |
| Business Users (UAT - Onshore) | Various | Week 18 | 240 hrs | $5,770 |
| **Total** | | | **2,072 hours** | **$55,526** |

**Additional Costs:**
- Tools & Licenses: $5,000
- Training & Documentation: $3,000
- Contingency (15%): $9,529
- **Grand Total:** $73,055

**Critical Dependencies:**
- Salesforce platform stability during upgrade
- Integration partner test environment availability
- No major Salesforce releases during timeline

---

## PROJECT 5: Platform Event Volume Reduction

### Scope
**In Scope:**
- Refactor 6 core Apex classes/triggers for bulkification:
  1. CasetoQuoteAutomation.trigger
  2. PlatformEventProcessor.cls (RaiseTaskAndGenesysPE method)
  3. QouteValiationHandler.cls
  4. AutoSendEmailToServiceApprovers.cls
  5. Logger.cls (deprecate saveLog() method)
  6. Associated test classes
- Create PlatformEventPublisher utility framework
- Deploy Platform Event Health Dashboard
- Documentation and team training

**Out of Scope:**
- Platform Event subscriber refactoring
- Flow-based Platform Event publishing
- Historical data remediation

### Financial Benefits
**Quantitative Benefits:**
- **97.8% reduction in EventBus.publish() API calls** (450/hour → <25/hour)
- **80-95% reduction in overall Platform Event volume**
- **0% event drop rate** (currently ~98% dropped in CasetoQuote)

**Risk Avoidance:**
- Prevented production outages: $50,000+ per incident
- Avoided Salesforce licensing increases due to API consumption
- Complete audit trail maintained (compliance)

**Investment:**
- **Total Cost:** $52,080
- **ROI:** 200-400% over 3 years
- **Payback Period:** Immediate (prevented incident cost > project cost)

### Timeline
**Duration:** 5 weeks

| Week | Phase | Key Deliverables |
|------|-------|------------------|
| 1 | Baseline & Design | Baseline metrics, technical design, Fix #1-2 started |
| 2 | Critical Fixes | Fix #1-2 complete, Fix #3-4 development, security review |
| 3 | Framework & Testing | PlatformEventPublisher utility, QA test execution, dashboard |
| 4 | UAT & Finalization | UAT execution, documentation, training materials |
| 5 | Deployment | Production deployment, validation, team training |

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Senior Apex Developer (Offshore) | 1.0 | 5 weeks | 200 hrs | $4,000 |
| Project Manager (Onshore) | 1.0 | 5 weeks | 200 hrs | $11,538 |
| QA Engineer (Offshore) | 0.6 | 3 weeks | 72 hrs | $1,440 |
| DevOps Engineer (Offshore) | 0.2 | 5 weeks | 40 hrs | $800 |
| Business Analyst (Onshore) | 0.4 | 2 weeks | 32 hrs | $1,846 |
| Salesforce Admin (Offshore) | 0.2 | 5 weeks | 40 hrs | $800 |
| **Total** | | | **584 hours** | **$20,424** |

**Note:** Budget table in charter shows $52,080 total which includes additional overhead not detailed in the labor breakdown shown.

**Critical Success Factors:**
- CasetoQuoteAutomation fix addresses data loss issue
- Integration with Genesys CTI remains stable
- Monitoring dashboards provide real-time visibility

---

## PROJECT 6: Workflow Rule and Process Builder Migration

### Scope
**In Scope:**
- Migrate 26 automation files to modern technologies:
  - 4 Active Process Builders → Flow Builder or Apex
  - 7 Draft/Inactive Process Builders → Archive
  - 22 Active Workflow Rules → Flow Builder or Apex
  - 19 Inactive Workflow Rules → Archive
- Replace 6 Outbound Messages with Platform Events + Apex:
  - Acorn integrations (Case, WorkOrder, Quote, Comment)
  - Genesys integrations (Email routing, Task routing, Reporting)
- Create monitoring dashboards for all integrations

**Out of Scope:**
- New feature development
- Historical data remediation
- Other technical debt items

### Financial Benefits
**Cost Avoidance (3-Year Projection):**

| Benefit Category | Year 1 | Year 2 | Year 3 | Total |
|------------------|--------|--------|--------|-------|
| Avoided Support Costs | $30,000 | $45,000 | $60,000 | $135,000 |
| Integration Reliability | $25,000 | $35,000 | $45,000 | $105,000 |
| Developer Productivity | $15,000 | $20,000 | $25,000 | $60,000 |
| Platform Event Volume | $10,000 | $15,000 | $20,000 | $45,000 |
| **Total** | **$80,000** | **$115,000** | **$150,000** | **$345,000** |

**Investment:**
- **Total Cost:** $39,666
- **3-Year ROI:** 770%
- **Payback Period:** 6.0 months

### Timeline
**Duration:** 16 weeks

| Weeks | Phase | Key Deliverables |
|-------|-------|------------------|
| 1 | Preparation | Environment setup, baseline metrics, communication |
| 2-7 | Phase 1: Critical Integrations | Acorn (Case, WorkOrder, Quote), Email-to-Case, Genesys routing |
| 8-11 | Phase 2: Field Updates & Logic | Contact, Business Rule, Account, Supplier, simple field updates |
| 12 | Phase 3: Cleanup | Archive inactive automations, documentation |
| 13-16 | Post-Migration | Monitoring, stabilization, optimization |

**Phase Breakdown:**
- **Phase 1 (6 weeks):** 166 hours - Critical external integrations
- **Phase 2 (4 weeks):** 113 hours - Field updates and business logic
- **Phase 3 (1 week):** 15 hours - Cleanup and archival
- **Post-Migration (3 weeks):** 45 hours - Stabilization and optimization

### Resource Requirements

| Role | FTE | Duration | Total Hours | Cost |
|------|-----|----------|-------------|------|
| Lead Developer (Offshore) | 1.0 | 16 weeks | 512 hrs | $10,240 |
| Developer 2 (Offshore) | 0.75 | 12 weeks | 288 hrs | $5,760 |
| Developer 3 (Offshore) | 0.5 | 8 weeks | 160 hrs | $3,200 |
| QA Engineer (Offshore) | 0.5 | 12 weeks | 240 hrs | $4,800 |
| Salesforce Admin (Offshore) | 0.25 | 16 weeks | 160 hrs | $3,200 |
| Integration Specialist (Offshore) | 0.25 | 8 weeks | 80 hrs | $1,600 |
| Project Manager (Onshore) | 0.25 | 16 weeks | 64 hrs | $3,692 |
| **Total** | | | **1,504 hours** | **$32,492** |

**Additional Costs:**
- Tools & Testing: $2,000
- Contingency (15%): $5,174
- **Grand Total:** $39,666

**Critical Compliance Note:**
- **Salesforce End of Support:** December 31, 2025 (PASSED)
- Project is now **OVERDUE** - no support or bug fixes available
- Creates compliance risk and audit findings

---

## Recommended Project Sequencing

### Immediate Start (Q1 2026) - CRITICAL PATH

#### Track 1: Compliance & Stability (MUST DO)
```
Week 1-18: API Version Upgrade (CRITICAL)
  ├─ Parallel with ─→ Week 1-16: Workflow/Process Builder Migration (CRITICAL)
  └─ Parallel with ─→ Week 1-5: Platform Event Volume Reduction (HIGH)
```

**Rationale:**
1. **API Upgrade (18 weeks):** Breaking changes threaten production stability
2. **Workflow Migration (16 weeks):** Past End of Support deadline - compliance risk
3. **Platform Event Reduction (5 weeks):** Currently losing data (98% drop rate)

**Resource Requirements:**
- **API Upgrade:** 2 developers + PM + QA (offshore/onshore mix)
- **Workflow Migration:** 2-3 developers + PM + QA (offshore/onshore mix)
- **Platform Event:** 1 developer + QA (5 weeks, offshore)

**Total Q1 Investment:** $164,801 (API + Workflow + Platform Event)

---

### Q2 2026 Start - HIGH VALUE

#### Track 2: Contact Search Modernization (Sequential)
```
Week 1-6: Apex Refactoring (Phase 1) - PREREQUISITE
  └─ Then Choose ONE:
       Option A: Week 7-14: As-Is LWC Migration (8 weeks) [$27K]
       Option B: Week 7-20: Redesigned LWC (14 weeks) [$125K]
```

**Decision Matrix: As-Is vs Redesign**

| Factor | As-Is (Option A) | Redesign (Option B) | Winner |
|--------|------------------|---------------------|---------|
| **Cost** | $27,542 | $124,614 | ✅ As-Is |
| **Duration** | 8 weeks | 14 weeks | ✅ As-Is |
| **Annual ROI** | $37,040 | $472,750 | ✅ Redesign |
| **Payback Period** | 11 months | 3.2 months | ✅ Redesign |
| **3-Year ROI %** | 304% | 1,038% | ✅ Redesign |
| **Training Required** | Minimal | Moderate | ✅ As-Is |
| **User Adoption Risk** | Very Low | Low-Medium | ✅ As-Is |

**Recommendation:**
- **IF Budget Constrained:** Choose As-Is ($48,635 total for Phase 1 + 2)
- **IF Budget Available:** Choose Redesign ($145,707 total for Phase 1 + 3)
  - **Why Redesign Wins:** 12.7x higher annual ROI ($472K vs $37K), payback in 3.2 months, transforms user experience

**Q2 Investment (Phase 1 only):** $21,093

---

## Financial Summary by Quarter

### Q1 2026 (Immediate Start)

| Project | Duration | Cost | Annual ROI | Priority |
|---------|----------|------|------------|----------|
| API Version Upgrade | 18 weeks | $73,055 | $140,000 | CRITICAL |
| Workflow/PB Migration | 16 weeks | $39,666 | $80,000 | CRITICAL |
| Platform Event Reduction | 5 weeks | $52,080 | Risk Avoidance | HIGH |
| **Q1 Total** | | **$164,801** | **$220,000+** | |

**Q1 ROI:** 133% (first year alone)

---

### Q2 2026 (Post-Q1 Completion)

| Project | Duration | Cost | Annual ROI | Priority |
|---------|----------|------|------------|----------|
| Contact Search Phase 1 (Apex) | 6 weeks | $21,093 | $218,980 | HIGH |
| **Followed by ONE of:** | | | | |
| Option A: As-Is LWC Migration | 8 weeks | $27,542 | $37,040 | MEDIUM |
| Option B: Redesigned LWC | 14 weeks | $124,614 | $472,750 | MEDIUM |

**Q2 Total (with As-Is):** $48,635 | Annual ROI: $256,020
**Q2 Total (with Redesign):** $145,707 | Annual ROI: $691,730

---

### Full Portfolio Cost & Benefits

#### Scenario 1: Minimum Investment (Q1 Required + Q2 As-Is)
- **Total Cost:** $213,436
- **Year 1 Benefits:** $476,020
- **Year 1 ROI:** 123%
- **3-Year Benefits:** $1,428,060
- **3-Year ROI:** 569%

#### Scenario 2: Maximum Investment (Q1 Required + Q2 Redesign)
- **Total Cost:** $310,508
- **Year 1 Benefits:** $911,710
- **Year 1 ROI:** 194%
- **3-Year Benefits:** $2,733,750
- **3-Year ROI:** 780%

**Recommendation:** **Scenario 2 (Maximum Investment)** - Higher upfront cost delivers 2.8x more value over 3 years

---

## Risk Assessment by Project

### Critical Risks Across Portfolio

| Risk | Affected Projects | Mitigation |
|------|------------------|------------|
| **Resource Constraint** | All projects | Stagger start dates, use offshore resources, dedicated teams |
| **Integration Breakage** | API Upgrade, Workflow Migration, Platform Event | Extensive testing, parallel runs, rollback plans |
| **User Adoption** | Contact Search Redesign | Comprehensive training, UAT with 30+ users, gradual rollout |
| **Compliance Failure** | Workflow Migration | Already past deadline - START IMMEDIATELY |
| **Data Loss** | Platform Event Reduction | Currently losing data - PRIORITIZE THIS |

---

## Executive Recommendations

### 1. Immediate Action Required (January 2026)

✅ **APPROVE and FUND:**
- API Version Upgrade ($73,055) - CRITICAL
- Workflow/Process Builder Migration ($39,666) - CRITICAL
- Platform Event Volume Reduction ($52,080) - HIGH

**Total Q1 Investment:** $164,801

**Rationale:** These are non-negotiable compliance and stability projects. Delays increase risk exponentially.

---

### 2. Q2 2026 Action (April 2026)

✅ **APPROVE and FUND:**
- Contact Search Apex Refactoring ($21,093) - Foundation

**Then DECIDE:**
- ⭐ **RECOMMENDED:** Redesigned LWC ($124,614) for maximum ROI
- Alternative: As-Is LWC ($27,542) if budget constrained

**Rationale:**
- Redesign delivers $472K annual value vs $37K for As-Is
- Payback in 3.2 months makes this a no-brainer investment
- User experience transformation worth the additional $97K

---

### 3. Resource Planning

**Q1 2026 Staffing Needs:**
- 4-5 Offshore Developers (full-time)
- 1-2 Onshore Technical Architects (part-time)
- 2-3 Offshore QA Engineers (part-time)
- 1 Onshore Project Manager (full-time)
- 1 Offshore Salesforce Admin (part-time)

**Q2 2026 Additional Needs (if Redesign chosen):**
- 1 Onshore Senior UX Designer (part-time)
- 1 Offshore UI Designer (part-time)
- 1 Onshore UX Researcher (part-time)

---

### 4. Budget Approval Request

**2026 Total Budget Request:**

| Priority | Projects | Total Cost | Expected ROI (Year 1) |
|----------|----------|------------|----------------------|
| **Must Fund (Q1)** | API Upgrade + Workflow Migration + Platform Event | $164,801 | $220,000+ (134% ROI) |
| **Should Fund (Q2)** | Contact Search Phase 1 + Redesign | $145,707 | $691,730 (375% ROI) |
| **Grand Total** | | **$310,508** | **$911,730** |

**3-Year Projected Value:** $2,733,750 (780% ROI)

---

## Conclusion

This portfolio represents **mandatory compliance projects** combined with **high-value strategic improvements** that will:

✅ Eliminate technical debt and compliance risks
✅ Modernize the Salesforce platform to current standards
✅ Dramatically improve system performance and reliability
✅ Deliver nearly $1M in annual productivity gains
✅ Position the organization for future scalability

**The recommended investment of $310,508 will return $2.7M+ over 3 years - a 780% ROI.**

**Critical Path:** Start Q1 projects IMMEDIATELY (already behind on Workflow migration deadline)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 19, 2026 | George Martin | Initial consolidated portfolio summary |

---

## Appendices

### Appendix A: Detailed Budget Breakdown

See individual project charters for complete budget details:
- Contact Search Phase 1: Project-Charter-1-Apex-Refactoring.md
- Contact Search Phase 2: Project-Charter-2-AsIs-LWC-Migration.md
- Contact Search Phase 3: Project-Charter-3-Redesigned-LWC.md
- API Version Upgrade: Project-Charter-API-Version-Upgrade.md
- Platform Event Reduction: PROJECT_CHARTER_Platform_Events_Reduction.md
- Workflow Migration: PROJECT_CHARTER_Workflow_Process_Builder_Migration.md

### Appendix B: Resource Rate Structure

**Offshore Resources:** $20/hour
- Developers (Apex, LWC, general)
- QA Engineers
- Salesforce Administrators

**Onshore Resources:** $57.69/hour (based on $120K annual salary)
- Technical Architects
- Project Managers
- Business Analysts
- UX Designers
- Accessibility Specialists

**Onshore UAT Users:** $24.04/hour (based on $50K annual salary)

### Appendix C: Dependencies Map

```
API Version Upgrade (18 weeks)
  └─ No dependencies, can start immediately

Workflow/Process Builder Migration (16 weeks)
  └─ No dependencies, MUST start immediately (overdue)

Platform Event Volume Reduction (5 weeks)
  └─ No dependencies, can start immediately

Contact Search Apex Refactoring (6 weeks)
  └─ No dependencies, can start immediately
  └─ PREREQUISITE FOR:
       ├─ Contact Search As-Is LWC (8 weeks)
       └─ Contact Search Redesigned LWC (14 weeks)
```

### Appendix D: Testing Standards

**All projects follow organizational testing standards:**
- **UAT and QA Testing:** Performed in full copy sandboxes
- **Production data:** Used for realistic testing scenarios
- **Apex Code Coverage:** Minimum 85% required
- **Jest Test Coverage (LWC):** Minimum 85% required
- **Integration Testing:** Required for all external system touchpoints
- **Performance Testing:** Required for all major changes
- **Regression Testing:** Required before production deployment

---

**END OF DOCUMENT**
