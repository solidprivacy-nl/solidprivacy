# Document Processing Skills

Reusable, narrow skills for privacy-document handling. These skills should not embed broad legal workflows.

Planned skill directories:

- `classify_document/`
- `extract_privacy_facts/`
- `detect_sensitive_content/`
- `analyse_scrubbed_document/`
- `validate_ai_output/`

Each implemented skill should define inputs, outputs, evidence requirements, failure modes, source/framework dependencies, evaluation cases and human-review conditions.

Document-processing skills must assume scrubbed/minimised inputs where feasible and must not create a second uncontrolled anonymisation engine inside this repository.
