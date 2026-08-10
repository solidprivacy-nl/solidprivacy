# Workflow — Document to DPIA

Status: governed analysis implemented through WP5.

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
  -> structured canonical DPIA analysis/draft
  -> detector findings
  -> traceability/finding validator
  -> Privacy Officer review
  -> scrubbed report
  -> controlled reinsert handoff
```

Current executable coverage: WP1 canonical processing/DPIA contracts; WP2 pre-scan/legal-decision/integrity gates; WP3 evidence/fact provenance/readiness; WP4 safe AI-call boundary, provider-independent detector interface, provenance validator and contradiction detection; WP5 curated legal rules, jurisdiction/freshness resolution and source/fact-traceable DPIA draft validation.

CI uses deterministic fixture providers. No production external AI provider is enabled by WP5. The model does not select legal authority: WP5 resolves legal context from governed source/rule registries. Non-final consultation material may be forward context but cannot support a legal claim.

Original identifiers and the Scrub Key remain outside this workflow by default. `scrubbed=true` is not proof of anonymisation. External egress of scrubbed-personal-data content requires an explicit approved model-call policy, while direct identifiers and the Scrub Key are rejected by the external boundary.

Provenance validation is not human fact acceptance. Sections using unreviewed facts must keep those fact IDs explicit. Material legal conclusions and final residual-risk acceptance require designated Privacy Officer/DPO review.
