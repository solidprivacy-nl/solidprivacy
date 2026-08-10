# SolidPrivacy Roadmap

Status date: 2026-08-11

This file is authoritative for sequencing. `docs/architecture.md` remains authoritative for architectural responsibilities. `docs/POAAS_REFERENCE_WORKFLOW.md` defines the reference customer-lifecycle flow that the roadmap must eventually execute.

## Product objective

Build a controlled Privacy Officer operating system for EU/EEA + Netherlands that can support a scalable **Privacy Officer as a Service (POaaS)** operating model.

AI may perform high-volume extraction, analysis and drafting over approved scrubbed/minimised inputs, while deterministic contracts, authoritative legal sources, provenance, privacy-boundary policies and qualified human review control material conclusions.

The system must ultimately support two kinds of state at the same time:

1. **governed global capability state** — law, sources, methodologies, controls, workflows, model policies and evaluations maintained by SolidPrivacy;
2. **isolated client operating state** — organisation facts, engagements, evidence, processing activities, systems, processors, assessments, findings, actions, deliverables and review history for one client.

The public/shared repository is the governed capability layer. It is **not** the location for real client evidence or identifiers.

## Principles

1. **Evidence before reasoning.** Findings trace to evidence or remain explicit inference/assumption.
2. **Methodology is not law.** Assessment templates never silently become binding legal requirements.
3. **Deterministic gates before generative layers.** Schema, integrity, source, privacy-boundary and high-impact gates precede authoring.
4. **One canonical processing model.** DPIA, RoPA, breach, vendor, retention and DSAR reuse shared concepts.
5. **Human accountability.** Designated privacy professionals approve/reject material conclusions.
6. **Scrub is a privacy boundary, not an anonymity claim.** Original identifiers and the Scrub Key stay outside external AI calls; scrubbed/pseudonymised content can still be personal data.
7. **No model call without an egress policy.** Provider/model, content class, permitted egress and training/retention/logging posture must be explicit.
8. **Vertical slices before breadth.** Complete one trustworthy end-to-end workflow before mass-importing skills.
9. **Exact-head assurance.** Capability work packages require executable regression evidence on the reviewed commit.
10. **Approved legal context before legal drafting.** Generative analysis may only consume a deterministically assembled, source-governed legal context bundle.
11. **Client state is first-class.** A workflow run is temporary; the organisation and its accepted privacy state persist across workflows and service periods.
12. **Documents are evidence, not the source of truth.** RoPA, DPIA and management reports are projections of governed structured state; changing one source fact must not require manual edits in unrelated documents.
13. **Questions should be gap-driven.** After evidence ingestion, the system should ask clients only for material missing, contradictory or outdated information rather than repeatedly issuing generic questionnaires.
14. **Client isolation is architectural, not procedural.** Tenant/customer boundaries, access policy, data classification and evidence storage are explicit contracts.
15. **Changes propagate through dependencies.** A new processor, system, purpose, data category, measure or legal-source change should create an impact/review requirement for affected objects; it should not silently regenerate approved conclusions.
16. **Commitments are traceable.** Engagement scope and promised deliverables must be machine-readable enough to determine what remains due, blocked, under review or complete.
17. **Thin operational surfaces before a large GRC platform.** Build only the operator/client views needed to execute proven workflows; do not let UI design become the architecture.

## Target operating architecture

```text
GLOBAL GOVERNED CAPABILITY PLANE
law / sources / methodologies / canonical semantics / controls / workflows / evals
                         |
                         v
EXECUTION + ASSURANCE PLANE
workflow runs / privacy gates / model calls / validation / review / audit
                         |
                         v
ISOLATED CLIENT OPERATING PLANE
organisation / engagement / evidence / privacy state / assessments / actions
                         |
                         v
DELIVERY + CONTINUOUS-SERVICE PLANE
client questions / PO work queue / deliverables / reporting / change intake
```

A POaaS customer should therefore become a durable organisational state over which multiple governed workflows operate, rather than a folder containing a series of unrelated reports.

## Phase 0 — Operating architecture

### WP0 / PR #1 — Privacy operating architecture
Status: COMPLETE IN DRAFT STACK

Delivered: architecture layers, contracts, vocabularies, jurisdictions, methodologies, source governance, provenance, control/evidence concepts and workflow structure.

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
Status: COMPLETE IMPLEMENTATION — current PR head exact-head CI green

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
Status: NEXT

Before extracting a generalized platform, prove the first complete vertical slice as one execution rather than only as individually green components.

Required acceptance:
- one positive synthetic case runs end-to-end:
  evidence → extraction → provenance/readiness → pre-scan → legal context → governed analysis → Privacy Officer review → report/reinsert/audit;
- one blocked/adversarial case proves deterministic stop behaviour;
- one run identifier and correlated stage evidence demonstrate that no manual hidden handoff is required between stages;
- exact-head CI proves the integrated chain.

**Gate:** WP7 may not generalise execution/audit infrastructure until M1 is green.

## Phase 2 — Shared operating and client substrate

The lesson from the DPIA slice and POaaS reference workflow is that shared infrastructure must support both **workflow execution** and **durable client state**. Building many new workflows before these two concepts are explicit would create isolated agents and duplicate customer facts.

### WP7 — Generalised workflow execution + audit model

Goal: extract the reusable run machinery proven by M1.

Required:
- run/workflow IDs and versions;
- deterministic stage state and stop conditions;
- step replay rules;
- input/output hashes;
- source/model/prompt/policy versions;
- human decisions;
- failure/abstention states;
- immutable audit events across workflows;
- parent/child workflow relationship for orchestrated service flows.

### WP8 — Client / organisation / engagement operating model

Goal: make the customer and the commercial service commitment first-class without placing real client data in the shared repository.

Required canonical contracts/concepts:
- `organisation` / legal entities / organisational units;
- `engagement` / service period / jurisdiction / service package;
- stakeholders, roles and designated reviewers;
- promised deliverables and acceptance state;
- service scope, exclusions and due dates;
- client/tenant boundary and access classification;
- links from workflow runs and review records to the correct client/engagement without embedding identifiers in public test fixtures;
- synthetic medium-sized Dutch home-care organisation fixture.

**Design rule:** sector profiles such as healthcare/home care may define expected evidence, terminology or control baselines, but may not masquerade as legal authority.

### WP9 — Persistent organisational privacy state + dependency graph

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

### WP10 — Executable control / evidence / finding / remediation model

Goal: convert privacy recommendations from prose into operationally trackable work.

Required:
- control ↔ implementation ↔ evidence ↔ finding ↔ remediation ↔ approval;
- owner, status, due date and verification state;
- materiality/prioritisation rules with human override;
- evidence freshness/expiry;
- links to affected processing activities, systems, processors and assessments;
- no unlicensed normative-text replication.

### WP11 — Model gateway + privacy-policy hardening

WP4 is the minimum call boundary; WP11 generalises it only after real workflow and client-state requirements are known:
- real/multiple provider adapters and routing;
- organisation-level data classification;
- local/external inference routing;
- prompt/model/policy registry;
- secrets isolation;
- retries/cost/latency controls;
- safe telemetry;
- provider terms/retention/training review cycle.

## Phase 3 — POaaS onboarding reference slice

This phase turns the architecture into the first repeatable sellable customer onboarding process. The reference scenario is a medium-sized Dutch home-care provider.

### WP12 — Engagement onboarding + evidence request orchestration

Goal: start from a signed POaaS engagement and produce a controlled evidence intake rather than a generic document request.

Required:
- service-package → evidence-requirement mapping;
- initial organisation questionnaire for facts not discoverable from evidence;
- document/evidence inventory and classification;
- Scrub/minimisation routing policy;
- completeness/coverage state;
- contradiction and missing-information queue;
- targeted client-question generation from validated gaps;
- question/answer provenance and human confirmation state;
- no direct use of model-generated questions as legal requirements.

### WP13 — RoPA / processing inventory backbone

Goal: produce and maintain the first reusable client processing inventory from evidence and confirmed facts.

Required:
- organisation-wide processing discovery and deduplication;
- processing activity ↔ systems ↔ processors ↔ data ↔ subjects ↔ purposes ↔ legal basis ↔ retention links;
- completeness/gap indicators;
- human approval of material processing-state changes;
- import/mapping support for an existing client RoPA;
- output projection for a client-grade Article 30 register;
- changed-state impact signals for dependent DPIAs/vendor/retention work.

### WP14 — Privacy baseline + action plan + deliverable projection

Goal: transform the client state into the initial POaaS onboarding deliverable set.

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
  -> organisation profile
  -> evidence request/intake
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

## Phase 4 — Privacy Officer workflow expansion

Only after M2 proves that new workflows can consume and update persistent client state should breadth accelerate.

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

### Thin product surfaces
Build only after contracts/workflows are stable enough to support them:
- internal PO workbench;
- controlled client evidence/question portal;
- management readout;
- no large configurable GRC platform as an early dependency.

## Explicitly deferred

- mass-importing prompt/skill collections;
- broad multi-jurisdiction expansion;
- autonomous final legal decisions;
- large GRC UI/platform before workflow and client-state contracts stabilise;
- website evidence collection without a consuming workflow;
- ISO normative-content replication without licensing;
- real external AI-provider enablement without verified/approved model-call policy;
- storing real client evidence, direct identifiers or Scrub Keys in this shared repository.

## Roadmap health checks

Revisit ordering when:
- EDPB finalises the 2026 DPIA or breach template;
- the Dutch Rijksmodel/PAR model materially changes;
- a completed vertical slice exposes a missing shared prerequisite;
- Scrub changes its integration contract;
- a source/legal change invalidates an executable rule;
- provider data-handling terms change;
- POaaS onboarding exposes a client-state concept that cannot be represented without duplication;
- another workflow has materially higher operational/regulatory value.

Every roadmap change must explain **why the dependency/order changed**, not merely rename work packages.
