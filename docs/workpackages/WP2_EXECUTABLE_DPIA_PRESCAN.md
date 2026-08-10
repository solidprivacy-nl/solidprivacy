# WP2 — Executable DPIA Contract + Pre-scan Decision Engine

## Objective

Turn the WP1 canonical DPIA model into an executable release gate and implement a deterministic Dutch pre-scan decision engine before any production AI authoring layer is introduced.

## Scope delivered

- Python runtime with no application framework;
- JSON Schema 2020-12 validation with local `$ref` resolution;
- referential-integrity validation for canonical DPIA objects;
- global uniqueness for canonical IDs used by cross-object references;
- safety invariants for unresolved high residual risk;
- deterministic Rijksmodel pre-scan 2.0 methodology calculation;
- separate legal decision gate using approved legal-source classes;
- synthetic pre-scan regression cases;
- command-line interface;
- GitHub Actions release gate.

## Separation of methodology and law

The Dutch Government pre-scan is an official methodology. Its output must not automatically be treated as a binding legal conclusion.

The runtime therefore emits two results:

1. `methodology.level` — parity-oriented interpretation of the pinned Rijksmodel pre-scan;
2. `legal.decision` — conservative SolidPrivacy legal gate.

The legal gate can emit:

- `DPIA_REQUIRED`
- `DPIA_RECOMMENDED`
- `DPIA_NOT_INDICATED`
- `NEEDS_REVIEW`

A direct `DPIA_REQUIRED` conclusion is limited to recorded direct Article 35(3) triggers, an applicable law/regulation explicitly requiring a DPIA, or a verified match with the Dutch AP mandatory list.

For the AP list, `verified` means that the complete factual conditions of the relevant listed processing type have been assessed. A category-name or keyword match alone is insufficient.

The EDPB two-criteria pattern remains regulator guidance. It creates a strong DPIA recommendation and human-review gate rather than being silently reclassified as binding law.

## Rijksmodel parity

Pinned source:

- repository: `MinBZK/par-dpia-form`
- commit: `d8d690989da03287b8879ba1319f78ca8a404bd5`
- pre-scan version: `2.0`
- source: `sources/prescan.yaml`

The methodology engine implements the DPIA assessment-level rules recorded in that source:

- new legislation scope;
- aggregate methodology risk score greater than four;
- one or more AP-list selections;
- two or more EDPB criteria;
- one EDPB criterion as recommendation.

The risk-score components are represented deterministically in code and covered by regression tests. A known upstream `0.4.1` reference anomaly in the international-transfer score is documented in `methodologies/nl_rijksmodel_dpia/KNOWN_UPSTREAM_ANOMALIES.md`; SolidPrivacy uses a transparent normalized interpretation rather than silently reproducing an unresolved source-reference defect.

## Integrity gates

The runtime rejects unresolved or ambiguous references between:

- personal data and data subjects;
- retention entries and purposes/data subjects/personal data;
- risks and processing activities/data subjects;
- measures and risks/evidence;
- special-data assessments and canonical entities;
- purpose-compatibility entries and processing activities.

IDs used across canonical processing activities (`DS-*`, `PD-*`, `PUR-*`, `PTY-*`) must be globally unique so DPIA-wide references cannot resolve ambiguously.

Additional safety invariant:

- a DPIA with `high` residual risk cannot record prior consultation as definitively false;
- high residual risk requires human review;
- high residual risk cannot be represented as already approved by the runtime contract gate.

## CLI

```bash
solidprivacy validate-dpia evals/synthetic_cases/dpia_nl_basic.json
solidprivacy validate-dpia evals/synthetic_cases/dpia_nl_high_risk.json
solidprivacy prescan evals/prescan_smoke_input.json
```

## Release gate

`.github/workflows/wp2-contract-gate.yml` runs:

1. package installation;
2. deterministic pytest suite;
3. both WP1 canonical DPIA fixtures through JSON Schema + integrity validation;
4. representative pre-scan decision through the CLI.

## Acceptance criteria

WP2 is complete when:

- all contract schemas pass JSON Schema meta-validation;
- the two WP1 synthetic DPIAs pass executable validation;
- intentionally broken and ambiguous references fail;
- all pre-scan regression cases produce the expected methodology and legal outcomes;
- high-residual-risk safety invariants are enforced;
- methodology-source IDs resolve to registered governed sources;
- GitHub Actions is green on the exact PR head.

## Explicit non-goals

WP2 does not:

- generate DPIA prose with AI;
- determine uncertain facts such as whether processing is actually “large scale”;
- autonomously decide that an organisation fits an AP-list category without a verified input;
- replace DPO/privacy-officer review;
- vendor the BZK questionnaire or application code.

## Next work package

After WP2 passes, WP3 may implement the first AI-assisted DPIA authoring/review skill. That layer must consume these validated canonical objects and may not bypass the deterministic gates.
