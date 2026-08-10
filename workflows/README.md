# Workflows

Workflows orchestrate skills, methodologies, source lookups, deterministic gates and human review into auditable end-to-end privacy processes.

Current / planned workflow directories:

- `document_to_dpia/` — first reference vertical slice;
- `document_to_ropa/`;
- `incident_to_breach_assessment/`;
- `dsar_document_review/`;
- `vendor_documents_to_assessment/`.

A workflow defines sequence, dependencies, evidence flow, stop conditions and human-review gates. It should consume legal rules from approved source/framework layers rather than duplicating them in workflow prompts.

Production workflows should be deterministic about required stages even when individual AI analyses are probabilistic.

See `ROADMAP.md` for sequencing. The current expansion order after the DPIA vertical slice is RoPA → breach → DSAR, because RoPA provides reusable organisational processing state and production DSAR depends on broader operational discovery/redaction capabilities.
