# Evidence Collectors

Evidence collectors are bounded tools that produce reproducible observations for privacy workflows.

Collectors do **not** make final legal decisions. They provide typed evidence for later validation and human review.

Potential collector families:

- website cookies, trackers, storage and third-party requests;
- document metadata and hidden-content inspection;
- repository/code privacy-flow analysis;
- structured questionnaire ingestion;
- configuration/control-state inspection.

## Requirements

Every collector must document:

- scope and exclusions;
- data touched and whether personal data may be present;
- local/cloud execution characteristics;
- output schema;
- reproducibility information;
- false-positive/false-negative limitations;
- evidence hashes or stable locators where practical.

Sensitive evidence should remain local unless an explicitly approved architecture permits otherwise.
