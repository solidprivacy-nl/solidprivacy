# Evaluations

Evaluations are a first-class release gate for SolidPrivacy AI workflows.

Planned evaluation areas:

- `synthetic_cases/` — privacy-safe representative cases without real personal data;
- `assertions/` — machine-checkable expected properties and required omissions;
- `regression/` — tests protecting previously verified behaviour;
- `legal_accuracy/` — tests that verify material legal claims, classifications and citations against approved sources.

Evaluation suites should test not only whether an answer contains expected content, but also whether the system:

- distinguishes law from guidance, policy and best practice;
- exposes missing information;
- avoids unsupported legal certainty;
- invokes human review when required;
- preserves evidence traceability;
- avoids leaking unnecessary personal data;
- remains stable across model or prompt changes.

Only synthetic or otherwise approved test data belongs in this repository.
