# Workflow — Document to DPIA

Status: full governed reference slice implemented through Privacy Officer review boundary (WP6 implementation pending exact-head acceptance).

```text
SCRUBBED / MINIMISED INPUT
  -> evidence registration
  -> model-call privacy policy gate
  -> candidate fact extraction
  -> fact provenance validator
  -> contradiction + missing-information gate
  -> deterministic readiness
  -> pre-scan / DPIA-necessity decision support
  -> governed legal-context resolver
  -> structured DPIA analysis/draft
  -> traceability validator
  -> hash-bound Privacy Officer review request
  -> item-level human review + residual-risk/prior-consultation disposition
  -> minimal immutable review record
  -> scrubbed reviewed report
  -> local controlled reinsert handoff
```

Current executable coverage: WP1 canonical processing/DPIA contracts; WP2 pre-scan/legal-decision/integrity gates; WP3 evidence/fact provenance/readiness; WP4 safe AI-call boundary and detector/validator; WP5 governed legal context and source/fact-traceable analysis; WP6 object-level human review, snapshot/audit hashes and scrubbed report/reinsert boundary.

CI uses deterministic fixture providers and synthetic scrubbed review evidence. No production external AI provider is enabled. The model never selects legal authority or finalises material human decisions.

`Scrubbed` is not equivalent to anonymous. AI and human-review input privacy contexts remain explicit. The Scrub Key and direct identifiers stay outside cloud-side review packages. The final handoff contains no key or replacement map and only instructs the local Scrub process to perform controlled reinsertion.

A reviewed DPIA with `approved_pending_prior_consultation` is a reviewed assessment, **not** authorization to proceed before the required consultation dependency is resolved.
