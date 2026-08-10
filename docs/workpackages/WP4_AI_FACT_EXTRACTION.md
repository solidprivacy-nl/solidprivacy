# WP4 — Safe AI Execution Boundary + Fact Extraction Validator

Status: implementation slice

Base: WP3 exact head `38b3b76669141664770301622d1517030d2931b3`

## Objective

Prove that SolidPrivacy can place a probabilistic fact extractor behind an executable privacy boundary and deterministic validator without allowing model output to become accepted truth or legal conclusion. CI intentionally uses a deterministic fixture provider; no production external provider is enabled.

## Why the model boundary is part of WP4

A model call itself is a privacy decision: what content leaves the controlled environment, to which provider/model, under what training/retention/logging posture and with what Scrub state. The minimum policy gate must therefore precede every provider call. A broader multi-provider gateway remains later hardening.

## Contracts

- `model_call_policy.schema.json` — approved provider/model/task and data-handling boundary. `scrubbed_personal_data` has an explicit egress flag because scrubbed/pseudonymised content is not automatically anonymous.
- `fact_extraction_request.schema.json` — content, evidence, jurisdiction, provider/model/prompt and explicit privacy context.
- `fact_extraction_result.schema.json` — detector facts, missing information, abstentions, model metadata and evidence support proofs.

## External model-call gates

The runtime rejects unapproved policies; task/provider/model mismatch; any Scrub Key; required-but-unscrubbed input; classification above policy; scrubbed-personal-data egress without explicit permission; raw personal/special-category egress without explicit permissions; direct identifiers; unknown direct-identifier status for sensitive input; unresolved provider training posture; unknown/indefinite retention; and unsafe/unresolved sensitive-content logging.

## Detector → validator

The detector is probabilistic/high-recall. The deterministic validator checks request/provider/model/prompt identity, unique fact IDs, evidence references, exact support excerpts, prohibition on detector review outcomes/user confirmation/self-validation, canonical-path boundary and support for observed/inferred facts.

`validation_status=provenance_validated` means provenance checks passed, not that a human accepted the fact. Model confidence remains calibration metadata, never an automatic truth/legal threshold.

Different values on the same granular canonical path remain separate and create explicit contradictions. Legal-basis, retention, transfer, special-category and automated-decision conflicts are initially high severity.

## Acceptance

All schemas must meta-validate; synthetic safe calls require explicit policy; Scrub Key/direct identifiers/unsafe egress/provider posture must fail; detector self-approval and invented support must fail; ready extraction remains human-review pending; conflicting retention must block analysis; CI requires no network/secrets; inherited WP1–WP3 regressions must stay green; final exact-head Actions must pass.

## Non-goals

No production provider adapter or endorsement, no AI legal conclusion, no automatic fact acceptance, no DPIA prose, no claim Scrub output is anonymous, and no organisation-wide routing/cost/secret platform yet.

## Next

WP5 should consume only validated evidence packs and approved legal sources. Before any real external provider is enabled, a real model-call policy must be populated from verified contractual/product data-handling facts and explicitly approved.
