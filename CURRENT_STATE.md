# SolidPrivacy Current State

Status date: 2026-08-11

This is the project-local human-readable current-state view. Live GitHub branch/PR/Actions evidence outranks stale text in this file. Reconcile before presenting consequential status or starting assurance.

## Product state

- Product objective: controlled Privacy Officer operating system / POaaS for EU/EEA + Netherlands.
- First reference vertical slice: DPIA/pre-scan.
- WP1–WP6 are implemented in the stacked draft line through PR #7.
- PR #8 extends architecture/roadmap from individual workflow execution into the durable POaaS client operating model and now also adopts the client data-plane and project-governance foundation.
- The shared/public repository is not a customer dossier store.
- Real client processing is not yet production-enabled.
- No real external AI provider is approved merely by the existence of model interfaces/fixtures.

## Active integration line

```text
claim_id=SP-WC-0008
pull_request=PR #8
branch=agent/poaas-client-operating-roadmap
target=agent/privacy-officer-review-package
live_head=reconstruct_from_github
claim_register=control/WORK_CLAIMS.json
```

The recorded claim head is an observed reconciliation point. The branch may advance as this governance/data-architecture package is completed; exact live head must be reconstructed before assurance or merge.

## Current candidate scope

PR #8 now covers:

- POaaS client/engagement/persistent-state architecture;
- POaaS reference onboarding workflow;
- roadmap sequencing through M2;
- private Client Data Plane architecture and AI-access boundary;
- POaaS unit-economics/HMPO measurement requirements;
- project-local GitHub source-of-truth governance;
- work-claim/branch lifecycle adoption;
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

M1 requires both a positive and a blocked/adversarial synthetic path as one correlated execution.

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

Project-local governance now follows the canonical `market-predictions/control-plane` operating method for consequential work.

Authoritative local records:

- `control/PROJECT_GOVERNANCE_BOOTSTRAP.md`
- `CURRENT_STATE.md`
- `ROADMAP.md`
- `WORKPACKAGES.md`
- `CHANGELOG.md`
- `DECISION_LOG.md`
- `control/WORK_CLAIMS.json`
- `handover/`
- `docs/architecture.md`
- relevant tests/evals/Actions evidence

`implementation_operations` cannot certify its own release. Material candidates require independent `governance_release_assurance` under `control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md`.

## Open risks / unresolved decisions

- Production Client Data Plane technology/provider has not yet been selected or approved.
- Dedicated-per-client isolation is the initial architecture recommendation; any later pooled multi-tenancy requires separate isolation assurance.
- Real model-provider production approval remains outstanding.
- M1 has not yet proven the full DPIA chain as one run.
- M2 has not yet proven end-to-end POaaS onboarding or measured production-like HMPO/unit economics.
- The stacked PR lineage must remain reconciled as dependencies merge; stale integration lines may not keep accumulating.

## Principal decisions currently required

None for the architecture/governance package. Provider selection, commercial pricing and any relaxation from dedicated tenant isolation remain future consequential decisions after evidence is available.
