# WP4 — Safe AI Execution Boundary + Fact Extraction Validator

Status: COMPLETE IMPLEMENTATION — draft PR #5; final exact-head gates required after closeout.

Base: WP3 exact head `38b3b76669141664770301622d1517030d2931b3`

## Objective

Place probabilistic fact extraction behind an executable privacy boundary and deterministic validator without allowing model output to become accepted truth or legal conclusion. CI uses a deterministic fixture provider; no production external provider is enabled.

## Privacy boundary

A model call is itself a privacy decision. `scrubbed=true` is not proof of anonymisation. The policy gate therefore precedes every provider call and separately controls `scrubbed_personal_data` egress.

The WP4 external boundary rejects unapproved policies, provider/model/task mismatch, Scrub Key, required-but-unscrubbed input, classification above policy, scrubbed-personal-data egress without explicit permission, raw personal/special-category egress without explicit permissions, direct identifiers, unknown direct-identifier status for sensitive input, unresolved provider training posture, unknown/indefinite retention, and unsafe/unresolved sensitive-content logging.

## Detector → validator

The detector may propose facts, gaps and abstentions. The deterministic validator checks request/provider/model/prompt identity, fact-ID uniqueness, registered evidence references, exact support excerpts, prohibition on detector review outcomes/user confirmation/self-validation, canonical-path boundary and support for observed/inferred facts.

`validation_status=provenance_validated` means provenance passed; it is not human fact acceptance. Confidence remains calibration metadata, not a truth/legal threshold.

Different values on the same granular canonical path remain separate and produce contradictions. Legal-basis, retention, transfer, special-category and automated-decision conflicts are initially high severity.

## Acceptance evidence

Implementation head `fe6af9a62a3ffa038bbdb5ccddc08389d6defad9` passed all pull-request workflows:

- WP4 AI boundary + extraction run `31433415045`: **success**;
- inherited WP3 evidence/fact run `31433415040`: **success**;
- inherited WP2 contract/pre-scan run `31433415052`: **success**.

The WP4 run passed full deterministic tests, permitted synthetic model-call evaluation, ready extraction, conflict extraction and inherited evidence/DPIA/pre-scan commands.

The final roadmap/closeout head must pass the same relevant exact-head gates before PR #5 is frozen for review.

## Non-goals

No production provider adapter/endorsement, no AI legal conclusion, no automatic fact acceptance, no generative DPIA prose, no claim that Scrub output is anonymous, and no organisation-wide routing/cost/secret platform yet.

## Next

WP5 begins with a deterministic legal-context bundle/resolver. Only after approved/fresh legal context is assembled may a structured DPIA analysis/drafting provider run. Real external-provider enablement remains a separate explicit decision backed by a verified model-call policy.
