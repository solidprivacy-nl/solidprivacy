# Workflows

Workflows orchestrate multiple skills and framework lookups into auditable end-to-end privacy processes.

Planned workflow directories:

- `document_to_dpia/`
- `document_to_ropa/`
- `vendor_documents_to_assessment/`
- `incident_to_breach_assessment/`
- `dsar_document_review/`

A workflow defines sequence, dependencies, evidence flow, stop conditions and human-review gates. It should consume legal rules from `frameworks/` rather than duplicating them in workflow prompts.

Production workflows should be deterministic about required stages even when individual AI analyses are probabilistic.
