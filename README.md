# SolidPrivacy

Controlled AI workflow and client operating architecture for privacy-officer and privacy-document processing tasks.

The repository is designed as a **privacy operating layer**, not a prompt collection and not a customer dossier store. It separates:

- canonical privacy semantics and mappings;
- jurisdiction-specific legal overlays;
- authoritative legal-source governance;
- assessment/risk methodologies;
- controls, evidence and remediation;
- reusable document-processing and privacy-officer skills;
- auditable end-to-end workflows;
- machine-readable execution contracts;
- synthetic, regression and legal-accuracy evaluations;
- third-party provenance and licensing;
- project-local roadmap/workpackage/work-claim/release governance.

## Architecture and roadmap

See [`docs/architecture.md`](docs/architecture.md) for the overall architecture, source-authority model, safety model, runtime planes and intended integration with SolidPrivacy Scrub.

See [`docs/DATA_ARCHITECTURE.md`](docs/DATA_ARCHITECTURE.md) for the private Client Data Plane: where real customer evidence/state live, tenant isolation, AI retrieval, encryption/key boundaries, retention/deletion and the initial dedicated-per-client EU/EEA posture.

See [`docs/POAAS_REFERENCE_WORKFLOW.md`](docs/POAAS_REFERENCE_WORKFLOW.md) for the end-to-end Privacy Officer as a Service customer journey.

See [`docs/POAAS_OPERATING_ECONOMICS.md`](docs/POAAS_OPERATING_ECONOMICS.md) for Human Minutes per Privacy Outcome (HMPO) and the evidence required before making automation/pricing claims.

See [`ROADMAP.md`](ROADMAP.md) for authoritative capability sequencing and milestones, and [`WORKPACKAGES.md`](WORKPACKAGES.md) for the executable workpackage index.

See [`docs/SOURCE_CATALOG.md`](docs/SOURCE_CATALOG.md) for the donor/source landscape and permitted source use.

## Project governance

Consequential work follows the canonical operating method in `market-predictions/control-plane` plus the project-local [`control/PROJECT_GOVERNANCE_BOOTSTRAP.md`](control/PROJECT_GOVERNANCE_BOOTSTRAP.md).

Project-local source-of-truth files include:

- `CURRENT_STATE.md`;
- `ROADMAP.md`;
- `WORKPACKAGES.md` + `docs/workpackages/`;
- `CHANGELOG.md`;
- `DECISION_LOG.md`;
- `control/WORK_CLAIMS.json`;
- `handover/`;
- raw tests/evals/GitHub Actions evidence.

Implementation cannot certify its own consequential release candidate; independent assurance follows [`control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md`](control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md).

## Client-data boundary

Real client evidence, identifiers, production secrets, model payloads and Scrub Keys **must not** be committed to this repository, GitHub Issues/PR comments, Actions artifacts or regression fixtures.

The shared repository is the governed product/project source of truth. Real customer dossiers live in an explicitly isolated private Client Data Plane. Models receive only bounded tenant-scoped context through governed runtime retrieval; they are not the durable customer database or cross-client memory.

## Initial production scope

The first production-oriented jurisdiction scope is **EU/EEA + Netherlands**.

The first complete reference vertical slice is DPIA / pre-scan:

1. canonical processing/DPIA model;
2. executable pre-scan and legal-decision gates;
3. evidence/fact provenance and readiness;
4. AI fact extraction + validator;
5. AI-assisted governed DPIA analysis;
6. Privacy Officer review/report/reinsert boundary;
7. M1 chained end-to-end integration acceptance.

After M1, the roadmap builds shared execution/audit, the private Client Data Plane and durable client state before proving M2: a complete synthetic POaaS onboarding for a medium-sized Dutch home-care organisation.

Third-party privacy/GRC skill libraries remain donor material. Their legal assertions are not authoritative until independently verified against approved sources and covered by evaluations.
