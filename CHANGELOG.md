# Changelog

Material repository/product changes are recorded here. Durable architecture/product/governance decisions and rationale belong in `DECISION_LOG.md`.

## Unreleased

### 2026-08-11 — POaaS data plane, economics and project-governance foundation

- made the Client Data Plane an explicit architectural boundary rather than an implied future datastore;
- defined initial production preference for dedicated EU/EEA client data projects/accounts, with pooled multi-tenancy deferred until separately assured;
- defined evidence vault, canonical state store, tenant-scoped retrieval index, audit store, artifact vault and KMS/secrets boundaries;
- clarified that an AI model is an execution consumer of bounded retrieved context, not the customer dossier store or persistent cross-client memory;
- added data retention/deletion/offboarding and Scrub/reinsert trust boundaries;
- inserted Client Data Plane implementation as a prerequisite before real durable client state;
- added HMPO and supporting POaaS unit-economics instrumentation requirements to M1/M2 planning;
- adopted the canonical `market-predictions/control-plane` operating method for consequential SolidPrivacy work;
- added project-local governance bootstrap, independent release-assurance contract, workpackage index, work-claim register, current-state record, handover contract and governance manifest;
- added a static GitHub Actions governance gate to prevent obvious source-of-truth structure drift;
- expanded PR #8 from POaaS client-model documentation into the integrated POaaS architecture/data/governance foundation.

### 2026-08-11 — POaaS client operating model

- introduced organisation/engagement/persistent client state as first-class architecture;
- established incoming documents as evidence and outgoing reports as projections of governed structured state;
- introduced gap-driven client questioning and dependency/change propagation;
- added a POaaS onboarding reference vertical slice and synthetic Dutch home-care M2 acceptance milestone;
- deferred broad workflow expansion until the shared client substrate is proven.

## DPIA reference slice history

### WP6 / PR #7

- implemented item-level Privacy Officer review, human residual-risk/prior-consultation disposition, scrubbed reviewed reporting, local reinsert handoff and immutable review audit record;
- established M1 integrated chained DPIA execution as the next integration gate.

### WP5 / PR #6

- added governed legal-context resolution and structured fact/rule/claim-traceable DPIA analysis;
- prevented models from selecting their own legal authority or self-finalising residual risk.

### WP4 / PR #5

- added minimum safe model-call/data-egress policy and provider-independent fact extraction/validation;
- explicitly treated scrubbed/pseudonymised content as potentially still personal data.

### WP3 / PR #4

- added evidence/fact provenance, epistemic states, contradictions, missing information and deterministic readiness;
- corrected sequencing so evidence and model privacy boundaries precede generative DPIA drafting.

### WP2 / PR #3

- made DPIA contracts executable and added deterministic Dutch pre-scan/legal-decision gates.

### WP1 / PR #2

- added canonical reusable processing/DPIA model, Dutch Rijksmodel adapter and DPV semantic mapping.

### WP0 / PR #1

- established SolidPrivacy as a controlled privacy-operating architecture with separate semantics, jurisdiction, legal sources, methodologies, controls/evidence, workflows, contracts, evaluations and provenance.
