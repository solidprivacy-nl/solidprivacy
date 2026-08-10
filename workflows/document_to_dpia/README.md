# Workflow — Document to DPIA

Status: staged implementation.

```text
SCRUBBED / MINIMISED INPUT
  -> evidence registration
  -> model-call privacy policy gate
  -> candidate fact extraction
  -> fact provenance validator
  -> contradiction + missing-information gate
  -> deterministic readiness
  -> pre-scan / DPIA-necessity decision support
  -> canonical DPIA analysis
  -> detector findings
  -> finding validator
  -> Privacy Officer review
  -> scrubbed report
  -> controlled reinsert handoff
```

Current executable coverage: WP1 canonical processing/DPIA contracts; WP2 pre-scan/legal-decision/integrity gates; WP3 evidence/fact provenance/readiness; WP4 safe AI-call boundary, provider-independent detector interface, provenance validator and contradiction detection.

CI uses a deterministic fixture provider. No production external AI provider is enabled by WP4. Generative DPIA analysis remains downstream of validated evidence/facts.

Original identifiers and the Scrub Key remain outside this workflow by default. `scrubbed=true` is not proof of anonymisation. External egress of scrubbed-personal-data content requires an explicit approved model-call policy, while direct identifiers and the Scrub Key are rejected by the WP4 external boundary.

Provenance validation is not human fact acceptance. Material legal conclusions and final residual-risk acceptance require designated human review.
