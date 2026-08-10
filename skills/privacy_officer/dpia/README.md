# DPIA skill family

Status: governed analysis + Privacy Officer review boundary through WP6.

## Execution chain

```text
validated evidence/facts
  -> deterministic pre-scan/legal-decision support
  -> governed legal context
  -> policy-gated structured DPIA analysis
  -> traceability validator
  -> Privacy Officer review request with frozen hashes
  -> item-level human decisions
  -> human residual-risk/prior-consultation decision
  -> scrubbed reviewed report
  -> local Scrub reinsertion handoff
```

DPIA analysis consumes only a valid evidence pack, a legal-context request resolved by the runtime against approved source/rule registries, and a model call passing the active privacy/egress policy. The provider never decides which source is authoritative.

The AI output remains structured, traceable and review-pending. Legal claims identify governed rule IDs and source-bound metadata. Sections identify supporting facts/rules and separately list facts whose human review is unresolved. Risks/measures are candidates. `residual_risk_status` remains `requires_human_assessment`.

WP6 converts that draft into a human-accountable package. Review decisions target facts, claims, risks, measures and sections. Open questions and assumptions must be resolved for approval. Residual risk, prior consultation and DPO/FG status are explicitly human decisions.

The review package is hash-bound to the exact analysis/evidence/legal context that was reviewed. Approved packages may generate a scrubbed Markdown report and a **local-only** reinsertion handoff. The handoff never contains the Scrub Key or replacement mappings.

The skill family must not turn guidance into law, use consultation-only material as authority, fabricate citations/fact IDs, silently accept unreviewed facts, hide open questions, let AI finalise residual risk, or treat a pending prior-consultation dependency as processing approval.
