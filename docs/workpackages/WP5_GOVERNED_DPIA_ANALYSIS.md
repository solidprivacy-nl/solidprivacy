# WP5 — Governed Legal Context + DPIA Analysis

Status: implementation slice

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

## Acceptance criteria

New schemas meta-validate; rule registry is clean against the full source registry; current EU/NL bundle is ready; non-final EDPB 2026 template is forward-only; stale required context blocks; valid fixture becomes `traceability_validated`; unreviewed facts remain explicit; wrong classifications/sources/locators fail; residual risk remains human; exact-head Actions preserve WP1–WP4 regressions.

## Next

WP6 turns the governed draft into an operational Privacy Officer review package with accept/reject/change actions, evidence/source appendix, report generation and Scrub reinsertion handoff.
