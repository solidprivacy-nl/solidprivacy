# MISSION SPP R3 GAP-40 — evidence provenance and review responsibility

## Mission binding

- Mission: `SOLID_PRIVACY_PLATFORM`
- Revision: `2026-09-02-r3`
- Gap: `SPP-GAP-40`
- Repository: `solidprivacy-nl/solidprivacy`
- Authoritative baseline: `main@49a9222227b423ef563180cd3b3fbdcbadd71b6a`

## Outcome

GAP-40 extends the already-integrated GAP-30 workflow through the existing JSON contracts and native DPIA validation path. It does not add another evidence store, review framework, workflow engine, queue, scheduler, state plane or orchestration service.

The executable rule is simple: a material professional output may become final only when an attributable human review is bound to the exact reviewed artifact/version and exact reviewable content, including its current evidence and source lineage.

## Deterministic review responsibility

`contracts/human_review.schema.json` remains the single human-review contract. Pending review remains representable. An `approved` or `approved_with_changes` review must now identify:

- `reviewer_id` and `reviewer_role`;
- `reviewer_actor_type=HUMAN`;
- `reviewed_at` and rationale;
- exact `reviewed_artifact_id` and `reviewed_artifact_version`;
- deterministic `reviewed_content_sha256`;
- all bound `evidence_ids` and `source_reference_ids`;
- `decision_ref` for the professional approval decision.

A review marked not required cannot satisfy a required professional review. `approved_with_changes` remains a governed review state, but it is not a final approval: the work must return through professional review and reach `approved` before the DPIA can become `final`.

## Deterministic provenance

The existing evidence and source-reference contracts remain authoritative. The DPIA validator resolves the current evidence identities and source identities already present in the canonical assessment and requires an approved review to bind those exact sets. Missing, invented or stale evidence/source references therefore fail closed instead of being silently accepted.

The review-content fingerprint is SHA-256 over canonical JSON for the reviewed DPIA content. `human_review` and lifecycle `status` are excluded from the digest so the governed review record can be written and an approved assessment can transition to `final` without changing the reviewed substance. Artifact version, methodology, processing activities, legal context, risks, measures, conclusions, evidence, claims and source versions remain inside the digest.

## Stale-approval prevention

`src/solidprivacy/runtime/schema_validation.py` recomputes the current review-content fingerprint during canonical DPIA validation. An approval whose recorded fingerprint no longer matches the current professional content fails closed. The same validation requires the reviewed artifact id/version to match the current artifact.

Accordingly a material change after approval cannot inherit an earlier approval merely because the old review object remains present.

## Human professional gate

A canonical DPIA with lifecycle `status=final` requires:

1. `human_review.required=true`;
2. review status exactly `approved`;
3. explicit human reviewer identity/responsibility;
4. exact artifact/version/content binding;
5. exact current evidence/source provenance binding;
6. an attributable professional `decision_ref`.

`approved_with_changes` cannot satisfy the final gate; outstanding changes must pass back through the canonical GAP-30 professional-review path before final approval.

AI preparation remains proposal-only under GAP-30. Nothing in this candidate authorizes an AI actor to create the final professional approval.

## Verification

Focused tests in `tests/test_review_provenance.py` prove that:

- existing pending-review fixtures remain valid;
- a final DPIA without approved human review fails closed;
- a final DPIA with `approved_with_changes` fails closed until review status reaches `approved`;
- a correctly bound approved review validates;
- material content changes invalidate prior approval;
- missing current source provenance fails closed;
- missing current evidence provenance fails closed;
- non-human approval and stale artifact-version binding fail closed.

The existing `WP2 executable privacy gates` workflow already runs the full test suite and canonical DPIA fixture validation for changes under `contracts/**`, `src/**`, `tests/**` and `evals/**`; no second CI path is introduced.

## Explicit non-authority

This candidate introduces no real-client data processing, production deployment, client delivery, autonomous final legal/privacy/compliance/risk decision, release authority, or standing integration authority. `SPP-GAP-50` remains outside this candidate and dependent on governed completion of GAP-40.

## Acceptance mapping

- **Evidence provenance and review responsibility are deterministic:** exact evidence/source sets, artifact/version, decision responsibility and review-content fingerprint are machine-validated through the existing contracts/runtime path.
- **Material professional conclusions remain human-reviewed:** `final` fails closed unless the exact professional content has an attributable `HUMAN` approval with review status exactly `approved`.
