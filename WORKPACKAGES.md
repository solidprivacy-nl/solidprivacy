# SolidPrivacy Workpackage Index

This file is the authoritative project-local index of executable workpackages. `ROADMAP.md` owns strategic sequencing; detailed workpackage files define executable scope/acceptance. A roadmap item may be planned before a detailed workpackage exists, but implementation may not become consequential `ACTIVE` work until its workpackage contract and claim are repository-backed.

Project execution state is machine-readable in `control/PROJECT_STATE.json`; this index does not replace current-state/freshness reconstruction.

## Status semantics

- `PLANNED` — roadmap sequence exists; detailed package may still need authoring.
- `READY` — dependencies satisfied and detailed package/acceptance exists; claim may be opened.
- `ACTIVE` — one or more reconciled work claims own implementation scope.
- `BLOCKED` — active scope cannot responsibly proceed.
- `IMPLEMENTED` — implementation candidate exists; assurance/closeout may still be outstanding.
- `COMPLETE` — applicable exact-head assurance, claim disposition, handover/closeout and source-of-truth updates are complete.
- `SUPERSEDED` — replaced by a named successor package/line.

## Foundation / current architecture-governance package

| ID | Name | Status | Specification / evidence |
|---|---|---|---|
| WP0 | Privacy operating architecture | COMPLETE IN DRAFT STACK | PR #1 + repository architecture/source governance |
| GOVDATA-FOUNDATION-2026-08-11 | POaaS client model + data plane + project governance foundation | ACTIVE | PR #8; `docs/POAAS_REFERENCE_WORKFLOW.md`; `docs/DATA_ARCHITECTURE.md`; `docs/POAAS_OPERATING_ECONOMICS.md`; `docs/PROJECT_CONTROL_ARCHITECTURE.md`; `control/PROJECT_GOVERNANCE_BOOTSTRAP.md`; `control/PROJECT_STATE.json`; claim `SP-WC-0008` |

The Control freshness/machine-state/candidate-identity refinement is part of this existing foundation package. It does **not** create a new product milestone before M1.

## DPIA reference vertical slice

| ID | Name | Status | Detailed specification |
|---|---|---|---|
| WP1 | Canonical privacy + Dutch DPIA model | COMPLETE | `docs/workpackages/WP1_CANONICAL_DPIA_MODEL.md` |
| WP2 | Executable DPIA contracts + pre-scan | COMPLETE | `docs/workpackages/WP2_EXECUTABLE_DPIA_PRESCAN.md` |
| WP3 | Evidence + fact provenance | COMPLETE | `docs/workpackages/WP3_EVIDENCE_FACTS.md` |
| WP4 | Safe AI boundary + fact extraction validator | COMPLETE | `docs/workpackages/WP4_AI_FACT_EXTRACTION.md` |
| WP5 | Governed legal context + DPIA analysis | COMPLETE | `docs/workpackages/WP5_GOVERNED_DPIA_ANALYSIS.md` |
| WP6 | Privacy Officer review + report/reinsert | IMPLEMENTED | `docs/workpackages/WP6_PRIVACY_OFFICER_REVIEW.md`; PR #7; integration closeout remains governed by live stack state |
| M1 | Chained DPIA reference execution milestone | PLANNED / NEXT PRODUCT GATE | Acceptance in `ROADMAP.md`; detailed execution workpackage must be created before activation |

## Shared operating/client substrate

The numbering below is authoritative once the PR #8 roadmap package is accepted.

| ID | Name | Status | Detailed spec requirement |
|---|---|---|---|
| WP7 | Generalized workflow execution + audit model | PLANNED | Create detailed package after M1 PASS |
| WP8 | Client Data Plane + tenant/security boundary | PLANNED | `docs/workpackages/WP8_CLIENT_DATA_PLANE.md` |
| WP9 | Client / organisation / engagement operating model | PLANNED | Create before activation |
| WP10 | Persistent organisational privacy state + dependency graph | PLANNED | Create before activation |
| WP11 | Executable control/evidence/finding/remediation model | PLANNED | Create before activation |
| WP12 | Model gateway + privacy-policy hardening | PLANNED | Create before activation |

## POaaS onboarding reference slice

| ID | Name | Status | Detailed spec requirement |
|---|---|---|---|
| WP13 | Engagement onboarding + evidence request orchestration | PLANNED | Create before activation |
| WP14 | RoPA / processing inventory backbone | PLANNED | Create before activation |
| WP15 | Privacy baseline + action plan + deliverable projection | PLANNED | Create before activation |
| M2 | Synthetic medium-sized Dutch home-care POaaS onboarding acceptance | PLANNED | Acceptance in `ROADMAP.md`; include unit-economics report |

## Later workflow expansion

After M2, create separately claimed workpackages for breach, vendor/Article 28, DSAR, transfers, retention/deletion and AI privacy/rights-assessment coordination. Do not activate them as bespoke agents outside the shared client-state/data-plane substrate.

## Workpackage creation contract

Before a planned item becomes `ACTIVE`, its detailed workpackage must state at least:

```text
workpackage_id
outcome
scope
non_goals
dependencies
authority/contracts affected
privacy/security/legal constraints
acceptance criteria
tests/evidence
required documentation updates
assurance route
definition of done
```

Then create/reconcile a machine-readable ownership claim in `control/WORK_CLAIMS.json` under the canonical work-claim/branch lifecycle standard and update `control/PROJECT_STATE.json` with the active objective/scope/next gate.

## Completion contract

A workpackage is `COMPLETE` only if, where applicable:

- implementation scope is complete or explicitly deferred;
- exact candidate is identifiable;
- required CI/evals/tests pass on that exact head;
- independent assurance has issued a valid verdict;
- production action and post-action confirmation are separated and evidenced;
- claim is `CLOSED`, validly `TRANSFER`red or `SUPERSEDED`;
- handover/disposition is recorded when ownership/lineage changed;
- `control/PROJECT_STATE.json` and `CURRENT_STATE.md` converge with live state;
- `ROADMAP.md`, `CHANGELOG.md` and `DECISION_LOG.md` are reconciled.
