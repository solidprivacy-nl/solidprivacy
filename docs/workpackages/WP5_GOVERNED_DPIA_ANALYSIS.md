# WP5 — Governed Legal Context + DPIA Analysis

Status: COMPLETE IMPLEMENTATION — draft PR #6; final closeout head must preserve exact-head gates.

Base: WP4 exact head `bc71c84e7055f3b1c8b8bb6d445eda857a035375`

## Objective

Allow structured AI-assisted DPIA analysis only after **both** factual provenance and legal authority have passed deterministic gates. The model must not select law or regulatory guidance from its own memory; a legal-context request is resolved against the governed source registry plus curated source-bound rules before provider invocation.

## Legal context gate

`legal_sources/rules/dpia_core.yaml` contains concise paraphrased DPIA rules linked to approved source IDs and exact locators. `legal_context.py` verifies rule/source compatibility, jurisdiction and freshness. Required stale/missing/inapplicable rules block the bundle. Official methodology and non-final consultation material can be included only in explicit context modes and cannot back a legal claim. The 2026 EDPB DPIA template is intentionally `forward_context_only` while finalisation is pending.

## Analysis boundary

The request embeds a validated evidence pack and a legal-context **request**, not a caller-supplied legal bundle. The runtime recomputes the bundle from governed repository data. The validator checks provider/model/prompt identity, fact provenance, unresolved-fact visibility, legal-rule membership, legal classification/source/authority/jurisdiction/locator binding, risk/measure references and the mandatory human residual-risk gate.

An unreviewed fact can support draft analysis, but it must remain listed as an unresolved fact in every section that uses it. Provenance validation is not human fact acceptance.

## Safety rules

Blocked evidence or stale legal context prevents provider invocation. Non-final/context-only sources cannot support claims. Guidance cannot masquerade as `LAW_REQUIRED`. Invented references fail. The provider cannot self-validate analysis or finalise residual risk. External model calls still pass the WP4 egress policy.

## Acceptance evidence

Implementation head `0e3e82a2f036d6cc5c9f4d50d82f11c12e5c2e5e` passed all relevant pull-request workflows:

- WP5 governed DPIA analysis run `31435239155`: **success**;
- inherited WP4 AI boundary/fact extraction run `31435239139`: **success**;
- inherited WP3 evidence/fact provenance run `31435239144`: **success**;
- inherited WP2 contract/pre-scan run `31435239264`: **success**.

The WP5 job passed the full deterministic suite, curated-rule integrity, current legal-context resolution, deterministic governed DPIA analysis and all inherited runtime smoke gates.

The final roadmap/closeout head must pass the same relevant exact-head gates before PR #6 is frozen for review.

## Acceptance criteria

New schemas meta-validate; rule registry is clean against the full source registry; current EU/NL bundle is ready; non-final EDPB 2026 template is forward-only; stale required context blocks; valid fixture becomes `traceability_validated`; unreviewed facts remain explicit; wrong classifications/sources/locators fail; residual risk remains human; exact-head Actions preserve WP1–WP4 regressions.

## Next

WP6 turns the governed draft into an operational Privacy Officer review package. A minimal immutable review record is deliberately included in WP6 because human accountability requires the reviewed draft/evidence/source/model/policy versions and decision timestamps to be frozen at sign-off. WP7 later generalises audit/event infrastructure across workflows.
