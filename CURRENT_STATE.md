# SolidPrivacy Current State

Status date: 2026-08-11

This is the project-local **human-readable projection** of coordination state. `control/PROJECT_STATE.json` is the machine-readable project-state contract; durable project decisions and live GitHub evidence outrank stale narrative text. Reconcile before consequential status reporting, routing, assurance or merge.

## Product state

- Product objective: controlled Privacy Officer operating system / POaaS for EU/EEA + Netherlands.
- First reference vertical slice: DPIA/pre-scan.
- WP1–WP6 are implemented in the stacked draft line through PR #7.
- PR #8 extends architecture/roadmap from individual workflow execution into the durable POaaS client operating model and adopts the client data-plane, project-governance and Control-freshness foundation.
- The shared/public repository is not a customer dossier store.
- Real client processing is not yet production-enabled.
- No real external AI provider is approved merely by the existence of model interfaces/fixtures.

## Project-control state

Machine authority: `control/PROJECT_STATE.json`.

Current objective is to close PR #8 under the updated Control architecture without expanding the next product milestone. The current control alignment adds:

- machine-readable freshness-bound project state;
- explicit next-gate owner/principal-decision contract;
- `CURRENT_RELEASE / NEXT_RELEASE / PARKING_LOT` scope protection;
- explicit implementation-candidate versus live-branch versus administrative-descendant semantics;
- strict separation between project D0–D3 decisions and privacy/legal runtime accountability.

Central `market-predictions/control-plane` is a coordination/freshness-bound cache layer for project status. It does not become SolidPrivacy's project-specific source of truth.

## Active integration line

```text
claim_id=SP-WC-0008
pull_request=PR #8
branch=agent/poaas-client-operating-roadmap
target=agent/privacy-officer-review-package
live_head=reconstruct_from_github
machine_state=control/PROJECT_STATE.json
claim_register=control/WORK_CLAIMS.json
```

Recorded SHAs are reconciliation observations. The live branch/PR/target heads must be reconstructed at mandatory gates; a file cannot safely promise its own containing commit SHA.

## Scope protection

### CURRENT_RELEASE

- close PR #8 POaaS architecture/data/governance foundation;
- Control freshness/machine-state alignment;
- candidate identity and exact-head assurance semantics;
- project-control versus privacy/legal decision-plane separation.

### NEXT_RELEASE

- M1 chained DPIA reference execution;
- M1 HMPO/cycle-time/model-compute telemetry primitives.

### PARKING_LOT

- pooled multi-tenant Client Data Plane optimisation;
- large GRC-style management UI;
- broad multi-jurisdiction expansion.

New insights are recorded, but do not silently enter `CURRENT_RELEASE` unless required for safety, correctness or the stated outcome.

## Current candidate scope

PR #8 covers:

- POaaS client/engagement/persistent-state architecture;
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

### M1 — Chained DPIA reference execution

After PR #8 architecture/governance closeout, the next product implementation milestone remains M1:

```text
evidence
 -> extraction
 -> provenance/readiness
 -> pre-scan
 -> legal context
 -> governed analysis
 -> Privacy Officer review
 -> report/reinsert
 -> audit
```

M1 requires both a positive and a blocked/adversarial synthetic path as one correlated execution. This governance alignment must not insert another product implementation milestone before M1.

## Newly established prerequisites after M1

Before durable real client state is production-enabled:

1. generalized workflow/audit substrate;
2. Client Data Plane implementation/security assurance;
3. client/organisation/engagement contracts;
4. persistent organisational privacy state/dependency model;
5. control/evidence/finding/remediation model;
6. hardened production model gateway where external AI is used.

The roadmap is authoritative for exact numbering/order.

## Data posture

Target initial production posture for healthcare clients:

- dedicated EU/EEA client data project/account per client;
- separate encrypted evidence/object store, structured state database and tenant-scoped retrieval index;
- per-client key/credential scope;
- AI receives bounded retrieved/minimised context rather than database access;
- no cross-client model memory;
- original identifiers/Scrub Keys excluded from external AI paths;
- public/shared GitHub remains free of real client evidence.

See `docs/DATA_ARCHITECTURE.md`.

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
- `docs/architecture.md`
- relevant tests/evals/Actions evidence

`implementation_operations` cannot certify its own release. Material candidates require independent `governance_release_assurance` under `control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md`.

The Control D0–D3 framework applies to project/development decisions only. It does not override runtime Privacy Officer/DPO/FG/legal review requirements.

## Open risks / unresolved decisions

- Production Client Data Plane technology/provider has not yet been selected or approved.
- Dedicated-per-client isolation is the initial architecture recommendation; any later pooled multi-tenancy requires separate isolation assurance.
- Real model-provider production approval remains outstanding.
- M1 has not yet proven the full DPIA chain as one run.
- M2 has not yet proven end-to-end POaaS onboarding or measured production-like HMPO/unit economics.
- The stacked PR lineage must remain reconciled as dependencies merge; stale integration lines may not keep accumulating.
- SolidPrivacy central control-plane enrollment remains a post-merge follow-up under issue #9.

## Principal decisions currently required

None for the current architecture/governance alignment. Provider selection, commercial pricing and any relaxation from dedicated tenant isolation remain future consequential decisions after evidence is available.
