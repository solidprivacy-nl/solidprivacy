# SolidPrivacy Release Assurance Contract V1

## Status

```text
contract_id=SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1
project=solidprivacy-nl/solidprivacy
implementation_role=implementation_operations
assurance_role=governance_release_assurance
exact_head_required=true
blind_initial_review=true
```

## Purpose

SolidPrivacy performs privacy-sensitive AI processing and creates legal/compliance decision-support artefacts. A passing implementation test or a narrative work claim is not sufficient to establish a trustworthy release. Consequential candidates require independent reconstruction against the exact candidate head.

## Trigger

Use independent release assurance for material changes to:

- legal-source or legal-rule handling;
- canonical privacy contracts/state;
- evidence/provenance handling;
- model-call/egress/privacy policy;
- tenant/client-data isolation;
- Scrub/reinsert boundaries;
- human-review/finalisation gates;
- workflow orchestration/audit;
- production data-plane/storage/security configuration;
- client-facing deliverable generation;
- claims that a workpackage/milestone is complete or production-ready.

Pure editorial documentation can use a proportionate path only when it does not change authority, sequencing, acceptance criteria, security posture or production claims.

## Initial blind-review boundary

Before recording its initial `PASS | FAIL | INDETERMINATE`, assurance must not rely on:

- implementation self-assessment;
- implementation handover conclusions;
- PR narrative claims that describe what should be true;
- prior PASS evidence from an ancestor head as authorization for a descendant.

Assurance may and should read:

- the principal's requested outcome;
- project governance bootstrap;
- current roadmap/workpackage/decision records;
- candidate source/diff;
- schemas/contracts;
- test/eval definitions;
- raw GitHub Actions evidence on the exact head;
- approved legal/source registries where relevant;
- live target/data-plane evidence required by the acceptance contract.

After the initial verdict, handover/implementation narrative may be read to check administrative completeness or identify undisclosed scope.

## Exact-head rule

The assurance verdict binds only to the exact reviewed candidate SHA.

Any repair, rebase, cherry-pick, dependency reconciliation, generated release-output commit or security/configuration mutation produces a new candidate identity. Required assurance must be rerun on the surviving exact head.

## Required assurance dimensions

Depending on scope, reconstruct at least:

1. **Source/contract correctness** — schemas, referential integrity, deterministic gates.
2. **Privacy boundary** — direct identifiers/Scrub Key/model-egress restrictions.
3. **Legal-source governance** — authority, jurisdiction, freshness and claim binding.
4. **Evidence provenance** — results trace to exact evidence/support or stay unresolved.
5. **Human accountability** — high-impact conclusions cannot self-finalise.
6. **Tenant/data isolation** — cross-tenant negative paths, access policy, retrieval scope, secrets/log boundaries.
7. **Execution/audit** — run/version/hash lineage and blocked/failure semantics.
8. **Output/delivery** — generated artefacts represent reviewed state and preserve lineage.
9. **Governance lifecycle** — roadmap/workpackage/work claim/handover/current-state records agree with live GitHub.
10. **Post-action confirmation** — merge/deploy/data migration success is separately confirmed on the target state.

## Verdict semantics

### PASS

All required acceptance conditions are evidenced on the exact candidate and no material unresolved contradiction remains.

### FAIL

A required acceptance/security/legal/privacy condition is demonstrably violated.

### INDETERMINATE

Evidence is insufficient, unavailable, contradictory, stale or not tied to the exact candidate. Missing evidence is never inferred as success.

## Implementation/assurance separation

Implementation may repair after `FAIL` or `INDETERMINATE`, but assurance may not silently make the repair itself and then certify its own modification.

The repair is a new candidate and returns through the required assurance path.

## Production data-plane rule

For a candidate that enables real client data processing, code/CI PASS alone is insufficient. The assurance package must include target-environment evidence appropriate to scope, for example:

- tenant isolation configuration and negative test;
- EU/EEA storage/backup configuration;
- key/secrets posture;
- retrieval-index tenant binding;
- provider/model egress policy;
- logging/telemetry content policy;
- deletion/retention behaviour;
- deployment health/migration result.

Do not put sensitive target evidence itself into a public repository when it contains secrets or customer data. Store sanitized proofs/hashes/opaque references and keep sensitive evidence in the approved private assurance store.

## Completion rule

A workpackage is not governance-complete until:

- implementation scope is complete or explicitly deferred;
- exact-head tests/evidence are available;
- required assurance verdict is recorded;
- work claim is terminal or validly transferred;
- handover/disposition is complete where required;
- current state/roadmap/changelog/decision records are reconciled;
- production action and post-action confirmation are distinct and complete where applicable.
