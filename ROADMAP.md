# SolidPrivacy Roadmap

Status date: 2026-08-10

When workflow ordering in older architecture text conflicts with this file, **this roadmap is authoritative for sequencing**. Architecture layer responsibilities remain authoritative in `docs/architecture.md`.

## Product objective

Build SolidPrivacy into a controlled Privacy Officer operating system for EU/EEA + Netherlands: AI performs high-volume analysis and drafting over scrubbed/minimised information, while deterministic contracts, authoritative sources, evidence provenance and qualified human review control material privacy conclusions.

The roadmap is intentionally **capability-first**, not prompt-count-first. A new workflow is production-oriented only when its facts, legal sources, deterministic gates, evaluations and review path are explicit.

## Roadmap principles

1. **Evidence before reasoning.** AI-generated findings must trace to evidence or be labelled inference/assumption.
2. **Methodology is not law.** Government/regulator assessment methods never silently become binding legal requirements.
3. **Deterministic gates before generative layers.** Schema, integrity, source and high-impact decision gates run before AI authoring.
4. **One canonical processing model.** DPIA, RoPA, breach, vendor and DSAR workflows should reuse shared processing concepts.
5. **Human accountability at material decisions.** AI may prepare; designated privacy professionals approve or reject.
6. **Scrub is the privacy boundary.** Sensitive originals and the Scrub Key remain outside cloud AI workflows by default.
7. **Vertical slices before breadth.** Complete one trustworthy workflow before importing dozens of partial skills.
8. **Exact-head assurance.** Production-capability work packages require executable regression evidence on the exact reviewed commit.

## Phase 0 — Operating architecture

Status: COMPLETE IN DRAFT STACK

- WP0 / PR #1 — privacy operating architecture, source governance, provenance, contracts, methodology/vocabulary/control/evidence layers.
- Gate: architecture is explicit and third-party material is not treated as legal authority.

## Phase 1 — DPIA vertical slice

The DPIA is the first reference workflow because it exercises the full architecture: facts, methodology, legal sources, risk, controls, evidence, human advice and report generation.

### WP1 — Canonical privacy + Dutch DPIA model

Status: COMPLETE, draft PR #2

- reusable processing-activity model;
- canonical DPIA model;
- Dutch Rijksmodel adapter;
- DPV mapping;
- synthetic positive/high-risk cases.

### WP2 — Executable DPIA contracts + pre-scan

Status: COMPLETE, draft PR #3, exact-head CI green

- executable JSON Schema and referential-integrity gates;
- deterministic Dutch pre-scan methodology;
- legal decision gate separated from methodology;
- source-governed AP/EDPB handling;
- regression matrix and GitHub Actions.

### WP3 — Evidence and fact provenance layer

Status: IN PROGRESS

Goal: make evidence-backed facts, uncertainty, contradictions and missing information first-class before any AI drafting.

Deliverables:
- privacy-fact contract;
- evidence-pack contract;
- deterministic provenance/integrity gate;
- deterministic analysis/finalisation readiness gate;
- synthetic ready and blocked evidence packs;
- fact-extraction skill boundary;
- document-to-DPIA workflow stage model;
- exact-head CI.

### WP4 — AI fact extraction + validator

Status: PLANNED

Goal: convert scrubbed documents/questionnaire material into candidate canonical facts without allowing unsupported facts to pass silently.

Required:
- model/provider-independent extraction interface;
- evidence locators for every observed/inferred fact;
- detector -> validator architecture;
- contradiction detection;
- confidence calibration;
- abstention/missing-information behaviour;
- adversarial/near-miss evaluations;
- no autonomous legal conclusion.

### WP5 — AI-assisted DPIA analysis and drafting

Status: PLANNED

Goal: turn a validated evidence pack into structured DPIA analysis and draft narrative.

Required:
- consume only validated canonical facts + approved sources;
- section-level source/evidence traceability;
- explicit assumptions and open questions;
- legal-claim classification;
- risk/measure linkage;
- no final residual-risk acceptance;
- validator pass after generation;
- legal-accuracy and omission evals.

### WP6 — Privacy Officer review package + report/reinsert boundary

Status: PLANNED

Goal: make DPIA output operationally usable by a certified Privacy Officer and compatible with Scrub.

Required:
- review diff: AI proposal vs accepted version;
- unresolved issue queue;
- approve/reject/change workflow;
- source/evidence appendix;
- management summary and full report;
- scrubbed output contract;
- controlled reinsertion handoff;
- immutable execution/audit record.

**DPIA capability milestone:** after WP6, validate the full scrubbed-document → evidence → facts → pre-scan → DPIA → human review → report chain on a representative synthetic corpus.

## Phase 2 — Shared operating substrate

Do not build each later privacy workflow as a bespoke agent. Extract reusable runtime capabilities from the DPIA vertical slice.

### WP7 — Workflow execution and audit model

- workflow/run IDs and versioning;
- step status and replayability;
- input/output hashes;
- source/model/prompt versions;
- human decisions;
- immutable audit events;
- failure/abstention states.

### WP8 — Control/evidence/remediation model

- executable OSCAL-inspired control objects;
- implementation/evidence/finding/remediation linkage;
- reusable measures library without copying licensed normative text;
- owner, due date, status and verification evidence.

### WP9 — Model gateway and privacy policy

- model/provider abstraction;
- data-classification policy controlling which model may receive which content;
- local vs external inference policy;
- prompt/version registry;
- deterministic redaction/scrub precondition;
- telemetry without leaking personal data.

## Phase 3 — Expand Privacy Officer workflows

Order revised on 2026-08-10.

### 1. RoPA / processing inventory

Priority: HIGH

Reason for moving before DSAR: RoPA is shared organisational state. It reuses the canonical processing model and supports DPIA, retention, vendor, transfer and later DSAR scoping.

### 2. Personal-data-breach assessment

Priority: HIGH

Reason: bounded, high-value Privacy Officer workflow with clear evidence, timeline, risk and notification review gates. Human sign-off remains mandatory.

### 3. DSAR / right of access

Priority: HIGH, after RoPA + breach

Reason for moving later: production DSAR is operationally broader than a legal Q&A skill. It needs identity assurance, scope, deadline control, system/document discovery, third-party data handling, exemptions/restrictions, Scrub/redaction, delivery evidence and auditability.

### 4. Vendor / processor agreement assessment

- Article 28 requirement mapping;
- contract clause extraction;
- divergence/missing-clause analysis;
- human legal/privacy review.

### 5. International transfers

- transfer inventory;
- mechanism;
- SCC/BCR/adequacy context;
- transfer-impact evidence;
- supplementary measures;
- human approval.

### 6. Retention and deletion governance

- processing/data-purpose retention mapping;
- legal/policy basis separation;
- evidence of deletion/archiving;
- exceptions and holds.

### 7. AI privacy / fundamental-rights assessment

- coordinate DPIA, AI Act and IAMA/FRIA-style workflows without conflating their legal bases.

## Phase 4 — DPO operating layer

After several workflows share the substrate:

- obligations/open-risk dashboard;
- annual DPO reporting;
- audit programme;
- recurring source-freshness review;
- policy/control maturity;
- portfolio-level evidence;
- management actions;
- certified officer sign-off and accountability records.

## Explicitly deferred

These are useful, but should not outrank the trusted workflow core:

- mass-importing third-party prompt/skill collections;
- broad multi-jurisdiction support;
- autonomous final legal decisions;
- large GRC UI/platform build before workflow contracts stabilise;
- website evidence collection unless a concrete workflow consumes it;
- ISO normative-content replication without licensing.

## Roadmap health checks

Revisit this roadmap when any of the following becomes true:

- EDPB finalises the 2026 DPIA or breach template;
- Dutch government materially updates the Rijksmodel/PAR model;
- a completed vertical slice exposes a missing shared platform capability;
- Scrub changes its integration contract;
- source/legal changes invalidate an executable rule;
- a new workflow has materially higher user value or regulatory urgency.

Every roadmap change should explain **why the ordering changed**, not only rename work packages.
