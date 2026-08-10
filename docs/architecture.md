# SolidPrivacy AI Workflow Architecture

## Purpose

This repository is the controlled AI workflow and privacy-officer automation layer for SolidPrivacy. It is intentionally **not** a dump of third-party prompts, legal text or GRC applications.

The architecture separates legal authority, privacy semantics, assessment methodologies, execution logic, controls/evidence and evaluation so each can evolve independently and remain auditable.

For Privacy Officer as a Service, the architecture additionally distinguishes the **shared governed capability layer** from **isolated durable client operating state**. The repository defines how work is performed; it must not become a store for real customer evidence, direct identifiers or Scrub Keys.

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

## Operating planes

The repository folders above are the implementation structure. At runtime, SolidPrivacy should reason in four operating planes:

```text
1. GLOBAL GOVERNED CAPABILITY PLANE
   legal sources / jurisdictions / methodologies / semantics / controls / workflow definitions / evals

2. EXECUTION + ASSURANCE PLANE
   workflow runs / stage state / model-call policy / validators / human review / immutable audit

3. ISOLATED CLIENT OPERATING PLANE
   organisation / engagement / evidence / accepted privacy state / assessments / findings / actions

4. DELIVERY + CONTINUOUS-SERVICE PLANE
   targeted client questions / PO work queue / deliverables / management reporting / change intake
```

The same global capability can be applied to many clients, but client state and evidence must remain segregated. A workflow run consumes a bounded snapshot of client state and may propose reviewed changes back to that state.

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

The first complete reference vertical slice is DPIA/pre-scan. After its integrated acceptance, the roadmap first extracts shared execution/client-state primitives and then builds the POaaS onboarding slice around persistent processing inventory/RoPA state. Subsequent workflows include breach, vendor/Article 28, DSAR, transfers, retention and AI privacy assessments.

A workflow is **not** the durable customer record. It reads a versioned client-state snapshot, produces evidence-backed results, and may propose changes/findings/actions that pass review before becoming durable state.

## Client operating model

POaaS requires concepts that are broader than one assessment:

```text
organisation
  -> engagement
      -> service commitments / deliverables
      -> evidence requirements
      -> workflow runs

organisation
  -> evidence
  -> accepted privacy facts
  -> systems
  -> processing activities
  -> processors / recipients
  -> measures
  -> assessments
  -> findings
  -> actions
  -> deliverable history
```

Important rules:

1. Client/tenant identity and access are explicit; no cross-client state is inferred from prompts.
2. Engagement scope says what SolidPrivacy has promised to do; it is separate from the organisation's underlying privacy state.
3. Accepted organisation facts survive individual workflow runs and can be reused across RoPA, DPIA, vendor, breach, DSAR and retention work.
4. Proposed AI facts never become durable accepted client state merely because provenance validation succeeded.
5. Real client data belongs in an appropriately controlled client data store, not in this shared repository or regression fixtures.

See `docs/POAAS_REFERENCE_WORKFLOW.md` for the reference lifecycle.

## Documents, evidence and projections

Incoming documents are evidence sources. Outgoing documents are controlled projections.

```text
incoming evidence
   -> extracted/proposed facts
   -> provenance / contradiction / gap validation
   -> human acceptance where required
   -> persistent structured client state
   -> workflow assessments/findings/actions
   -> client-grade projections (RoPA / DPIA / management report / action plan)
```

This avoids a common consultancy failure mode in which the RoPA, DPIA, processor register and management report become separate manually maintained truths.

Every material projection should eventually record the state/evidence/source/review versions from which it was produced.

## State lifecycle and change propagation

Durable client facts need lifecycle states such as:
- proposed;
- provenance-valid;
- human-accepted;
- disputed;
- superseded;
- stale/reassessment-required.

A change to one object should create impact events for dependent objects instead of silently rewriting approved conclusions.

Example:

```text
processor changed
  -> processing activity affected
  -> RoPA projection stale
  -> Article 28 assessment affected
  -> transfer assessment possibly affected
  -> DPIA facts possibly affected
  -> review/work items created
```

Legal-source changes can create the same type of impact from the governed capability plane toward affected assessments.

## Canonical execution model

```text
CLIENT/WORKFLOW INPUT SNAPSHOT
  -> classify / register evidence
  -> extract candidate facts
  -> normalize to canonical privacy concepts
  -> provenance / contradiction / missing-information validation
  -> select jurisdiction
  -> select methodology
  -> resolve approved legal sources
  -> execute deterministic assessment steps
  -> detector findings
  -> validator / suppression / traceability checks
  -> human review gate where required
  -> structured result / proposed state changes / remediation
  -> reviewed client-state update
  -> report/deliverable projection
  -> immutable audit linkage
```

The detector/validator split is intentional. Candidate findings should be generated broadly, then challenged against evidence, transformations, context, source authority and false-positive suppression rules before they become reportable findings.

## Gap-driven questioning

Client onboarding should not remain a static questionnaire process.

Initial service/evidence requirements may be standardized, but after evidence ingestion the system should derive a targeted queue from:
- missing stage-critical information;
- contradictions;
- stale evidence;
- unclear scope;
- decisions only the client/Privacy Officer can confirm.

Answers become evidence or user-confirmed facts with provenance. A model-generated question never by itself establishes a legal requirement.

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

Generalized execution will additionally require run/organisation/engagement linkage, state snapshots/hashes, review decisions and proposed state changes. JSON Schemas in `contracts/` are the machine-readable source of truth.

## Legal-claim classification

Every compliance statement must be classified as one of:
- `LAW_REQUIRED` — directly required by binding law/regulation;
- `REGULATOR_GUIDANCE` — non-binding regulator or supervisory-authority guidance;
- `ORGANISATION_POLICY` — rule chosen by the organisation;
- `BEST_PRACTICE` — recommended practice not itself legally mandatory;
- `ASSUMPTION` — unresolved premise used for analysis.

A workflow must not silently promote guidance, policy, best practice or assumptions into legal requirements.

Sector profiles such as healthcare/home care may configure expected evidence, terminology or control baselines but do not create legal authority.

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
- low-confidence or incomplete outputs;
- material proposed changes to accepted client state when accountability requires explicit approval.

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

The client operating layer may retain a reference to evidence lifecycle and workflow outputs, but cloud-side workflow packages must not acquire the local Scrub Key/replacement mapping.

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
- introduce cloud document processing by default;
- store real client evidence or become a multi-tenant customer database itself;
- make a large GRC UI the prerequisite for proving workflow and client-state contracts.
