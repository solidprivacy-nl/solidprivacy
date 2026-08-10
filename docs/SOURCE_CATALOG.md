# Source Catalog

This catalog records candidate and approved sources for SolidPrivacy privacy-officer automation. It is a design inventory, not itself legal authority. Machine-readable legal-source state lives in `legal_sources/source_registry.yaml`; third-party donor provenance lives in `provenance/upstream_manifest.yaml`.

## Selection criteria

Sources are assessed on:

- authority and jurisdiction;
- legal or methodological role;
- currency and versioning;
- machine-readability;
- licensing/reuse constraints;
- usefulness for deterministic workflow design;
- suitability for synthetic evaluation;
- privacy/security posture.

## Tier A — primary architecture sources

### Dutch Government PAR DPIA / IAMA assessment project

- Source: `https://github.com/MinBZK/par-dpia-form`
- Authority: Dutch Ministry of the Interior and Kingdom Relations ecosystem
- Role: official-methodology / machine-readable assessment donor
- License: EUPL-1.2
- Notable assets: structured YAML definitions for pre-scan, DPIA and IAMA plus terminology files and validation schemas.
- SolidPrivacy use: primary Dutch DPIA/pre-scan methodology donor and mapping target.
- Rule: reuse only with license/provenance review; do not equate every field with a binding legal requirement.

### Dutch Government DPIA information model

- Source: `https://modellen.jenvgegevens.nl/dpia/`
- Authority: Dutch Government / Ministry of Justice and Security data-model publication
- Role: conceptual and logical DPIA information model
- SolidPrivacy use: canonical object-model reference for Dutch DPIA entities and relationships.

### W3C Data Privacy Vocabulary (DPV)

- Source: `https://github.com/w3c-cg/dpv` and `https://w3id.org/dpv`
- Authority: W3C Community Group output
- Role: privacy semantic vocabulary
- SolidPrivacy use: preferred semantic mapping for personal data, purposes, processing, entities, legal bases, rights, risks, measures and technologies.
- Rule: semantic reference only; not legal authority. License/reuse terms must be verified before vendoring content.

### EDPB DPIA template 2026

- Source: EDPB public-consultation material adopted for consultation in March 2026.
- Authority: European Data Protection Board
- Role: European DPIA template/meta-template direction
- Status at catalog verification (2026-08-10): consultation material; do not treat as final binding or final guidance.
- SolidPrivacy use: forward-compatible adapter target and legal-accuracy evaluation input once finalised.

### EDPB personal-data-breach notification template 2026

- Authority: European Data Protection Board
- Role: harmonised breach-notification structure
- Status at catalog verification (2026-08-10): public-consultation cycle completed/pending finalisation; not a binding final rule.
- SolidPrivacy use: breach-output structure and future regulator-adapter target.

### EDPB Right of Access Guidelines 01/2022

- Authority: European Data Protection Board
- Role: authoritative EU supervisory guidance for Article 15/right-of-access workflows
- SolidPrivacy use: primary DSAR/right-of-access guidance source together with GDPR text.

### Autoriteit Persoonsgegevens

- Source: `https://autoriteitpersoonsgegevens.nl/`
- Authority: Dutch supervisory authority
- Role: NL regulator guidance and operational procedures
- SolidPrivacy use: Dutch overlays for breach handling, DPIA/accountability, rights and regulator interaction.

### European Commission Standard Contractual Clauses

- Source: European Commission official SCC publications
- Authority: European Commission
- Role: official contractual clauses for controller/processor and international-transfer use cases
- SolidPrivacy use: source for structured contract comparison; never rely on donor prompts instead of official clauses.

## Tier A — control, evidence and engineering references

### NIST OSCAL

- Source: `https://pages.nist.gov/OSCAL/`
- Authority: NIST
- Role: machine-readable control, implementation, assessment and remediation architecture
- SolidPrivacy use: architectural inspiration for the internal control/evidence object model; not a GDPR legal source.

### NIST Privacy Risk Assessment Methodology (PRAM)

- Source: NIST Privacy Engineering Program
- Role: privacy-risk methodology
- SolidPrivacy use: secondary risk methodology and cross-check for structured privacy-risk reasoning.

### EDPS Website Evidence Collector

- Authority: European Data Protection Supervisor
- Role: local/reproducible website privacy evidence collection
- SolidPrivacy use: evidence-collector design reference for cookies, storage and third-party requests.

### Meta SecPriv

- Source: `https://github.com/facebookresearch/secpriv-skill`
- License: MIT
- Role: agent-engineering and evaluation donor
- Notable pattern: detector/validator decomposition, explicit suppression rules, benchmark with positive and near-miss cases.
- SolidPrivacy use: evaluation architecture and finding-validation pattern, especially for repository/code privacy reviews.

### Probo

- Source: `https://github.com/getprobo/probo`
- License: MIT
- Role: open-source GRC architecture reference
- Notable concepts: DPIA/TIA, processing activities, rights requests, evidence, controls, vendors, audit trails, MCP/GraphQL automation.
- SolidPrivacy use: object-model and automation-interface reference; do not copy the whole product.

### compliance-agent-skills

- Source: `https://github.com/vaquarkhan/compliance-agent-skills`
- License: MIT
- Role: agent lifecycle/evidence/redaction engineering donor
- Notable pattern: scope -> audit -> evidence -> remediate -> report, deterministic checks, provenance/SME metadata.
- SolidPrivacy use: selected engineering patterns only.

## Tier B — regulator and methodology donors

### CNIL PIA

- Source: `https://github.com/LINCnil/pia`
- Authority: CNIL ecosystem
- License: GPL-3.0 repository
- Role: PIA methodology and implementation reference
- SolidPrivacy use: methodology/risk/UX comparison; license review required before code/content reuse.

### CNIL GDPR Developer Guide

- Source: `https://github.com/LINCnil/GDPR-Developer-Guide`
- Authority: CNIL
- Role: privacy-engineering best-practice guide
- SolidPrivacy use: privacy-by-design and engineering checklist donor. Distinguish best practice from legal requirement.

### CNIL RoPA and DPO materials

- Authority: CNIL
- Role: processing-record and DPO operational templates
- SolidPrivacy use: secondary methodology/reference for RoPA and future DPO annual-report workflows.

### AEPD Facilita RGPD / risk tools

- Authority: Spanish supervisory authority
- Role: screening, questionnaire and risk-workflow references
- SolidPrivacy use: workflow pattern donor; Spanish jurisdiction must remain explicit.

### ICO audit and privacy toolkits

- Authority: UK Information Commissioner's Office
- Role: audit/checklist methodology
- SolidPrivacy use: structural inspiration only unless a UK jurisdiction pack is explicitly active. UK rules must never silently populate EU/NL conclusions.

## Existing skill-library donors

### Privacy-Data-Protection-Skills

- Source: `https://github.com/mukul975/Privacy-Data-Protection-Skills`
- License: Apache-2.0
- Role: broad privacy task/workflow raw material
- SolidPrivacy use: selected workflow skeletons after legal deconstruction and validation.

### Claude-Skills-Governance-Risk-and-Compliance

- Source: `https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance`
- License: MIT
- Role: framework/router/evaluation raw material
- SolidPrivacy use: selected framework and eval patterns after source verification.

## Ingestion rule

No catalog entry is automatically approved for direct copying. Each future import must record:

1. exact upstream source/path and version or commit;
2. license and attribution obligations;
3. imported/adapted path;
4. conceptual role (semantic, methodology, legal, workflow, engineering, evidence);
5. legal verification state;
6. evaluation coverage;
7. human-review implications.

When the same proposition appears in multiple sources, the legal-source authority hierarchy in `docs/architecture.md` controls which source may support a legal claim.
