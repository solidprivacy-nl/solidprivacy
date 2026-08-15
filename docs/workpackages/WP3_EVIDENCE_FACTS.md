# WP3 — DPIA Evidence and Fact Provenance Layer

Status: COMPLETE — draft PR #4; exact-head gates required on final closeout head.

Base: WP2 exact head `017902f3116fac914020a449db3f628df90b485b`

## Objective

Insert the missing trust boundary between scrubbed source material and AI-assisted DPIA reasoning.

WP2 can already answer deterministic pre-scan questions and validate a completed canonical DPIA. It does **not** yet control how facts enter that DPIA. WP3 therefore makes evidence, candidate facts, epistemic status, contradictions, missing information and readiness executable objects.

This work package deliberately precedes generative DPIA drafting.

## Threat model

Without this layer an LLM could invent a purpose, party, location or retention period; merge contradictory documents into a false single fact; treat an assumption as observed evidence; silently omit missing information; or draft a legally material conclusion from an unsupported premise.

WP3 does not attempt to make LLM extraction infallible. It makes unsupported or unresolved states visible and machine-testable.

## Contracts

### `privacy_fact.schema.json`

Each candidate fact records a stable fact ID, fact type, target canonical path, JSON value, epistemic status, confidence metadata, evidence references, basis summary, review status and sensitivity classification.

Observed, inferred and user-confirmed facts require at least one evidence reference. Inferred facts also require a concise basis summary. Confidence is retained for future calibration/evaluation; it is deliberately **not** used as an automatic truth or legal-validity gate.

### `evidence_pack.schema.json`

A case-level pack contains evidence, candidate facts, contradictions, missing-information items, deterministic readiness claim, human-review state and source/runtime versions.

## Deterministic integrity rules

The runtime rejects duplicate IDs, unknown evidence/fact references, resolved items without resolution, assumptions represented as accepted established facts and readiness claims inconsistent with deterministic blockers.

## Readiness semantics

Two stages are initially supported: `analysis` and `finalisation`.

High/critical unresolved contradictions and high/critical stage-blocking missing information block progression. Normal unresolved uncertainty and explicitly accepted uncertainty remain review signals. Finalisation additionally blocks on unresolved assumptions or rejected facts.

Readiness is not a legal conclusion. It answers only whether the current evidence state is mature enough for the next processing stage.

## AI boundary

WP3 defines the future `extract_privacy_facts` skill interface but does not choose an LLM provider. A future extractor may propose facts; it may not invent evidence locators, verify AP-list conditions, decide final DPIA necessity, accept high residual risk, or suppress contradictions/missing information.

The validator and human reviewer remain separate roles.

## Acceptance evidence

Initial WP3 head `e38aeeb85d0e4d80987b8c98c5e5fd3e974e997f` passed both pull-request workflows:

- WP3 evidence/fact gate run `31432376592`: success;
- inherited WP2 contract/pre-scan run `31432377577`: success.

The final roadmap closeout head must pass the same relevant exact-head gates before PR #4 is considered frozen for review.

## Acceptance criteria

- schemas pass JSON Schema 2020-12 meta-validation;
- ready fixture passes contract + integrity validation and derives `ready`;
- blocked fixture passes contract + integrity validation and derives `blocked`;
- unsupported evidence references fail;
- duplicate IDs fail;
- unresolved high contradiction blocks analysis;
- critical missing information blocks analysis;
- assumption blocks finalisation;
- false readiness claim fails integrity;
- CLI validates packs and reports derived readiness;
- WP1 DPIA + WP2 pre-scan regressions remain green;
- GitHub Actions green on exact PR head.

## Non-goals

- no LLM API integration;
- no free-form DPIA generation;
- no legal conclusion from extracted fact text;
- no raw personal-data corpus;
- no automatic conflict resolution;
- no model-specific prompt optimisation.

## Next

WP4 implements the minimum safe AI execution boundary plus AI-assisted fact extraction and a separate validator. WP5, not WP4, introduces DPIA analysis/drafting.
