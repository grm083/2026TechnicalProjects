# Project Briefer: Workflow Rule & Process Builder Migration

**Project Code:** PBWR-2026
**Audience:** Executive Leadership, IT Governance, Development & Admin Teams
**Author:** George Martin, Salesforce Technical Architect
**Date:** May 12, 2026
**Read Time:** ~5 minutes

---

## 1. What This Project Is

The Workflow Rule and Process Builder Migration is a 16-week initiative to retire every active Workflow Rule and Process Builder in our Salesforce org and replace it with modern, supported automation — **Flow Builder, Apex Triggers, and Platform Events**. The work spans **11 Process Builders** and **15 Workflow Rule files** (~50 individual rules) touching mission-critical domains: Case management, Email-to-Case, Genesys CTI routing, Acorn field-service integration, CPQ quoting, and the Business Rules engine.

The full scope is captured across five companion documents in this folder:
- `PROJECT_CHARTER_Workflow_Process_Builder_Migration.md` — scope, budget, ROI, governance
- `AUTOMATION_MIGRATION_ANALYSIS.md` — per-rule technical assessment
- `FUNCTIONAL_TECHNICAL_DESIGN_Workflow_Modernization.md` — target architecture
- `ACCEPTANCE_CRITERIA_BY_OBJECT.md` — object-by-object acceptance gates
- `QA_TESTING_CHECKLIST_Workflow_Modernization.md` / `UAT_CHECKLIST_Workflow_Modernization.md` — validation plans

---

## 2. Why It Matters — Salesforce's Official End of Support

Per Salesforce Help Article [001096524](https://help.salesforce.com/s/articleView?id=001096524&language=en_US&type=1):

> "The official 'End of Support' date for Workflow Rules and Process Builder is December 31, 2025. While these tools will continue to function, they will no longer be backed by Salesforce's support team. If you have active Workflow Rules or Process Builder processes running beyond 2025, you will no longer be able to receive support, and any bugs will no longer be fixed."

Salesforce's published retirement timeline:

| Release | Milestone |
|---------|-----------|
| Winter '23 | No new Workflow Rules can be created |
| Summer '23 | No new Process Builders can be created |
| **Dec 31, 2025** | **Official End of Support** |
| Jan 1, 2026 → today | No bug fixes, no support cases accepted |

Salesforce's own guidance directs customers to migrate to Flow. The Trailhead module [Migrate Workflows and Processes to Flows](https://trailhead.salesforce.com/content/learn/projects/migrate-workflows-and-processes-to-flows) and the in-platform **Migrate to Flow** tool ([Help article](https://help.salesforce.com/s/articleView?id=platform.flow_migrate_to_flow.htm)) exist specifically to accelerate this transition. The Salesforce Admins blog post [Go with the Flow](https://admin.salesforce.com/blog/2021/go-with-the-flow-whats-happening-with-workflow-rules-and-process-builder) frames Flow as the platform's strategic, forward-investment automation tool.

**As of today (May 2026), we are already five months past End of Support.** Every active rule running in production is unsupported code. The business risk is no longer theoretical:

- **No bug fixes, no security patches, no support cases** for any failure in our Email-to-Case pipeline, Acorn/Genesys integrations, or CPQ quoting automation.
- **Outbound Messages** — used by 6 of our integration workflows — are legacy technology with no retry logic, no monitoring, and a hard 24-hour retry window. Failures today are silent.
- **Audit and IT governance exposure** — running unsupported software typically constitutes a finding under SOX, internal IT controls, and most enterprise governance frameworks.

This migration is not optional; it is compliance-mandated remediation of a known End-of-Life dependency.

---

## 3. Benefits to Our Developers and Administrators

Beyond simply being supported again, modern automation materially improves day-to-day life for the people who build, ship, and maintain our org.

### For Developers

- **One trigger per object, finally.** Today, Case logic lives across one draft Process Builder, 17 Workflow Rules, and an existing Apex trigger. After migration, `CaseTrigger` is the single source of truth. New hires can read it in an afternoon instead of chasing logic across three Setup screens.
- **Real debugging.** Apex stack traces, the Flow Debugger, and Platform Event monitoring replace the "guess-and-check" pattern of Process Builder, where a failed criteria node returns no actionable error.
- **Source control & CI/CD.** Flows and Apex live in metadata that diffs cleanly in Git. Process Builder XML, by contrast, is famously merge-hostile — a single admin edit in production can silently overwrite a developer's sandbox work.
- **Testable automation.** Apex triggers require ≥75% unit test coverage and Flow now supports Flow Tests. Today, our Process Builder logic has effectively zero automated regression coverage.
- **Modern integration patterns.** Replacing Outbound Messages with Platform Events + Queueable Apex gives us configurable retries, exponential backoff, dead-letter handling, and an Event Bus we can actually observe. Anecdotally, teams that have made this switch report integration success rates climbing from ~70–80% to 95%+ and Mean Time To Resolution dropping by roughly 5×.
- **Performance headroom.** Flow's Fast Field Updates run before-save and skip a DML round-trip — typically 50–70% fewer DML operations on hot-path objects like Case and EmailMessage. For complex logic, consolidated Apex triggers run 20–40% faster than the equivalent Process Builder.

### For Administrators

- **A visual canvas they actually want to use.** Flow Builder's drag-and-drop canvas is self-documenting; admins onboarding to our org can read a flow diagram instead of reverse-engineering a 20-row criteria table.
- **Versioning and safe rollback.** Every Flow save creates a new version. If a change misbehaves in production, an admin can activate the prior version in two clicks — a capability Workflow Rules never had.
- **Fault paths and notifications.** Flows can branch on failure, post to Chatter, or email an admin group. Today, a failed workflow field-update is invisible until an end user complains.
- **Scheduled automation without code.** Time-dependent actions (e.g., the Business_Rule__c expiration deactivations) move from rigid Workflow time triggers to a Scheduled Flow the admin team owns end-to-end.
- **Lower escalation rate to engineering.** Admins anecdotally tell us that ~30–40% of their current "open a ticket with dev" moments stem from Process Builder limitations (no loops, no record deletes, no callouts). Flow closes most of those gaps, letting admins ship more without a developer in the loop.
- **Trailhead-aligned skill growth.** Flow is Salesforce's flagship automation product going forward. Time invested learning it compounds; time invested fighting Process Builder does not.

---

## 4. Bottom Line

Salesforce ended support on December 31, 2025. Every Workflow Rule and Process Builder in our org is now unsupported, unpatched, and — for our integration rules — operating on a 24-hour-retry technology with no monitoring. This project closes that gap, consolidates fragmented automation into a maintainable trigger-and-Flow architecture, and pays back the migration cost in roughly six months through reduced incident time, faster admin throughput, and elimination of a known compliance finding.

**Recommended next step:** approve the Project Charter and assign the Project Manager / Lead Developer roles currently listed as `[TBD]` in Appendix C.

---

## Official Salesforce References

1. Salesforce Help — [Workflow Rules & Process Builder End of Support (Article 001096524)](https://help.salesforce.com/s/articleView?id=001096524&language=en_US&type=1)
2. Salesforce Help — [Migrate to Flow Tool](https://help.salesforce.com/s/articleView?id=platform.flow_migrate_to_flow.htm&language=en_US&type=5)
3. Salesforce Release Notes — [Convert Workflow Rules to Flows](https://help.salesforce.com/s/articleView?id=release-notes.rn_automate_flow_mgmt_migrate_to_flow_tool.htm&language=en_US&release=236&type=5)
4. Trailhead — [Migrate Workflows and Processes to Flows](https://trailhead.salesforce.com/content/learn/projects/migrate-workflows-and-processes-to-flows)
5. Salesforce Admins Blog — [Go with the Flow: What's Happening with Workflow Rules and Process Builder](https://admin.salesforce.com/blog/2021/go-with-the-flow-whats-happening-with-workflow-rules-and-process-builder)
