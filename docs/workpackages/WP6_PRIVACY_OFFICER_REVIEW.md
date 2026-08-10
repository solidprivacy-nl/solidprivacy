# WP6 — Privacy Officer Review Package + Report/Reinsert Boundary

Status: implementation slice

Base: WP5 exact head `3a7f7fd0fe225146c5f1c1d1f2bc637948d5b1d4`

## Objective

Turn a traceability-validated DPIA draft into a human-accountable reviewed package. Human review is not represented by a generic approval flag: the reviewer acts on material structured objects, resolves open questions/assumptions, makes the residual-risk and prior-consultation disposition, and signs a hash-bound snapshot.

## Review request

The runtime freezes the complete DPIA analysis request, validated draft and governed legal-context bundle. SHA-256 hashes cover the analysis request, evidence pack, legal context and analysis. Any mutation after review-request creation invalidates the snapshot.

Required review targets are generated deterministically:

- every human-unreviewed fact used by the draft;
- every legal claim;
- every candidate risk;
- every candidate measure;
- every generated section.

## Human decisions

The reviewer is structurally required to be a human actor and uses a stable reviewer identifier plus reviewer role. Supported item decisions are `accept`, `reject`, `change` and `request_evidence`. Change/reject/request-evidence actions require rationale; section changes require replacement text.

Supplemental review evidence and reviewer-authored content are covered by a separate review-input privacy context. That context must state scrubbed input, no Scrub Key and no direct identifiers; raw personal/special-category review input is not accepted by the WP6 package contract.

## Finalisation gate

An `approve` disposition cannot become a final reviewed package when required item decisions are missing, a target is rejected, evidence is requested, open questions/assumptions remain unresolved, residual risk is unknown, prior consultation needs legal review, DPO/FG status is unknown, or high residual risk is paired with `not_required` prior consultation.

High residual risk with a human `required` prior-consultation disposition produces `approved_pending_prior_consultation`, not ordinary approval. The generated report remains a reviewed DPIA artefact; that status is not permission to start/continue processing before the consultation dependency is resolved.

## DPO/FG status

WP5 carries GDPR Article 35(2) as governed legal context. WP6 therefore requires the reviewer to resolve whether a DPO/FG is designated. A designated-and-consulted state requires advice summary and supporting evidence. A not-designated state also requires evidence. Unknown status blocks approval.

## Report and Scrub boundary

Only approved statuses receive a deterministic scrubbed Markdown report and local reinsertion handoff. The handoff contains no Scrub Key, no replacement mapping and no direct identifiers. It only points to the scrubbed reviewed report and declares that reinsertion must happen locally through the controlled Scrub process.

Source and evidence appendices are derived from structured references, not free-text citations. Evidence excerpts are not copied into the appendix by default; identifiers/source/locator metadata are sufficient for traceability and minimise data exposure.

## Minimal immutable review record

WP6 deliberately pulls a minimal audit primitive forward from WP7 because accountable sign-off requires it. The audit record freezes hashes of the review request, analysis request, evidence pack, legal context, AI analysis and human decision set, together with reviewer ID/role, signature timestamp and runtime version. The audit record itself is hashed.

WP7 still owns general workflow/run event sourcing, replayability and cross-workflow audit infrastructure.

## Acceptance criteria

- all review schemas meta-validate;
- review request freezes material inputs and deterministic required targets;
- snapshot tampering fails;
- unknown/duplicate targets and evidence fail;
- approve with missing decisions or unresolved questions becomes `needs_revision`;
- request-evidence/reject actions cannot produce a final report;
- high residual risk cannot skip prior-consultation review;
- high residual risk + required consultation produces pending-consultation status;
- unknown DPO/FG status blocks approval;
- approved review produces source/evidence appendices, scrubbed report and safe local reinsert handoff;
- audit record verifies and tampering fails;
- inherited WP1–WP5 gates remain green on exact head.

## Non-goals

- no electronic-signature/QES implementation;
- no Scrub Key or reinsertion mapping transport;
- no claim that structural `contains_direct_identifiers=false` replaces human/privacy-quality review of free text;
- no generalized audit event store yet;
- no PDF/DOCX presentation layer yet;
- no processing authorization when prior consultation remains pending.

## Next

After the complete DPIA vertical slice is proven on a representative synthetic corpus, WP7 should extract the reusable workflow/run/audit substrate before expanding to RoPA.
