# SolidPrivacy Decision Log

This log records durable product/architecture/governance decisions and the rationale needed to prevent future drift. It does not duplicate transient implementation status.

## D-001 — SolidPrivacy is a privacy operating layer, not a prompt collection

Date: 2026-08-10  
Status: ACCEPTED

Decision: separate canonical privacy semantics, jurisdiction/legal authority, methodologies, controls/evidence, workflows, execution contracts, evaluations and provenance. Third-party prompt/skill repositories are donor material only.

Reason: privacy/legal assertions must remain source-governed, testable and auditable rather than hidden in prompts/model weights.

## D-002 — One canonical processing model is reused across workflows

Date: 2026-08-10  
Status: ACCEPTED

Decision: DPIA, RoPA, vendor, breach, retention and DSAR share canonical organisation/processing concepts rather than maintaining workflow-private customer truth.

Reason: reduces duplicate collection, contradictory reports and manual reconciliation.

## D-003 — Evidence precedes reasoning; provenance validation is not human acceptance

Date: 2026-08-10  
Status: ACCEPTED

Decision: AI may propose observed/inferred facts only with evidence/support proof. Contradictions/missing information remain explicit. Provenance-valid does not mean a qualified human has accepted a material fact.

Reason: separates traceability from truth/accountability.

## D-004 — Model call requires explicit privacy/egress policy

Date: 2026-08-10  
Status: ACCEPTED

Decision: provider/model/content class/egress/training/retention/logging posture must be explicit before an external model call. Direct identifiers and the Scrub Key are blocked from the external workflow boundary by default.

Reason: a model interface is not authorization to disclose client content.

## D-005 — Governed legal context is resolved before legal analysis

Date: 2026-08-10  
Status: ACCEPTED

Decision: the runtime deterministically resolves approved source-bound legal rules before AI analysis. Models cannot declare guidance/law authority from their own weights.

Reason: prevents jurisdiction/source hallucination and guidance-to-law promotion.

## D-006 — Material final conclusions remain human-accountable

Date: 2026-08-10  
Status: ACCEPTED

Decision: final residual risk, prior consultation and comparable high-impact decisions require designated human review. AI/provider output cannot self-approve.

Reason: accountability and legal/professional judgement cannot be delegated to probabilistic generation.

## D-007 — Workflow runs are temporary; client privacy state is durable

Date: 2026-08-11  
Status: ACCEPTED, QUALIFIED BY D-025

Decision: a POaaS customer becomes a durable versioned organisational privacy state over which multiple governed workflows operate. Workflow runs may propose reviewed state changes but do not own private copies of organisation truth.

Reason: prevents DPIA/RoPA/vendor/breach/DSAR workflow islands and creates cumulative customer knowledge.

Qualification: D-025 clarifies that this durable organisation-state rule applies only where the engagement authorises organisation-scoped persistence. A bounded project may instead retain only engagement-scoped state.

## D-008 — Documents are evidence/projections, not independent sources of operational truth

Date: 2026-08-11  
Status: ACCEPTED

Decision: incoming documents are evidence sources. Accepted structured client state is operational truth. RoPA/DPIA/management reports and similar files are versioned projections with lineage to state/evidence/review versions.

Reason: a change to one processor/system/fact must propagate through dependencies rather than require manual editing of multiple unrelated documents.

## D-009 — Real client data lives in a separate private Client Data Plane

Date: 2026-08-11  
Status: ACCEPTED

Decision: `solidprivacy-nl/solidprivacy` never becomes a customer dossier store. Real evidence, client state, retrieval indexes, generated customer artefacts and operational audit belong in a private controlled Client Data Plane.

Reason: code/product governance and customer-data residency/security have different access, retention, legal and operational requirements.

## D-010 — Initial healthcare production isolation is dedicated-per-client

Date: 2026-08-11  
Status: ACCEPTED AS INITIAL ARCHITECTURE POSTURE

Decision: for the first production cohort, especially healthcare, prefer one dedicated EU/EEA client data project/account per client with separate database/storage/retrieval/key scope. Pooled multi-tenancy is deferred until explicit machine-tested tenant isolation assurance exists.

Reason: maximises auditability and trust while the product/security model is young; reduces the blast radius and complexity of proving cross-tenant isolation. This is an implementation posture, not an eternal prohibition on pooled tenancy.

## D-011 — AI receives bounded tenant-scoped context; it is not the dossier store

Date: 2026-08-11  
Status: ACCEPTED

Decision: models/providers do not receive persistent database credentials or unrestricted dossier access. The SolidPrivacy runtime retrieves/minimises tenant-scoped context for one governed task, validates the result and persists approved structured outcomes/audit in the client data plane. Cross-client model memory is prohibited.

Reason: reading data for a task must not imply indefinite provider/model possession or hidden memory.

## D-012 — Retrieval indexes are customer data and are tenant-bound before ranking

Date: 2026-08-11  
Status: ACCEPTED

Decision: embeddings/chunks inherit customer classification, remain linked to source/version, and may not share a global cross-client customer index. Tenant filtering occurs before retrieval/ranking, not as a post-filter.

Reason: embeddings can leak/source customer information and cross-tenant retrieval is an unacceptable isolation failure.

## D-013 — M1 precedes platform generalisation; Client Data Plane precedes real client state

Date: 2026-08-11  
Status: ACCEPTED

Decision: first prove the full DPIA chain as one correlated execution (M1). Then generalise workflow/audit. Implement/assure the Client Data Plane before durable real customer state/engagement becomes production-enabled.

Reason: shared abstractions should be extracted from proven workflow needs, but real customer records cannot be introduced before their security/storage boundary exists.

## D-014 — M2 proves a sellable POaaS onboarding slice before broad workflow expansion

Date: 2026-08-11  
Status: ACCEPTED

Decision: one synthetic medium-sized Dutch home-care organisation must pass engagement → evidence → questions → client state → RoPA/DPIA screening → baseline/actions → PO review → deliverables/audit before breach/vendor/DSAR breadth accelerates.

Reason: validates that multiple capabilities operate over one durable customer state instead of becoming independent agents.

## D-015 — Unit economics are measured, not assumed

Date: 2026-08-11  
Status: ACCEPTED

Decision: instrument Human Minutes per Privacy Outcome (HMPO), role-specific human time, cycle time, rework, model/compute cost, evidence completeness and state reuse. No commercial automation reduction claim is treated as proven before M1/M2 measurement.

Reason: disruptive pricing depends on real delivery economics. Metrics may never improve by skipping mandatory review/evidence gates.

## D-016 — GitHub/project repo is the project source of truth; control-plane owns shared governance doctrine

Date: 2026-08-11  
Status: ACCEPTED

Decision: adopt the canonical `market-predictions/control-plane` operating method. The central control-plane owns shared governance standards; `solidprivacy-nl/solidprivacy` remains authoritative for its roadmap, current state, workpackages, claims, decisions, architecture, tests, release evidence and handovers.

Reason: prevents chat-memory drift and avoids copying/forking cross-project governance doctrine into each repository.

## D-017 — Consequential implementation and release assurance remain separate roles

Date: 2026-08-11  
Status: ACCEPTED

Decision: `implementation_operations` prepares candidates; `governance_release_assurance` independently reconstructs and issues `PASS | FAIL | INDETERMINATE`. Assurance does not silently repair the candidate it certifies.

Reason: self-certification creates confirmation bias and makes completion claims non-independent.

## D-018 — Active work requires work-claim/branch lifecycle reconciliation

Date: 2026-08-11  
Status: ACCEPTED

Decision: consequential active work is backed by a machine-readable claim and reconciled against live branch/PR/dependency state under `WORK_CLAIM_AND_BRANCH_LIFECYCLE_STANDARD_V1`. Materially stale integration lines stop accumulating and must be reconciled or superseded with explicit handover.

Reason: closes the gap between roadmap intentions and actual branches/PRs, and prevents orphaned/stale work from remaining implicitly authoritative.

## D-019 — Project status is machine-first and freshness-bound

Date: 2026-08-11  
Status: ACCEPTED

Decision: `control/PROJECT_STATE.json` is the machine-readable SolidPrivacy coordination state. `CURRENT_STATE.md` is a human-readable projection/context view. Live GitHub is reconstructed at mandatory gates; central Control is a freshness-bound coordination cache, not project-specific authority.

Reason: prevents duplicated narrative status from becoming stale truth and aligns SolidPrivacy with `CONTROL_STATE_FRESHNESS_STANDARD_V1`.

## D-020 — Scope is explicitly protected as CURRENT_RELEASE / NEXT_RELEASE / PARKING_LOT

Date: 2026-08-11  
Status: ACCEPTED

Decision: newly discovered improvements are classified rather than silently entering the active release. Only work required for the stated outcome, safety/correctness or explicit reprioritisation interrupts the primary objective.

Reason: preserves vertical-slice completion and prevents architecture discovery from indefinitely delaying M1.

## D-021 — Project-control decisions and privacy/legal decisions are different decision planes

Date: 2026-08-11  
Status: ACCEPTED

Decision: Control D0–D3 classes apply only to project/development decisions. Runtime privacy/legal conclusions remain governed by evidence, validators and accountable Privacy Officer/DPO/FG/legal review contracts.

Reason: avoids a category error in which project autonomy accidentally bypasses legal/professional accountability.

## D-022 — Candidate identity is distinct from live branch head and administrative descendants

Date: 2026-08-11  
Status: ACCEPTED

Decision: distinguish `implementation_candidate_sha`, live branch head and later administrative descendant commits. Exact-head product evidence binds to the candidate it actually tested; later claim/handover metadata cannot retroactively extend that evidence.

Reason: eliminates ambiguity created when handover/state commits are added after an implementation candidate has already been tested.

## D-023 — M1 remains the next product gate after governance alignment

Date: 2026-08-11  
Status: ACCEPTED

Decision: the Control freshness/project-state refinement is part of PR #8 closeout and does not create a new product milestone before M1.

Reason: governance must reduce drift and span of control without becoming scope creep that blocks execution of the already selected next vertical-slice gate.

## D-024 — PROJECT and MANAGED_SERVICE are first-class engagement modes over one governed engine

Date: 2026-08-14  
Status: ACCEPTED

Decision: SolidPrivacy supports at least `PROJECT` and `MANAGED_SERVICE` as engagement modes. Engagement mode is separate from workflow/service type. A standalone DPIA and a DPIA performed inside POaaS must use the same DPIA methodology, legal-source, evidence/provenance, validation and human-review contracts for equivalent facts.

Reason: enables bounded professional-service work without duplicating legal logic or allowing standalone and managed-service implementations to drift apart.

## D-025 — Client state has run, engagement and organisation scopes; promotion is explicit

Date: 2026-08-14  
Status: ACCEPTED

Decision: distinguish `RUN_SCOPED`, `ENGAGEMENT_SCOPED` and `ORGANISATION_SCOPED` state. A bounded project defaults to engagement-scoped accepted state. Reuse as durable organisation-scoped managed state requires an explicit governed promotion preserving provenance, review lineage, scope limitations, effective dates and retention authority.

Reason: a one-off DPIA must not silently create or maintain an organisation-wide privacy dossier, while useful reviewed knowledge can still be reused when the client and service scope authorise it.

## D-026 — Retention, closeout and change propagation are engagement-aware

Date: 2026-08-14  
Status: ACCEPTED

Decision: every engagement must define persistence/retention/closeout semantics. `MANAGED_SERVICE` may maintain dependency-driven reassessment according to contracted scope; a closed `PROJECT` has no implicit continuing monitoring obligation. Post-completion data outcomes are explicit per data class, including delete, bounded retention, restricted archive, legal hold, return/export or authorised promotion.

Reason: possession of historical project data must not be confused with an ongoing service obligation or permission to retain/monitor indefinitely.

## D-027 — M1 proves standalone PROJECT + DPIA; generalized production engagement remains WP9

Date: 2026-08-14  
Status: ACCEPTED

Decision: M1 remains the next product gate and is interpreted as the first complete standalone professional-service execution: a synthetic `PROJECT + DPIA` from bounded engagement scope through reviewed deliverable, audit and explicit closeout/retention disposition. M1 uses only a minimal synthetic engagement envelope. Generalized real-client organisation/engagement contracts remain sequenced for WP9 after independent assurance of the WP8 Client Data Plane.

Reason: proves a commercially usable bounded service flow early without bypassing the security/data-plane dependency or prematurely generalising a platform contract before the DPIA vertical slice is proven.
