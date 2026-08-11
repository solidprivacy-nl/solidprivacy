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

SolidPrivacy performs privacy-sensitive AI processing and creates legal/compliance decision-support artefacts. A passing implementation test or a narrative work claim is not sufficient to establish a trustworthy release. Consequential candidates require independent reconstruction against exact candidate identity and evidence.

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
- project governance authority, acceptance or release semantics;
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
- project governance bootstrap and project-control architecture;
- current machine project state, roadmap/workpackage/decision records;
- candidate source/diff;
- schemas/contracts;
- test/eval definitions;
- raw GitHub Actions evidence on the applicable exact head(s);
- approved legal/source registries where relevant;
- live target/data-plane evidence required by the acceptance contract.

After the initial verdict, handover/implementation narrative may be read to check administrative completeness or identify undisclosed scope.

## Candidate identity and exact-head rule

SolidPrivacy distinguishes:

```text
implementation_candidate_sha
release_candidate_sha
live_branch_head
administrative_descendant_sha
```

- `implementation_candidate_sha` is the exact semantic/product/architecture candidate produced by implementation and covered by its substantive test/eval evidence.
- `release_candidate_sha` is the exact candidate that assurance is asked to certify for merge/release. It may equal the implementation candidate or be a strictly administrative descendant.
- `live_branch_head` is always reconstructed from GitHub and may move after a recorded reconciliation observation.
- `administrative_descendant_sha` is a descendant whose diff is limited to claim/state/handover/assurance administration and does not modify product/runtime/security/legal semantics.

The assurance verdict binds only to the exact `release_candidate_sha` it reviewed.

Any functional repair, semantic architecture change, rebase/cherry-pick that changes candidate content, dependency reconciliation affecting authority/contracts, generated client/release output, or security/configuration mutation creates a new implementation/release candidate identity. Required substantive tests and assurance must run again on the surviving candidate as dictated by scope.

### Strictly administrative descendant rule

A later commit may record handover, work-claim or machine-state metadata for an already-tested implementation candidate. In that narrow case assurance may reuse substantive evidence from `implementation_candidate_sha` **only if** it independently verifies all of the following:

1. the implementation candidate is an ancestor of the release candidate;
2. the intervening diff is strictly administrative/governance metadata and contains no product/runtime/security/legal/configuration/generated-client-output change;
3. the project governance structural gate passes on the exact `release_candidate_sha`;
4. any inherited repository regression workflows configured for that release candidate pass as required;
5. no dependency/target drift invalidates the implementation evidence;
6. candidate identity and lineage are explicit in project state/work claim/handover records.

If any condition is uncertain, the result is `INDETERMINATE` until fresh exact-head evidence is produced. Administrative classification may not be used to smuggle a semantic change past exact-head assurance.

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
9. **Governance lifecycle** — `PROJECT_STATE`, roadmap/workpackage/work claim/handover/current-state records agree with live GitHub and freshness rules.
10. **Candidate lineage** — implementation/release/live/admin identities are unambiguous and evidence is bound to the correct SHA.
11. **Post-action confirmation** — merge/deploy/data migration success is separately confirmed on the target state.

## Verdict semantics

### PASS

All required acceptance conditions are evidenced for the exact release candidate and no material unresolved contradiction remains. When prior substantive evidence is reused under the strictly administrative descendant rule, the PASS must identify both the implementation candidate and release candidate.

### FAIL

A required acceptance/security/legal/privacy/governance condition is demonstrably violated.

### INDETERMINATE

Evidence is insufficient, unavailable, contradictory, stale or not correctly tied to candidate identity. Missing evidence is never inferred as success.

## Implementation/assurance separation

Implementation may repair after `FAIL` or `INDETERMINATE`, but assurance may not silently make the repair itself and then certify its own modification.

A semantic/product repair is a new implementation candidate and returns through the required assurance path. An assurance-only administrative record may be added only after the verdict and must not alter the certified product semantics.

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
- implementation and release candidate identities are explicit;
- exact-head/substantive evidence is correctly bound and available;
- required release-candidate structural/regression evidence is available;
- required assurance verdict is recorded;
- work claim is terminal or validly transferred;
- handover/disposition is complete where required;
- `control/PROJECT_STATE.json`, current-state/roadmap/changelog/decision records are reconciled;
- production action and post-action confirmation are distinct and complete where applicable.
