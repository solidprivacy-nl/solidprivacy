# SolidPrivacy AI Workflow Architecture

## Purpose

This repository is the controlled AI workflow and privacy-officer automation layer for SolidPrivacy. It is intentionally **not** a dump of third-party prompts, legal text or GRC applications.

The architecture separates legal authority, privacy semantics, assessment methodologies, execution logic, controls/evidence and evaluation so each can evolve independently and remain auditable.

## Architecture layers

```text
solidprivacy/
├── vocabularies/              # canonical privacy concepts and semantic mappings
├── jurisdictions/             # EU/NL first: jurisdiction-specific legal overlays
├── legal_sources/             # approved source registry and freshness/verification policy
├── methodologies/             # DPIA/risk/assessment methods independent of agent prompts
├── control_models/            # controls, implementation, evidence, findings, remediation
├── evidence_collectors/       # bounded tools that produce reproducible evidence
├── mappings/                  # adapters between external models and canonical concepts
├── frameworks/                # GDPR, ISO 27701, EU AI Act knowledge packages
├── skills/                    # reusable atomic AI tasks
├── workflows/                 # end-to-end privacy-officer processes
├── contracts/                 # machine-readable execution interfaces
├── evals/                     # synthetic, regression and legal-accuracy evaluations
├── provenance/                # upstream source/license/adaptation history
└── docs/
```

## Layer responsibilities

### 1. Vocabularies

The canonical semantic layer answers: **what is this thing?**

SolidPrivacy should align privacy concepts with the W3C Data Privacy Vocabulary (DPV) where practical rather than inventing incompatible terminology. Examples include personal data, purpose, processing, controller, processor, data subject, recipient, legal basis, risk, technical measure and organisational measure.

DPV is a semantic reference, not legal authority. Local SolidPrivacy identifiers may be retained where product needs require them, with explicit mappings.

### 2. Jurisdictions and legal sources

The jurisdiction layer answers: **which law, regulator or official guidance applies here?**

EU and Netherlands are the initial production jurisdictions. Other jurisdictions may be added only as explicit overlays. UK guidance, for example, must never silently become an EU/NL rule.

Every material legal claim must reference an approved entry in `legal_sources/source_registry.yaml`, including source status and verification date.

### 3. Methodologies

The methodology layer answers: **how should this assessment be performed?**

Examples:

- Dutch Government DPIA model / pre-scan;
- EDPB DPIA template or meta-template;
- CNIL PIA methodology;
- NIST Privacy Risk Assessment Methodology (PRAM).

Methodologies may contain regulator or government guidance, but their procedural structure is kept separate from binding legal requirements.

### 4. Control model

The control layer answers: **what measure should exist, is it implemented, what evidence supports that, and what remains unresolved?**

The design is OSCAL-inspired rather than a wholesale OSCAL implementation. SolidPrivacy should support at least:

```text
control
implementation
assessment
finding
evidence
remediation
approval
```

This enables privacy recommendations to become trackable work instead of disappearing into prose reports.

### 5. Evidence collectors

Evidence collectors produce bounded, reproducible observations. They do not make final legal decisions.

Potential examples include website tracker/cookie collection, document metadata inspection, repository privacy review and structured questionnaire ingestion. Collectors must state their scope and limitations and should prefer local processing where sensitive data is involved.

### 6. Skills

A skill is an atomic AI capability such as:

- classify a privacy document;
- extract processing facts;
- map facts to canonical concepts;
- identify missing DPIA information;
- compare a processor agreement to an approved requirement set;
- draft a finding from validated facts and legal sources;
- validate an AI output against evidence and contracts.

A skill must not become its own hidden legal knowledge base.

### 7. Workflows

A workflow orchestrates skills, methodologies, sources, evidence and review gates.

Initial production priority:

1. DPIA / pre-scan;
2. DSAR / right of access;
3. RoPA;
4. personal-data-breach assessment.

Later candidates include retention, vendor/processor assessment, international transfers, AI privacy assessments and DPO annual reporting.

## Canonical execution model

```text
INPUT
  -> classify / extract facts
  -> normalize to canonical privacy concepts
  -> select jurisdiction
  -> select methodology
  -> resolve approved legal sources
  -> execute assessment steps
  -> collect / link evidence
  -> detector findings
  -> validator / suppression / contradiction checks
  -> human review gate where required
  -> structured output / report / remediation
```

The detector/validator split is intentional. Candidate findings should be generated broadly, then challenged against evidence, transformations, context, source authority and false-positive suppression rules before they become reportable findings.

## Common execution contract

Every production-oriented skill or workflow should emit a normalized result containing at least:

```yaml
status: completed | blocked | needs_review
facts: []
findings: []
legal_basis: []
evidence: []
assumptions: []
missing_information: []
confidence: 0.0
requires_human_review: true
source_versions: []
```

JSON Schemas in `contracts/` are the machine-readable source of truth.

## Legal-claim classification

Every compliance statement must be classified as one of:

- `LAW_REQUIRED` — directly required by binding law/regulation;
- `REGULATOR_GUIDANCE` — non-binding regulator or supervisory-authority guidance;
- `ORGANISATION_POLICY` — rule chosen by the organisation;
- `BEST_PRACTICE` — recommended practice not itself legally mandatory;
- `ASSUMPTION` — unresolved premise used for analysis.

A workflow must not silently promote guidance, policy, best practice or assumptions into legal requirements.

## Source authority hierarchy

For EU/NL work, prefer sources in this order when resolving a legal proposition:

1. binding EU/NL law and official consolidated legal text;
2. CJEU or other binding case law where applicable;
3. EDPB guidance and decisions;
4. Autoriteit Persoonsgegevens guidance for NL application;
5. official Dutch government assessment models and explanatory material;
6. other EU supervisory-authority guidance where useful;
7. recognised standards and methodologies;
8. third-party professional material;
9. upstream AI skill/prompt repositories.

Lower-tier material may inform workflow design but must not override higher-tier authority.

## Source lifecycle and freshness

Each source entry has a lifecycle state such as `authoritative`, `authoritative_guidance`, `consultation_draft`, `official_methodology`, `standard_reference`, `engineering_reference` or `candidate_raw_material`.

Time-sensitive sources must have `last_verified` and `review_due` metadata. Draft/consultation documents may be used for forward-compatible design but cannot be presented as final legal requirements.

## Human review

Privacy workflows are decision-support systems. Human review is mandatory for high-impact conclusions, including:

- final DPIA residual-risk acceptance;
- refusal, restriction or exemption in a data-subject request;
- breach-notification decisions;
- international-transfer conclusions;
- conclusions materially affecting data-subject rights;
- unresolved conflicts between authoritative sources;
- low-confidence or incomplete outputs.

## Integration with SolidPrivacy Scrub

The intended privacy-preserving flow is:

```text
ORIGINAL DOCUMENT
  -> SolidPrivacy Scrub
       local detection
       human review
       local Scrub Key
  -> SCRUBBED DOCUMENT
  -> SolidPrivacy AI Workflow
       facts / DPIA / DSAR / RoPA / vendor / breach / other analysis
  -> SCRUBBED AI RESULT
  -> controlled Reinsert
  -> Export / Audit
```

The Scrub Key and original identifiers remain outside the AI workflow unless a separately approved use case explicitly requires otherwise. Cloud processing is never implied merely because a workflow exists.

## Third-party ingestion policy

Third-party privacy/GRC skill repositories and applications are donor material, not legal authority.

Before upstream content becomes SolidPrivacy-native:

1. record repository/source, path, version/commit and license in provenance;
2. identify whether the donor contributes semantics, methodology, workflow, engineering, templates or legal assertions;
3. separate reusable process logic from jurisdiction-specific assertions;
4. verify material legal assertions against approved sources;
5. map concepts to canonical vocabulary;
6. adapt inputs/outputs to `contracts/`;
7. add evidence and human-review gates;
8. add positive, negative and near-miss evaluations;
9. preserve required attribution and modification notices.

## Initial donor strategy

The initial architecture recognises four distinct donor classes:

- **semantic:** W3C DPV;
- **official methodology:** Dutch Government DPIA/pre-scan model, EDPB templates, CNIL PIA;
- **control/evidence engineering:** NIST OSCAL/PRAM and EDPS evidence tooling;
- **agent engineering:** selected privacy/GRC skill repositories, Meta SecPriv and open-source GRC systems such as Probo.

These classes must remain distinct in code and provenance.

## Non-goals

This repository is not intended to:

- replace a qualified privacy professional or DPO;
- treat third-party prompts as authoritative law;
- copy complete external GRC products;
- embed real personal data in tests;
- create uncontrolled autonomous legal decisions;
- duplicate the Scrub anonymisation engine;
- introduce cloud document processing by default.
