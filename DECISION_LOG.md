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
Status: ACCEPTED

Decision: a POaaS customer becomes a durable versioned organisational privacy state over which multiple governed workflows operate. Workflow runs may propose reviewed state changes but do not own private copies of organisation truth.

Reason: prevents DPIA/RoPA/vendor/breach/DSAR workflow islands and creates cumulative customer knowledge.

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
