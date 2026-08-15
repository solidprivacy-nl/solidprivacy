# SolidPrivacy

Controlled AI workflow library for privacy-officer and privacy-document processing tasks.

The repository is designed as a **privacy operating layer**, not a prompt collection. It separates:

- canonical privacy semantics and mappings;
- jurisdiction-specific legal overlays;
- authoritative legal-source governance;
- assessment/risk methodologies;
- controls, evidence and remediation;
- reusable document-processing and privacy-officer skills;
- auditable end-to-end workflows;
- machine-readable execution contracts;
- synthetic, regression and legal-accuracy evaluations;
- third-party provenance and licensing.

## Architecture and roadmap

See [`docs/architecture.md`](docs/architecture.md) for the architecture, source-authority model, safety model, common execution contract and intended integration with SolidPrivacy Scrub.

See [`ROADMAP.md`](ROADMAP.md) for the capability roadmap and work-package ordering.

See [`docs/SOURCE_CATALOG.md`](docs/SOURCE_CATALOG.md) for the current donor/source landscape and how each source may be used.

## Initial production scope

The first production-oriented jurisdiction scope is **EU/EEA + Netherlands**.

The first complete vertical slice is DPIA / pre-scan:

1. canonical processing/DPIA model;
2. executable pre-scan and legal-decision gates;
3. evidence/fact provenance and readiness;
4. AI fact extraction + validator;
5. AI-assisted DPIA analysis/drafting;
6. Privacy Officer review/report/reinsert handoff.

After the DPIA vertical slice is mature, workflow expansion is currently prioritised as:

1. RoPA / processing inventory;
2. personal-data-breach assessment;
3. DSAR / right of access;
4. vendor/processor assessment and transfers;
5. retention and AI-privacy assessment.

The revised ordering is intentional: RoPA creates reusable organisational processing state, while production DSAR requires broader operational capabilities such as identity, discovery, exemptions, redaction and delivery evidence.

Initial canonical references include the Dutch Government DPIA/pre-scan models, W3C DPV semantics, EDPB/AP legal guidance and an OSCAL-inspired evidence/control model.

Third-party privacy/GRC skill libraries remain donor material. Their legal assertions are not authoritative until independently verified against approved sources and covered by evaluations.
