# SolidPrivacy Roadmap

Status date: 2026-08-11

This file is authoritative for product sequencing and milestone dependencies. `docs/architecture.md` is authoritative for architectural responsibilities. `docs/DATA_ARCHITECTURE.md` defines the private client-data boundary. `docs/POAAS_REFERENCE_WORKFLOW.md` defines the reference customer-lifecycle flow. `docs/POAAS_OPERATING_ECONOMICS.md` defines the evidence needed before claiming disruptive unit economics. Project execution/governance follows `control/PROJECT_GOVERNANCE_BOOTSTRAP.md`.

## Product objective

Build a controlled Privacy Officer operating system for EU/EEA + Netherlands that can support a scalable **Privacy Officer as a Service (POaaS)** operating model.

AI may perform high-volume extraction, analysis and drafting over approved scrubbed/minimised inputs, while deterministic contracts, authoritative legal sources, provenance, privacy-boundary policies and qualified human review control material conclusions.

The system must ultimately support three different kinds of durable state without conflating them:

1. **governed global capability state** — law, sources, methodologies, controls, workflows, model policies and evaluations maintained by SolidPrivacy;
2. **private client data state** — real client evidence, structured organisational privacy state, retrieval indexes, deliverable artefacts and operational audit held outside the public/shared repository;
3. **project/release governance state** — roadmap, workpackages, work claims, decisions, handovers, tests and release evidence maintained in GitHub under the canonical control-plane method.

The shared repository is the governed capability and project source-of-truth layer. It is **not** the location for real client dossiers, direct identifiers, Scrub Keys or production secrets.

## Principles

1. **Evidence before reasoning.** Findings trace to evidence or remain explicit inference/assumption.
2. **Methodology is not law.** Assessment templates never silently become binding legal requirements.
3. **Deterministic gates before generative layers.** Schema, integrity, source, privacy-boundary and high-impact gates precede authoring.
4. **One canonical processing model.** DPIA, RoPA, breach, vendor, retention and DSAR reuse shared concepts.
5. **Human accountability.** Designated privacy professionals approve/reject material conclusions.
6. **Scrub is a privacy boundary, not an anonymity claim.** Original identifiers and the Scrub Key stay outside external AI calls; scrubbed/pseudonymised content can still be personal data.
7. **No model call without an egress policy.** Provider/model, content class, permitted egress and training/retention/logging posture must be explicit.
8. **Vertical slices before breadth.** Complete one trustworthy end-to-end workflow before mass-importing skills.
9. **Exact-head assurance.** Capability workpackages require executable regression evidence on the reviewed commit.
10. **Approved legal context before legal drafting.** Generative analysis may only consume a deterministically assembled, source-governed legal context bundle.
11. **Client state is first-class.** A workflow run is temporary; the organisation and its accepted privacy state persist across workflows and service periods.
12. **Documents are evidence, not the source of truth.** RoPA, DPIA and management reports are projections of governed structured state; changing one source fact must not require manual edits in unrelated documents.
13. **Questions should be gap-driven.** After evidence ingestion, ask clients only for material missing, contradictory or outdated information rather than repeatedly issuing generic questionnaires.
14. **Client isolation is architectural, not procedural.** Tenant/customer boundaries, access policy, data classification and evidence storage are explicit contracts.
15. **Changes propagate through dependencies.** A new processor, system, purpose, data category, measure or legal-source change creates impact/review requirements; it does not silently regenerate approved conclusions.
16. **Commitments are traceable.** Engagement scope and promised deliverables must be machine-readable enough to determine what remains due, blocked, under review or complete.
17. **Thin operational surfaces before a large GRC platform.** Build only the operator/client views needed to execute proven workflows; do not let UI design become the architecture.
18. **The Client Data Plane precedes real client state.** Production client dossiers may not be introduced before tenant isolation, storage, key, retrieval, retention and audit boundaries are implemented and assured.
19. **The model is not the dossier store.** AI receives bounded tenant-scoped context for one governed task; cross-client memory and unrestricted datastore access are prohibited.
20. **Efficiency is measured, not assumed.** Human Minutes per Privacy Outcome (HMPO), role-specific human time, cycle time, rework and model/compute cost are instrumented without weakening evidence/review gates.
21. **GitHub is the project source of truth.** Roadmap, workpackages, current state, claims, decisions, handovers and exact-head evidence are repository-backed; chat memory and PR narrative cannot silently override live project state.
22. **Implementation cannot certify itself.** Consequential candidates pass independent `governance_release_assurance`; repairs create new candidate identities.

## Target operating architecture

```text
GLOBAL GOVERNED CAPABILITY PLANE
law / sources / methodologies / canonical semantics / controls / workflows / evals
                         |
                         v
EXECUTION + ASSURANCE PLANE
workflow runs / privacy gates / retrieval / model calls / validation / human review / audit
                         |
                         v
PRIVATE CLIENT DATA PLANE
evidence vault / state database / tenant retrieval index / artifact vault / keys / backups
                         |
                         v
CLIENT OPERATING STATE
organisation / engagement / accepted facts / processing / assessments / findings / actions
                         |
                         v
DELIVERY + CONTINUOUS-SERVICE PLANE
client questions / PO work queue / deliverables / reporting / change intake / reassessment
```

A POaaS customer should become a durable organisational state over which multiple governed workflows operate, rather than a folder containing a series of unrelated reports. The data plane that stores that state remains private and tenant-controlled; the public/shared GitHub repository never becomes the customer database.

## Phase 0 — Operating architecture and governance foundation

### WP0 / PR #1 — Privacy operating architecture
Status: COMPLETE IN DRAFT STACK

Delivered: architecture layers, contracts, vocabularies, jurisdictions, methodologies, source governance, provenance, control/evidence concepts and workflow structure.

### GOVDATA-FOUNDATION / PR #8 — POaaS client model + data plane + project governance foundation
Status: IMPLEMENTED IN DRAFT CANDIDATE — independent closeout/assurance required

This cross-cutting architecture/governance package records insights exposed by walking the system as an actual POaaS business rather than only as isolated privacy workflows.

Delivered/defined:
- organisation/engagement/persistent-state operating model;
- POaaS reference customer lifecycle;
- documents-as-evidence/projections and dependency impact semantics;
- private Client Data Plane boundary;
- initial dedicated-per-client EU/EEA isolation posture for healthcare production;
- AI scoped-retrieval/no-cross-client-memory rule;
- HMPO/unit-economics measurement framework;
- project-local adoption of the canonical control-plane governance method;
- current-state, workpackage, work-claim, decision, changelog and handover source-of-truth structure;
- project-specific independent release-assurance contract;
- static governance CI gate.

This package changes architecture/sequencing; it does not enable real client data or approve a production data/model provider.

## Phase 1 — DPIA reference vertical slice

DPIA remains the first reference workflow because it exercises facts, methodology, legal sources, risk, controls, evidence, AI boundaries and human review.

### WP1 / PR #2 — Canonical privacy + Dutch DPIA model
Status: COMPLETE

- canonical processing activity and DPIA contracts;
- Dutch Rijksmodel adapter;
- DPV semantic mapping;
- synthetic normal/high-risk cases.

### WP2 / PR #3 — Executable DPIA contracts + pre-scan
Status: COMPLETE — exact-head CI green

- JSON Schema + referential integrity;
- deterministic Dutch pre-scan;
- legal decision separated from methodology score;
- governed AP/EDPB handling;
- high-residual-risk safeguards.

### WP3 / PR #4 — Evidence + fact provenance
Status: COMPLETE — exact-head CI green

- privacy-fact and evidence-pack contracts;
- observed/inferred/assumption/user-confirmed states;
- contradictions and missing information;
- deterministic analysis/finalisation readiness;
- extractor boundary and document-to-DPIA stage model.

### WP4 / PR #5 — Safe AI boundary + fact extraction validator
Status: COMPLETE — exact-head CI green

- provider-independent fact-extraction interface;
- executable model-call privacy policy;
- explicit scrubbed-personal-data egress permission;
- external Scrub Key/direct-identifier blocks;
- provider training/retention/logging gates;
- deterministic fixture provider for CI;
- detector → provenance validator;
- support-proof verification;
- contradiction detection;
- no automatic fact/legal acceptance.

No real external provider is approved or enabled by WP4.

### WP5 / PR #6 — Governed legal context + AI-assisted DPIA analysis/drafting
Status: COMPLETE — exact-head CI green in draft stack

Delivered:
- curated source-bound DPIA legal rules;
- legal-context request/bundle contracts;
- resolver against the full governed source registry;
- jurisdiction, authority and freshness checks;
- explicit forward-only treatment of non-final consultation material;
- structured DPIA analysis contract;
- fact/rule/claim/risk/measure traceability validator;
- unreviewed facts remain explicitly unresolved in draft sections;
- provider cannot self-validate or finalise residual risk;
- deterministic fixture analysis and adversarial regressions.

No real external analysis provider is approved or enabled by WP5.

### WP6 / PR #7 — Privacy Officer review + report/reinsert boundary
Status: IMPLEMENTED — exact-head CI green in draft stack; stack/claim closeout governed by live state

Delivered:
- hash-bound review package;
- item-level review targets and accept/reject/change/request-evidence actions;
- human residual-risk, prior-consultation and DPO/FG disposition;
- unresolved-question/assumption finalisation gates;
- evidence/source appendices;
- deterministic scrubbed reviewed report;
- local-only Scrub reinsertion handoff with no Scrub Key or direct identifiers;
- minimal immutable review audit record and tamper detection.

### M1 — Chained DPIA reference execution
Status: NEXT PRODUCT GATE

Before extracting a generalized platform, prove the first complete vertical slice as one execution rather than only as individually green components.

Required acceptance:
- one positive synthetic case runs end-to-end:
  evidence → extraction → provenance/readiness → pre-scan → legal context → governed analysis → Privacy Officer review → report/reinsert/audit;
- one blocked/adversarial case proves deterministic stop behaviour;
- one run identifier and correlated stage evidence demonstrate that no manual hidden handoff is required between stages;
- exact-head CI proves the integrated chain;
- execution emits the initial non-content operational measurement events needed for HMPO/cycle-time/cost instrumentation;
- M1 reports human intervention count/time where measurable, model/compute usage, rework/validation events and blocked-path timing without claiming commercial-scale economics from the small synthetic sample.

**Gate:** WP7 may not generalise execution/audit infrastructure until M1 is green.

## Phase 2 — Shared operating, data and client substrate

The lesson from the DPIA slice and POaaS reference workflow is that shared infrastructure must support workflow execution, secure private storage and durable client state. Building many new workflows before these concepts are explicit would create isolated agents, duplicate customer facts and unacceptable data-boundary ambiguity.

### WP7 — Generalised workflow execution + audit model

Goal: extract reusable run machinery proven by M1.

Required:
- run/workflow IDs and versions;
- deterministic stage state and stop conditions;
- step replay rules;
- input/output hashes;
- source/model/prompt/policy versions;
- human decisions;
- failure/abstention states;
- immutable audit events across workflows;
- parent/child workflow relationship for orchestrated service flows;
- operational timing/resource events needed to calculate role-specific human touch time, cycle time and model/provider cost without logging customer bodies into general telemetry.

### WP8 — Client Data Plane + tenant/security boundary

Goal: implement and independently assure the private storage/security substrate **before** real durable client state is enabled.

Detailed authority: `docs/DATA_ARCHITECTURE.md` and `docs/workpackages/WP8_CLIENT_DATA_PLANE.md`.

Initial production posture:
- dedicated EU/EEA data project/account per healthcare client;
- separate relational database, encrypted evidence/object store, retrieval/index and key/credential scope;
- tenant identity/authorization before any read/write/retrieval;
- tenant filter before retrieval ranking;
- no global cross-client customer vector index;
- no model/provider database credentials;
- bounded runtime retrieval/minimisation before model context assembly;
- EU/EEA primary storage/backups by default;
- retention/deletion/offboarding and backup/restore semantics;
- access/model-egress/security audit events;
- negative cross-tenant tests and live target-state assurance.

A later pooled multi-tenant architecture is a separate optimisation and cannot be inferred as safe from application-level `tenant_id` fields alone.

**Hard gate:** no production real-client dossier/state work proceeds until WP8 has independent PASS for the enabled data classes and target environment.

### WP9 — Client / organisation / engagement operating model

Goal: make the customer and the commercial service commitment first-class on the assured Client Data Plane.

Required canonical contracts/concepts:
- `organisation` / legal entities / organisational units;
- `engagement` / service period / jurisdiction / service package;
- stakeholders, roles and designated reviewers;
- promised deliverables and acceptance state;
- service scope, exclusions and due dates;
- tenant/data-plane linkage without leaking client identifiers into public fixtures;
- links from workflow runs and review records to the correct client/engagement;
- synthetic medium-sized Dutch home-care organisation fixture.

**Design rule:** sector profiles such as healthcare/home care may define expected evidence, terminology or control baselines, but may not masquerade as legal authority.

### WP10 — Persistent organisational privacy state + dependency graph

Goal: turn accepted facts from individual assessments into reusable organisational knowledge.

Required:
- versioned accepted facts with provenance and validity/effective dates;
- canonical systems, processors/recipients, processing activities, data categories, purposes, legal bases, retention and measures;
- distinction between proposed, provenance-valid, human-accepted, superseded and disputed state;
- reuse across DPIA/RoPA/vendor/breach/DSAR/retention workflows;
- object dependency graph;
- change-event model and impact queue;
- no silent overwrite of previously approved state;
- document/report projections reference the structured state version from which they were produced.

### WP11 — Executable control / evidence / finding / remediation model

Goal: convert privacy recommendations from prose into operationally trackable work.

Required:
- control ↔ implementation ↔ evidence ↔ finding ↔ remediation ↔ approval;
- owner, status, due date and verification state;
- materiality/prioritisation rules with human override;
- evidence freshness/expiry;
- links to affected processing activities, systems, processors and assessments;
- no unlicensed normative-text replication.

### WP12 — Model gateway + privacy-policy hardening

WP4 is the minimum call boundary; WP12 generalises it only after real workflow/data/client-state requirements are known:
- real/multiple provider adapters and routing;
- organisation-level data classification;
- local/external inference routing;
- prompt/model/policy registry;
- secrets isolation;
- retries/cost/latency controls;
- safe telemetry;
- provider terms/retention/training review cycle;
- explicit integration with WP8 tenant-scoped retrieval rather than direct datastore access;
- no-training/no-cross-client-memory default posture for client content.

## Phase 3 — POaaS onboarding reference slice

This phase turns the architecture into the first repeatable sellable customer onboarding process. The reference scenario is a medium-sized Dutch home-care provider running entirely on synthetic/non-personal evidence for acceptance.

### WP13 — Engagement onboarding + evidence request orchestration

Goal: start from a signed POaaS engagement and produce a controlled evidence intake rather than a generic document request.

Required:
- service-package → evidence-requirement mapping;
- initial organisation questionnaire for facts not discoverable from evidence;
- secure evidence intake into the WP8 client data plane;
- document/evidence inventory and classification;
- Scrub/minimisation routing policy;
- completeness/coverage state;
- contradiction and missing-information queue;
- targeted client-question generation from validated gaps;
- question/answer provenance and human confirmation state;
- no direct use of model-generated questions as legal requirements.

### WP14 — RoPA / processing inventory backbone

Goal: produce and maintain the first reusable client processing inventory from evidence and confirmed facts.

Required:
- organisation-wide processing discovery and deduplication;
- processing activity ↔ systems ↔ processors ↔ data ↔ subjects ↔ purposes ↔ legal basis ↔ retention links;
- completeness/gap indicators;
- human approval of material processing-state changes;
- import/mapping support for an existing client RoPA;
- output projection for a client-grade Article 30 register;
- changed-state impact signals for dependent DPIAs/vendor/retention work.

### WP15 — Privacy baseline + action plan + deliverable projection

Goal: transform client state into the initial POaaS onboarding deliverable set.

Required:
- governed baseline/control assessment over available evidence;
- findings with legal-claim classification and evidence traceability;
- remediation/action register with owner, priority and due date;
- DPIA candidate/screening register from the processing inventory;
- processor/vendor coverage overview;
- management summary derived from structured findings;
- deliverable manifest showing complete / blocked / needs-review / waiting-on-client;
- deterministic lineage from each report section to the state/evidence/review version used.

### M2 — Synthetic POaaS onboarding acceptance

Reference scenario: a synthetic medium-sized Dutch home-care institution with realistic but non-personal evidence and intentional gaps/conflicts.

M2 is green only when one chained service flow can:

```text
signed engagement
  -> tenant/client data project
  -> organisation profile
  -> secure evidence request/intake
  -> classification + scrub routing
  -> evidence/fact extraction
  -> contradiction/missing-information queue
  -> targeted client questions
  -> accepted organisational privacy state
  -> RoPA projection
  -> DPIA screening
  -> baseline/findings/actions
  -> Privacy Officer review
  -> promised deliverable package
  -> persistent audit + next-action state
```

The acceptance corpus must include at least one changed processor/system fact and prove that affected downstream objects are marked for reassessment rather than silently overwritten.

M2 must also produce an operating-economics report under `docs/POAAS_OPERATING_ECONOMICS.md`, including at minimum:
- HMPO for an accepted processing activity;
- HMPO for a DPIA screen;
- total onboarding human touch time by role;
- qualified Privacy Officer share versus operator work;
- model/compute cost;
- cycle time versus client-wait time;
- first-pass/rework/exception rates;
- evidence/state reuse across multiple deliverables;
- number of duplicate manual-entry steps avoided.

No commercial pricing/reduction claim is considered evidenced merely because M2 passes; M2 establishes the first controlled baseline.

## Phase 4 — Privacy Officer workflow expansion

Only after M2 proves that new workflows can consume/update persistent client state on the assured data plane should breadth accelerate.

Current order:

1. **Personal-data-breach assessment** — bounded evidence/timeline/risk/notification workflow with mandatory human sign-off; reuse known systems/processings/subjects.
2. **Vendor / Article 28 assessment** — processor inventory, clause extraction, requirement mapping, divergences, remediation and human review.
3. **DSAR / right of access** — identity, deadline control, system/document discovery, third-party data handling, exemptions, Scrub/redaction, delivery evidence and auditability.
4. **International transfers** — inventory, mechanism, SCC/BCR/adequacy, transfer-impact evidence and supplementary measures.
5. **Retention/deletion governance** — purpose/data retention mappings, legal/policy basis, deletion evidence and holds.
6. **AI privacy / IAMA / FRIA coordination** — coordinate but do not conflate GDPR DPIA, AI Act and rights-assessment obligations.

Each workflow must consume existing accepted client state where possible and return proposed state changes/findings/actions through review gates rather than maintaining a private copy of organisation facts.

## Phase 5 — Continuous POaaS operating layer

After multiple workflows share the client substrate:

### Continuous change intake
- new system/vendor/processing/change requests;
- incident and rights-request intake;
- evidence expiry and control re-verification;
- legal-source change impact;
- reassessment queue derived from dependencies.

### Privacy Officer/operator work management
- review queue prioritised by legal deadline/materiality/service commitment;
- waiting-on-client queue;
- open findings/remediation verification;
- separation of AI/operator/qualified-officer responsibilities;
- escalation rules for DPO/FG or specialist legal review.

### Client and management delivery
- engagement/deliverable status;
- open actions and decisions;
- privacy risk/control view;
- recurring management report;
- annual DPO/privacy report where in scope;
- evidence-backed history of what changed and why.

### Operating-economics control
- HMPO and human-touch trends by outcome/workflow;
- role mix and exception/escalation rate;
- state reuse versus recollection;
- model/provider cost and routing efficiency;
- first-pass acceptance/rework/quality escape rate;
- service-margin analysis separated from quality/assurance thresholds.

### Thin product surfaces
Build only after contracts/workflows are stable enough to support them:
- internal PO workbench;
- controlled client evidence/question portal;
- management readout;
- no large configurable GRC platform as an early dependency.

## Phase 6 — DPO/FG operating layer

Where SolidPrivacy offers or supports an external DPO/FG function, maintain role/independence boundaries distinct from operational PO execution:
- obligations/open-risk view;
- annual DPO/FG reporting;
- audit programme;
- recurring legal-source freshness review;
- policy/control maturity;
- portfolio evidence;
- management actions;
- independent sign-off/accountability records;
- conflict-of-interest safeguards between operational remediation ownership and independent oversight.

## Explicitly deferred

- mass-importing prompt/skill collections;
- broad multi-jurisdiction expansion;
- autonomous final legal decisions;
- large GRC UI/platform before workflow/data/client-state contracts stabilise;
- pooled multi-tenant real-client storage before dedicated-tenant security is proven and a separate assurance decision approves pooling;
- website evidence collection without a consuming workflow;
- ISO normative-content replication without licensing;
- real external AI-provider enablement without verified/approved model-call and data-plane policy;
- storing real client evidence, direct identifiers, model payloads, credentials or Scrub Keys in this shared repository.

## Roadmap health checks

Revisit ordering when:
- EDPB finalises the 2026 DPIA or breach template;
- the Dutch Rijksmodel/PAR model materially changes;
- a completed vertical slice exposes a missing shared prerequisite;
- Scrub changes its integration contract;
- a source/legal change invalidates an executable rule;
- provider data-handling/subprocessor/retention terms change;
- a selected Client Data Plane provider materially changes region, backup, key or access semantics;
- POaaS onboarding exposes a client-state concept that cannot be represented without duplication;
- HMPO/rework data shows a workflow is not economically or operationally suitable for the assumed service model;
- another workflow has materially higher operational/regulatory value.

Every roadmap change must explain **why the dependency/order changed**, not merely rename workpackages.

## Governance completion rule

Roadmap status is not updated from chat or implementation narrative alone. For consequential work, reconcile:

```text
ROADMAP
<-> WORKPACKAGES
<-> CURRENT_STATE
<-> WORK_CLAIMS
<-> live branch/PR/dependency state
<-> exact-head CI/evals
<-> independent assurance
<-> handover/claim disposition
<-> CHANGELOG / DECISION_LOG
```

A package is not `COMPLETE` while material branch drift, an orphaned active claim, missing required handover, stale current-state reference or outstanding required assurance exists.
