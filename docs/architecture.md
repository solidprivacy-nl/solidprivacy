# SolidPrivacy AI Workflow Architecture

## Purpose

This repository is the controlled AI workflow and privacy-officer automation layer for SolidPrivacy. It is intentionally **not** a dump of third-party prompts, legal text or GRC applications.

The architecture separates legal authority, privacy semantics, assessment methodologies, execution logic, controls/evidence and evaluation so each can evolve independently and remain auditable.

For Privacy Officer as a Service, the architecture additionally distinguishes the **shared governed capability layer**, the **private physical Client Data Plane**, and the **isolated durable client operating state**. The repository defines how work is performed and governed; it must not become a store for real customer evidence, direct identifiers, model payloads, credentials or Scrub Keys.

Supporting architecture documents:

- `docs/DATA_ARCHITECTURE.md` — physical/private client-data boundary, storage, tenancy, retrieval, AI access, retention and key posture;
- `docs/POAAS_REFERENCE_WORKFLOW.md` — end-to-end reference customer lifecycle;
- `docs/POAAS_OPERATING_ECONOMICS.md` — HMPO/unit-economics measurement framework;
- `control/PROJECT_GOVERNANCE_BOOTSTRAP.md` — GitHub/control-plane source-of-truth and assurance operating method.

## Repository implementation layers

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
├── control/                   # project-local governance/assurance/claim contracts
├── handover/                  # explicit claim/ownership/lineage dispositions
└── docs/
```

## Runtime operating planes

The repository folders above are implementation structure. At runtime, SolidPrivacy should reason in five operating planes:

```text
1. GLOBAL GOVERNED CAPABILITY PLANE
   legal sources / jurisdictions / methodologies / semantics / controls / workflow definitions / evals

2. EXECUTION + ASSURANCE PLANE
   workflow runs / stage state / authorization / retrieval / model-call policy / validators / human review / immutable audit

3. PRIVATE CLIENT DATA PLANE
   evidence vault / relational state store / tenant retrieval index / artifact vault / keys / backups / access logs

4. CLIENT OPERATING STATE
   organisation / engagement / accepted privacy facts / processing / processors / assessments / findings / actions

5. DELIVERY + CONTINUOUS-SERVICE PLANE
   targeted client questions / PO work queue / deliverables / management reporting / change intake / reassessment
```

The same global capability can be applied to many clients, but client data remains segregated in the private Client Data Plane. A workflow run consumes a bounded versioned snapshot of one client's state/evidence and may propose reviewed changes back to that client's state.

The physical Client Data Plane and the logical Client Operating State are deliberately separate. The storage technology can change without redefining canonical privacy concepts.

## Architecture responsibilities

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

Collector output for a real customer is stored as tenant-scoped evidence in the private Client Data Plane, never as a public repository fixture.

### 6. Skills

A skill is an atomic AI capability such as:
- classify a privacy document;
- extract processing facts;
- map facts to canonical concepts;
- identify missing DPIA information;
- compare a processor agreement to an approved requirement set;
- draft a finding from validated facts and legal sources;
- validate an AI output against evidence and contracts.

A skill must not become its own hidden legal knowledge base or hidden customer memory.

### 7. Workflows

A workflow orchestrates skills, methodologies, sources, evidence, runtime policies and review gates.

The first complete reference vertical slice is DPIA/pre-scan. After integrated M1 acceptance, the roadmap extracts shared execution/audit primitives, implements the Client Data Plane, then creates client/engagement/persistent-state primitives and the POaaS onboarding slice. Subsequent workflows include breach, vendor/Article 28, DSAR, transfers, retention and AI privacy assessments.

A workflow is **not** the durable customer record. It reads a versioned tenant-scoped snapshot, produces evidence-backed results, and may propose changes/findings/actions that pass validation/human review before becoming durable state.

## Client operating model

POaaS requires concepts broader than one assessment:

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
5. Real client data belongs in the private Client Data Plane, not in this shared repository or regression fixtures.
6. A model/provider is not a durable datastore and cannot implicitly carry state from one customer/run to another.

See `docs/POAAS_REFERENCE_WORKFLOW.md` for the reference lifecycle.

## Private Client Data Plane

The Client Data Plane is a first-class security architecture boundary, not a database implementation detail.

Its initial production responsibilities are:

```text
Evidence Vault
  original/submitted source objects + hashes + classifications + retention

Canonical Client State Store
  organisation/process/system/processor/fact/assessment/action revisions

Tenant Retrieval Index
  derived chunks/embeddings linked to exact source/version/classification

Workflow/Audit Store
  run/stage/version/policy/review/state-mutation/access evidence

Delivery Artifact Vault
  reviewed RoPA/DPIA/baseline/report/action-plan outputs + lineage

KMS / Secrets Boundary
  application/provider credentials + encryption-key scope outside repository/data content
```

### Initial isolation posture

For the first production cohort, especially healthcare clients, prefer one **dedicated EU/EEA client data project/account per customer** with separate database, object storage, retrieval and key/credential scope.

This is intentionally conservative. A later pooled multi-tenant architecture can reduce cost but is not automatically safe because rows contain `tenant_id`. Pooling requires explicit negative isolation testing across database, storage, indexes, batch jobs, telemetry, backups/restores and secrets before adoption.

### AI access boundary

AI/model providers never receive broad database credentials or unrestricted dossier access.

```text
workflow + authenticated tenant + purpose
  -> authorize
  -> retrieve tenant-scoped evidence/state
  -> minimise/scrub/classify
  -> evaluate provider/model egress policy
  -> bounded model context
  -> structured candidate result
  -> validation/human review
  -> persist approved result + audit in client data plane
```

Cross-client model/conversation memory is prohibited. If any application cache/history is persistent, it is a tenant-scoped client-data object with retention/deletion semantics.

Embeddings/chunks are treated as customer data and may not live in a global cross-client customer vector index. Tenant restriction happens before retrieval/ranking and all derived chunks retain exact source/version lineage.

See `docs/DATA_ARCHITECTURE.md` for the detailed contract.

## Documents, evidence and projections

Incoming documents are evidence sources. Outgoing documents are controlled projections.

```text
incoming evidence
   -> encrypted tenant Evidence Vault
   -> extracted/proposed facts
   -> provenance / contradiction / gap validation
   -> human acceptance where required
   -> persistent structured client state
   -> workflow assessments/findings/actions
   -> client-grade projections (RoPA / DPIA / management report / action plan)
```

This avoids a common consultancy failure mode in which the RoPA, DPIA, processor register and management report become separate manually maintained truths.

Every material projection should record the state/evidence/source/review versions from which it was produced.

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
  -> tenant authorization + data classification
  -> classify/register evidence
  -> extract candidate facts
  -> normalize to canonical privacy concepts
  -> provenance / contradiction / missing-information validation
  -> select jurisdiction
  -> select methodology
  -> resolve approved legal sources
  -> execute deterministic assessment steps
  -> retrieve only required tenant-scoped context for AI stages
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

Answers become tenant-scoped evidence or user-confirmed facts with provenance. A model-generated question never by itself establishes a legal requirement.

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

Generalized execution additionally requires run/organisation/engagement linkage, state snapshots/hashes, review decisions, proposed state changes and data-plane authorization context. JSON Schemas in `contracts/` are the machine-readable source of truth.

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

Automation economics may not be improved by removing a required review gate.

## Integration with SolidPrivacy Scrub

The intended privacy-preserving flow is:

```text
ORIGINAL DOCUMENT
  -> tenant Evidence Vault / controlled local source
  -> SolidPrivacy Scrub
       local/trusted detection
       human review
       local/private Scrub Key
  -> SCRUBBED/MINIMISED ARTIFACT
  -> SolidPrivacy AI Workflow
       facts / DPIA / DSAR / RoPA / vendor / breach / other analysis
  -> SCRUBBED AI RESULT
  -> controlled local/trusted Reinsert
  -> Delivery Artifact Vault / Export / Audit
```

The Scrub Key and original identifier mapping remain outside the external AI workflow unless a separately approved use case explicitly requires otherwise. Cloud processing is never implied merely because a workflow exists.

The Client Data Plane may retain original evidence where contractually/legally appropriate, but access to originals and access to reinsertion/key material should be separable capabilities rather than one broad AI-runtime credential.

## Operating economics as architecture telemetry

The potential disruptive advantage of POaaS must be demonstrated from controlled operational evidence.

The execution/audit plane should therefore emit non-content timing/resource events that allow calculation of:

- Human Minutes per Privacy Outcome (HMPO);
- human minutes by operator/qualified PO/independent FG-DPO/client role;
- cycle time and waiting-client time;
- model/provider/compute cost;
- first-pass acceptance and rework;
- exception/escalation rate;
- evidence completeness;
- client-state reuse across workflows/deliverables.

These metrics are observability metadata, not customer content logs. Efficiency targets may not weaken evidence, security or review thresholds.

See `docs/POAAS_OPERATING_ECONOMICS.md`.

## Project governance architecture

SolidPrivacy development/release itself is governed as a controlled system.

Authority is split deliberately:

```text
market-predictions/control-plane
  -> canonical cross-project governance doctrine / freshness / claim lifecycle

solidprivacy-nl/solidprivacy
  -> product roadmap / current state / workpackages / work claims / decisions
     architecture / schemas / tests / exact-head evidence / handovers / release state

private Client Data Plane
  -> real customer evidence and operational privacy state
```

The project-local mandatory source-of-truth set is defined by `control/GOVERNANCE_MANIFEST.json` and includes:

- `CURRENT_STATE.md`;
- `ROADMAP.md`;
- `WORKPACKAGES.md`;
- `CHANGELOG.md`;
- `DECISION_LOG.md`;
- `control/WORK_CLAIMS.json`;
- `handover/`;
- architecture/data contracts and exact-head test evidence.

Consequential implementation uses separate `implementation_operations` and `governance_release_assurance` roles. The latter reaches an initial `PASS | FAIL | INDETERMINATE` from source, acceptance criteria and raw evidence rather than implementation self-assessment. Repairs require a fresh candidate/assurance pass.

Work claims are reconciled against live branch/PR/dependency state under the canonical control-plane lifecycle standard. A materially stale integration line stops accumulating functional work and is reconciled or explicitly superseded.

`.github/workflows/project-governance-gate.yml` provides a static structural drift check; it cannot replace live reconciliation or independent assurance.

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
- embed real personal/client data in tests, issues or handovers;
- create uncontrolled autonomous legal decisions;
- duplicate the Scrub anonymisation engine;
- introduce cloud document processing by default;
- store real client evidence or become the production multi-tenant customer database itself;
- give an AI provider direct/unrestricted database access;
- make a large GRC UI the prerequisite for proving workflow/data/client-state contracts;
- infer project completion from chat memory or implementation narrative without repository/evidence reconciliation.
