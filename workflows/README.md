# Workflows

Workflows orchestrate skills, methodologies, source lookups, deterministic gates and human review into auditable end-to-end privacy processes.

Current / planned workflow directories:

- `document_to_dpia/` — first reference vertical slice;
- `engagement_onboarding_to_privacy_state/` — planned POaaS onboarding orchestrator after shared client-state primitives exist;
- `document_to_ropa/` — planned processing-inventory/RoPA backbone;
- `incident_to_breach_assessment/`;
- `vendor_documents_to_assessment/`;
- `dsar_document_review/`.

A workflow defines sequence, dependencies, evidence flow, stop conditions and human-review gates. It should consume legal rules from approved source/framework layers rather than duplicating them in workflow prompts.

Production workflows should be deterministic about required stages even when individual AI analyses are probabilistic.

A workflow run is not the durable customer record. It consumes a bounded version of isolated client state and may emit evidence-backed proposed facts, findings, actions or state changes. Material changes pass validation/human-review gates before becoming reusable organisational privacy state.

The POaaS onboarding orchestrator is intentionally an **orchestrating service flow**, not a giant prompt. It coordinates evidence intake, fact extraction, gap-driven questions, persistent client-state updates, RoPA/DPIA/baseline workflows, review and promised deliverables.

See `ROADMAP.md` for sequencing and `docs/POAAS_REFERENCE_WORKFLOW.md` for the reference medium-sized Dutch home-care onboarding flow. The roadmap requires M1 integrated DPIA acceptance first, then shared execution/client-state primitives, then the M2 POaaS onboarding slice. Broad workflow expansion follows only after those foundations are proven.
