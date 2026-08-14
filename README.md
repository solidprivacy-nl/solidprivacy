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

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the architecture, source-authority model, safety model, common execution contract and intended integration with SolidPrivacy Scrub.

See [`docs/SOURCE_CATALOG.md`](docs/SOURCE_CATALOG.md) for the current donor/source landscape and how each source may be used.

## Initial production scope

The first production-oriented jurisdiction scope is **EU/EEA + Netherlands**.

The first workflow tranche is intentionally limited to:

1. DPIA / pre-scan;
2. DSAR / right of access;
3. RoPA;
4. personal-data-breach assessment.

Initial canonical references include the Dutch Government DPIA/pre-scan models, W3C DPV semantics, EDPB/AP legal guidance and an OSCAL-inspired evidence/control model.

Third-party privacy/GRC skill libraries remain donor material. Their legal assertions are not authoritative until independently verified against approved sources and covered by evaluations.
