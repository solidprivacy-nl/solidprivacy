# MISSION_SPP_R2_GAP_30 — governed privacy-service workflow model

## Mission binding

- Mission: `SOLID_PRIVACY_PLATFORM`
- Revision: `2026-08-16-r2`
- Criterion: `SPP-SC-30`
- Gap: `SPP-GAP-30`
- Project governance: issue #11
- Authoritative baseline: `main` at `209ae65e3c343f2783be3b7f4aad59e90ab603ac`

## Purpose

Define one reusable workflow contract for recurring Privacy Officer service and standalone privacy assignments such as DPIA without creating another orchestration plane. The workflow reuses the existing client dossier, evidence, source-reference, legal-claim and human-review contracts and remains repository/governance architecture only.

## Workflow authority

A workflow instance belongs to exactly one tenant, client, engagement and dossier. The dossier remains the case container; evidence remains separately identified by the existing evidence contract. Workflow state records coordination and review status only. It does not duplicate client truth, evidence content or legal-decision authority.

The minimum common states are:

1. `INTAKE` — scope, purpose and required inputs are identified.
2. `EVIDENCE_PENDING` — required facts or evidence are explicitly missing or requested.
3. `ANALYSIS_READY` — required inputs are present enough for bounded preparation or analysis.
4. `AI_PREPARED` — optional AI-generated preparation exists as a proposal with provenance; it is never accepted professional truth by itself.
5. `PROFESSIONAL_REVIEW` — a qualified human reviews facts, assumptions, analysis, evidence and proposed conclusions.
6. `CHANGES_REQUIRED` — reviewer-requested corrections, evidence gaps or client clarifications must be resolved before approval.
7. `APPROVED` — required human review/approval is complete for the assignment output within its authorized scope.
8. `COMPLETED` — required output, decision record, provenance and completion evidence are frozen.
9. `BLOCKED` — progress cannot continue safely because required evidence, authority or a dependency is unavailable.

Only explicit governed transitions are valid:

`INTAKE -> EVIDENCE_PENDING | ANALYSIS_READY | BLOCKED`

`EVIDENCE_PENDING -> ANALYSIS_READY | BLOCKED`

`ANALYSIS_READY -> AI_PREPARED | PROFESSIONAL_REVIEW | BLOCKED`

`AI_PREPARED -> PROFESSIONAL_REVIEW | CHANGES_REQUIRED | BLOCKED`

`PROFESSIONAL_REVIEW -> CHANGES_REQUIRED | APPROVED | BLOCKED`

`CHANGES_REQUIRED -> EVIDENCE_PENDING | ANALYSIS_READY | PROFESSIONAL_REVIEW | BLOCKED`

`APPROVED -> COMPLETED`

`BLOCKED` has no automatic successor. Re-entry requires an explicit governed event that records what blocker was resolved and by whom.

## Recurring versus standalone assignments

The same state model is used where the professional control points are the same.

A standalone assignment, such as a DPIA, has one bounded engagement and reaches `COMPLETED` when its approved output and completion evidence are frozen.

A recurring Privacy Officer service uses repeated bounded work items under one ongoing engagement. Each work item follows the same state model and may complete independently. Recurrence scheduling, service calendars and commercial cadence are outside this contract; they must not become a second workflow authority.

## Evidence and provenance

Every material workflow event must be reconstructable from stable references:

- `workflow_id` — stable workflow-instance identity;
- `dossier_id` — authoritative dossier reference;
- `evidence_ids[]` — references to existing governed evidence identities;
- `source_reference_ids[]` — authoritative source references where applicable;
- `actor_id` and `actor_role` — who performed or approved the transition;
- `occurred_at` — transition/event time;
- `from_state` and `to_state` — exact state change;
- `reason` — concise transition rationale;
- `proposal_ref` — optional AI or human draft/proposal identity;
- `review_ref` — mandatory for professional review/approval events;
- `decision_ref` — mandatory where a material professional conclusion is approved;
- `completion_evidence_ids[]` — mandatory before `COMPLETED`.

Missing or conflicting required evidence is never silently normalized into success. The workflow remains `EVIDENCE_PENDING`, `CHANGES_REQUIRED` or `BLOCKED` until the gap is explicitly resolved.

## AI preparation boundary

AI may prepare bounded drafts, classifications, summaries, evidence mappings, questions and analysis proposals only when their input lineage is retained. Every AI-prepared artifact must remain distinguishable from facts, source material, reviewer findings and approved professional decisions.

AI must not:

- self-approve its output;
- issue a final legal, privacy, compliance or risk-acceptance decision;
- manufacture missing evidence or source authority;
- bypass a mandatory human review gate;
- turn a workflow transition into client-facing production or delivery authority.

## Human professional review and approval

`PROFESSIONAL_REVIEW` is mandatory before any material legal/privacy conclusion can reach `APPROVED`.

The reviewer must be able to identify:

- evidence and authoritative sources considered;
- material facts and unresolved assumptions;
- AI-prepared or human-drafted analysis inspected;
- requested changes or residual limitations;
- the exact conclusion or output being approved;
- reviewer identity and approval timestamp.

Approval is scoped to the exact reviewed artifact/version. Any material content change after approval returns the work item to `PROFESSIONAL_REVIEW` or `CHANGES_REQUIRED`.

## Handover model

A handover is an auditable workflow event, not a second task system. It records the current state, responsible role, required next action, unresolved blockers and exact dossier/evidence/proposal/review references.

Permitted handover targets include another internal professional role or a client request for facts, evidence, confirmation or an explicit decision. A handover never transfers authority beyond the receiving role's existing governed permissions.

## Completion gate

`COMPLETED` is permitted only when all of the following are true:

1. the output scope is explicit;
2. required evidence/source references are present and non-conflicting or limitations are explicitly recorded;
3. every mandatory professional review is complete;
4. the exact approved output/version is identifiable;
5. material decisions have reviewer/decision records where required;
6. completion evidence is frozen and auditable;
7. no unresolved blocker remains;
8. no production, client-delivery or autonomous legal-decision authority is inferred from completion.

## Reuse and non-duplication

Implementations should extend or reference existing contracts instead of introducing parallel truth:

- `contracts/client_dossier.schema.json` for tenant/client/engagement/dossier identity;
- `contracts/evidence.schema.json` for evidence identity;
- `contracts/source_reference.schema.json` for source provenance;
- `contracts/legal_claim.schema.json` for legal-claim representation;
- `contracts/human_review.schema.json` for human review records.

A later executable schema may encode this workflow if needed, but this gap does not justify a new scheduler, queue, mission pump, workflow engine or database.

## Explicit non-authority

This contract does not authorize:

- processing or importing real client data;
- production deployment;
- sending client deliverables;
- autonomous final legal, privacy, compliance or risk decisions;
- release authority;
- a second queue, scheduler, workflow engine or orchestration plane.

## Acceptance mapping

SPP-GAP-30 is satisfied by this candidate when independent exact-head assurance confirms that:

1. recurring and standalone assignments share one coherent bounded state model where their control points match;
2. AI preparation and human professional review/approval responsibilities are explicit and fail closed;
3. evidence lineage, handovers and completion gates are deterministic and auditable;
4. existing dossier/evidence/review contracts are reused rather than duplicated;
5. no autonomous final legal decision, production/client-delivery authority or second orchestration plane is introduced.
