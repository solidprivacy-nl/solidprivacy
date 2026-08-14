# SolidPrivacy Current State

Status date: 2026-08-14

This is the project-local **human-readable projection** of coordination state. `control/PROJECT_STATE.json` is the machine-readable project-state contract; durable project decisions and live GitHub evidence outrank stale narrative text. Reconcile before consequential status reporting, routing, assurance or merge.

## Product state

- Product objective: controlled Privacy Officer operating system supporting both bounded privacy projects and Privacy Officer as a Service for EU/EEA + Netherlands.
- First reference vertical slice: DPIA/pre-scan.
- WP1–WP6 are implemented in the stacked draft line through PR #7.
- PR #8 extends architecture/roadmap from individual workflow execution into a general client engagement model plus durable POaaS client operating model, and adopts the client data-plane, project-governance and Control-freshness foundation.
- `PROJECT` and `MANAGED_SERVICE` are first-class engagement modes over the same governed privacy engine; workflow/service type is separate from engagement mode.
- The shared/public repository is not a customer dossier store.
- Real client processing is not yet production-enabled.
- No real external AI provider is approved merely by the existence of model interfaces/fixtures.

## Project-control state

Machine authority: `control/PROJECT_STATE.json`.

PR #8 implementation was reopened on 2026-08-14 after the principal requested explicit support for standalone assignments such as a DPIA. The previous assurance handover was withdrawn before acceptance because this is a semantic architecture refinement and therefore requires a new candidate identity and fresh assurance.

The current refinement adds:

- first-class `PROJECT` and `MANAGED_SERVICE` engagement modes;
- separation of engagement mode from service/workflow type;
- `RUN_SCOPED`, `ENGAGEMENT_SCOPED` and `ORGANISATION_SCOPED` state semantics;
- explicit promotion from project state into durable organisation state;
- engagement-aware retention/offboarding and continuous change propagation;
- M1 interpretation as the first standalone professional-service `PROJECT + DPIA` execution;
- preservation of generalized production engagement contracts for WP9 after the assured Client Data Plane;
- existing machine-readable freshness-bound project state, next-gate ownership, scope protection, candidate identity and project/privacy decision-plane separation.

Central `market-predictions/control-plane` is a coordination/freshness-bound cache layer for project status. It does not become SolidPrivacy's project-specific source of truth.

## Active integration line

```text
claim_id=SP-WC-0008
claim_status=ACTIVE
pull_request=PR #8
branch=agent/poaas-client-operating-roadmap
target=agent/privacy-officer-review-package
live_head=reconstruct_from_github
machine_state=control/PROJECT_STATE.json
claim_register=control/WORK_CLAIMS.json
previous_handover=WITHDRAWN_BEFORE_ACCEPTANCE
```

Recorded SHAs are reconciliation observations. The live branch/PR/target heads must be reconstructed at mandatory gates; a file cannot safely promise its own containing commit SHA.

## Engagement architecture

Authoritative engagement-layer contract: `docs/ENGAGEMENT_ARCHITECTURE.md`.

```text
PROJECT
  bounded professional-service assignment
  default state = ENGAGEMENT_SCOPED
  no implicit continuous monitoring
  explicit closeout/retention

MANAGED_SERVICE
  continuous contracted privacy service
  accepted reusable state may be ORGANISATION_SCOPED
  dependency-driven reassessment within contracted scope
  service-period/offboarding lifecycle
```

Examples such as DPIA, vendor review, breach, DSAR or transfer assessment are service/workflow types. They do not get separate legal implementations for project versus managed-service delivery.

## Scope protection

### CURRENT_RELEASE

- close PR #8 architecture/data/governance foundation;
- Control freshness/machine-state alignment;
- candidate identity and exact-head assurance semantics;
- project-control versus privacy/legal decision-plane separation;
- first-class project versus managed-service engagement architecture;
- engagement-scoped state, explicit promotion, retention/offboarding and continuation semantics;
- fresh exact-head candidate/evidence and independent assurance after this semantic refinement.

### NEXT_RELEASE

- M1 standalone `PROJECT + DPIA` chained execution with positive and blocked/adversarial paths;
- minimal synthetic engagement envelope only;
- M1 HMPO/cycle-time/model-compute telemetry primitives;
- after M1 and shared execution/data-plane work: WP9 generalized production organisation/engagement contracts.

### PARKING_LOT

- pooled multi-tenant Client Data Plane optimisation;
- large GRC-style management UI;
- broad multi-jurisdiction expansion.

New insights are recorded, but do not silently enter `CURRENT_RELEASE` unless required for safety, correctness or the stated outcome.

## Current candidate scope

PR #8 now covers:

- generic engagement architecture for bounded project and managed-service delivery;
- POaaS client/engagement/persistent-state specialization;
- POaaS reference onboarding workflow;
- roadmap sequencing through M2;
- private Client Data Plane architecture and AI-access boundary;
- POaaS unit-economics/HMPO measurement requirements;
- project-local GitHub source-of-truth governance;
- work-claim/branch lifecycle adoption;
- Control state-freshness/reconciliation architecture;
- machine project-state and next-gate contract;
- candidate identity/exact-head semantics;
- project release-assurance contract;
- static governance CI gate.

## Next product gate

### M1 — Standalone `PROJECT + DPIA` chained reference execution

After PR #8 architecture/governance closeout, the next product implementation milestone remains M1:

```text
minimal project engagement/scope
 -> evidence
 -> extraction
 -> provenance/readiness
 -> pre-scan
 -> legal context
 -> governed analysis
 -> Privacy Officer review
 -> report/reinsert
 -> audit
 -> explicit synthetic closeout/retention disposition
```

M1 requires both a positive and a blocked/adversarial synthetic path as one correlated execution. It must prove no accidental promotion into organisation-wide managed state. It does not production-enable real client persistence and does not pull the full WP9 engagement platform forward.

## Newly established prerequisites after M1

Before durable real client state is production-enabled:

1. generalized workflow/audit substrate;
2. Client Data Plane implementation/security assurance;
3. generalized client/organisation/engagement contracts including `PROJECT | MANAGED_SERVICE` policies;
4. persistent organisational privacy state/dependency model;
5. control/evidence/finding/remediation model;
6. hardened production model gateway where external AI is used.

The roadmap/workpackage architecture is authoritative for exact numbering/order.

## Data posture

Target initial production posture for healthcare clients:

- dedicated EU/EEA client data project/account per client;
- separate encrypted evidence/object store, structured state database and tenant-scoped retrieval index;
- per-client key/credential scope;
- AI receives bounded retrieved/minimised context rather than database access;
- no cross-client model memory;
- original identifiers/Scrub Keys excluded from external AI paths;
- public/shared GitHub remains free of real client evidence;
- within a client boundary, engagement-scoped project state is logically distinct from organisation-scoped managed state and follows explicit retention/promotion policy.

See `docs/DATA_ARCHITECTURE.md` and `docs/ENGAGEMENT_ARCHITECTURE.md`.

## Governance posture

Project-local governance follows the canonical `market-predictions/control-plane` operating method for consequential work.

Authoritative local records include:

- `control/PROJECT_GOVERNANCE_BOOTSTRAP.md`
- `control/PROJECT_STATE.json`
- `CURRENT_STATE.md` (human projection)
- `ROADMAP.md`
- `WORKPACKAGES.md`
- `CHANGELOG.md`
- `DECISION_LOG.md`
- `control/WORK_CLAIMS.json`
- `handover/`
- `docs/PROJECT_CONTROL_ARCHITECTURE.md`
- `docs/ENGAGEMENT_ARCHITECTURE.md`
- `docs/architecture.md`
- relevant tests/evals/Actions evidence

`implementation_operations` cannot certify its own release. Material candidates require independent `governance_release_assurance` under `control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md`.

The Control D0–D3 framework applies to project/development decisions only. It does not override runtime Privacy Officer/DPO/FG/legal review requirements.

## Open risks / unresolved decisions

- Production Client Data Plane technology/provider has not yet been selected or approved.
- Dedicated-per-client isolation is the initial architecture recommendation; any later pooled multi-tenancy requires separate isolation assurance.
- Real model-provider production approval remains outstanding.
- M1 has not yet proven the full standalone DPIA chain as one run.
- M2 has not yet proven end-to-end `MANAGED_SERVICE` POaaS onboarding or measured production-like HMPO/unit economics.
- The generalized production engagement contract remains intentionally deferred to WP9 after the Client Data Plane; M1 uses only a synthetic minimal envelope.
- The stacked PR lineage must remain reconciled as dependencies merge; stale integration lines may not keep accumulating.
- SolidPrivacy central control-plane enrollment remains a post-merge follow-up under issue #9.

## Principal decisions currently required

None for the current architecture refinement. Provider selection, commercial pricing and any relaxation from dedicated tenant isolation remain future consequential decisions after evidence is available.
