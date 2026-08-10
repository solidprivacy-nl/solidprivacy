# SolidPrivacy Roadmap

Status date: 2026-08-10

This file is authoritative for sequencing. `docs/architecture.md` remains authoritative for architectural responsibilities.

## Product objective

Build a controlled Privacy Officer operating system for EU/EEA + Netherlands. AI may perform high-volume extraction, analysis and drafting over approved scrubbed/minimised inputs, while deterministic contracts, authoritative legal sources, provenance, privacy-boundary policies and qualified human review control material conclusions.

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
Status: COMPLETE IMPLEMENTATION — exact-head CI green on implementation head; closeout head must remain green

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

### WP6 — Privacy Officer review + report/reinsert boundary
Status: NEXT

Goal: turn the governed AI draft into a human-accountable decision package and scrubbed deliverable.

Required:
- item-level review decisions for facts, claims, risks, measures and draft sections;
- accept / reject / change / request-evidence actions;
- rationale requirements for material changes/rejections;
- explicit human residual-risk conclusion;
- explicit prior-consultation disposition;
- unresolved issue queue and finalisation gate;
- evidence/source appendix;
- management summary + full scrubbed report representation;
- controlled Scrub reinsertion handoff containing **no Scrub Key** and no direct identifiers;
- immutable minimal review record containing reviewed draft hash/version, source/evidence/model/policy versions and reviewer decision timestamps.

**Roadmap dependency note:** a minimal immutable review/audit record is required inside WP6 because accountable human sign-off is not meaningful without it. WP7 still generalises workflow/run event sourcing, replayability and audit infrastructure across all workflows.

**DPIA milestone:** representative synthetic corpus proves scrubbed input → evidence → facts → pre-scan → legal context → DPIA draft → validator → Privacy Officer review → report/reinsert handoff.

## Phase 2 — Shared operating substrate

Extract reusable capabilities from the completed DPIA slice rather than building later workflows as bespoke agents.

### WP7 — Workflow execution + audit model
- generalised run/workflow IDs and versions;
- step state/replayability;
- input/output hashes;
- source/model/prompt/policy versions;
- human decisions;
- failure/abstention states;
- immutable audit events across workflows.

### WP8 — Control/evidence/remediation model
- executable OSCAL-inspired control objects;
- control ↔ implementation ↔ evidence ↔ finding ↔ remediation;
- owners/status/due dates/verification;
- no unlicensed normative-text replication.

### WP9 — Model gateway + privacy-policy hardening
WP4 is the minimum call boundary; WP9 generalises it:
- real/multiple provider adapters and routing;
- organisation-level data classification;
- local/external inference routing;
- prompt/model/policy registry;
- secrets isolation;
- retries/cost/latency controls;
- safe telemetry;
- provider terms/retention/training review cycle.

## Phase 3 — Privacy Officer workflow expansion

Current order after DPIA:

1. **RoPA / processing inventory** — shared organisational state supporting DPIA, retention, vendor, transfer and DSAR scoping.
2. **Personal-data-breach assessment** — bounded evidence/timeline/risk/notification workflow with mandatory human sign-off.
3. **DSAR / right of access** — remains high priority but needs identity, deadline control, system/document discovery, third-party data handling, exemptions, Scrub/redaction, delivery evidence and auditability.
4. **Vendor / Article 28 assessment** — clause extraction, requirement mapping, divergences, human review.
5. **International transfers** — inventory, mechanism, SCC/BCR/adequacy, transfer-impact evidence and supplementary measures.
6. **Retention/deletion governance** — purpose/data retention mappings, legal/policy basis, deletion evidence and holds.
7. **AI privacy / IAMA / FRIA coordination** — coordinate but do not conflate GDPR DPIA, AI Act and rights-assessment obligations.

## Phase 4 — DPO operating layer

After multiple workflows share the substrate:
- obligations/open-risk view;
- annual DPO reporting;
- audit programme;
- recurring legal-source freshness review;
- policy/control maturity;
- portfolio evidence;
- management actions;
- certified officer sign-off/accountability records.

## Explicitly deferred

- mass-importing prompt/skill collections;
- broad multi-jurisdiction expansion;
- autonomous final legal decisions;
- large GRC UI/platform before workflow contracts stabilise;
- website evidence collection without a consuming workflow;
- ISO normative-content replication without licensing;
- real external AI-provider enablement without verified/approved model-call policy.

## Roadmap health checks

Revisit ordering when:
- EDPB finalises the 2026 DPIA or breach template;
- the Dutch Rijksmodel/PAR model materially changes;
- a completed vertical slice exposes a missing shared prerequisite;
- Scrub changes its integration contract;
- a source/legal change invalidates an executable rule;
- provider data-handling terms change;
- another workflow has materially higher operational/regulatory value.

Every roadmap change must explain **why the dependency/order changed**, not merely rename work packages.
