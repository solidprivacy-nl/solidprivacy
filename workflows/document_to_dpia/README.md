# Workflow — Document to DPIA

Status: staged implementation.

## Intended pipeline

```text
SCRUBBED / MINIMISED INPUT
  -> evidence registration
  -> candidate fact extraction
  -> fact validator
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

## Current executable coverage

- WP1: canonical processing/DPIA contracts;
- WP2: pre-scan, legal-decision separation, schema/integrity gates;
- WP3: evidence/fact provenance and readiness gates.

Generative DPIA analysis is intentionally downstream of the evidence gate.

## Privacy boundary

Original identifiers and the Scrub Key remain outside this workflow by default. Evidence locators should refer to scrubbed/minimised source artefacts. If an evidence excerpt may contain personal data, `contains_personal_data` must be set accurately and the model/privacy policy must determine whether it may leave the approved environment.

## Final authority

The workflow is decision support. Material legal conclusions and final residual-risk acceptance require designated human review.
