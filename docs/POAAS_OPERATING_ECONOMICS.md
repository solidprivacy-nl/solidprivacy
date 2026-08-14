# SolidPrivacy POaaS Operating Economics

Status: measurement framework; no commercial pricing claim is proven until production-like evidence exists.

## Purpose

SolidPrivacy's potential market advantage depends on producing reliable privacy outcomes with materially less human professional time while preserving or improving evidence quality, traceability and accountability.

The architecture must therefore measure unit economics as a first-class operational property rather than assuming that AI is cheaper.

## Governing rule

> Optimise human effort only after required legal, privacy, assurance and human-review gates are satisfied. Efficiency metrics may never be used to suppress mandatory review or lower an evidence threshold.

## Primary metric: HMPO

**Human Minutes per Privacy Outcome (HMPO)** measures qualified/operator human time required to reach one defined accepted outcome.

Example outcome types:

- one accepted processing-activity record;
- one completed DPIA pre-scan;
- one reviewed DPIA;
- one reviewed Article 28/vendor assessment;
- one resolved material contradiction;
- one completed customer onboarding deliverable;
- one closed remediation action.

HMPO must distinguish role classes where useful:

```text
operator_minutes
qualified_privacy_officer_minutes
independent_fg_dpo_minutes
client_minutes
```

A low HMPO is useful only when the outcome passed the same required quality/assurance gates.

## Secondary metrics

Track at least:

- **cycle time per outcome** — wall-clock elapsed time including waiting states;
- **active human touch time** — total human effort by role;
- **automation share** — deterministic/AI stages completed without human intervention;
- **first-pass review acceptance** — proportion accepted without substantive rework;
- **rework rate** — outcomes requiring correction after review/assurance;
- **evidence completeness** — required evidence present/validated;
- **blocked/waiting-client rate** — distinguishes automation failure from missing customer input;
- **cost per accepted outcome** — provider/compute + allocated human cost + operational overhead where available;
- **model/provider cost per run/outcome**;
- **exception rate** — percentage requiring senior judgement or specialist escalation;
- **quality escape rate** — issues discovered after formal approval/delivery;
- **state reuse ratio** — amount of accepted client state reused rather than re-collected across workflows.

## Measurement architecture

The workflow execution/audit layer should emit timing/resource events without logging unnecessary customer content.

Example event classes:

```text
run_started
stage_started
stage_completed
human_review_started
human_review_completed
client_wait_started
client_wait_completed
model_call_completed
validation_completed
state_change_approved
deliverable_approved
run_completed
```

Each can record timestamps, role, stage/outcome type, model/provider usage and cost metadata without copying document bodies into telemetry.

## M1 requirement

M1 should establish the measurement primitives on the integrated DPIA chain even if the synthetic sample is too small for commercial conclusions.

Report:

- total human interventions;
- human minutes by role where measurable;
- model/compute usage;
- stage cycle times;
- blocked/adversarial path behaviour;
- rework/validation events.

## M2 requirement

M2 should produce a complete synthetic POaaS onboarding economics report for the medium-sized Dutch home-care reference customer.

At minimum:

- HMPO for a processing-activity record;
- HMPO for a DPIA screen;
- HMPO for reviewed onboarding deliverables;
- total onboarding human touch time;
- qualified Privacy Officer share versus lower-cost operator work;
- model/compute cost;
- cycle time and client-wait time;
- number of facts/evidence items reused across deliverables;
- number of manual duplicate-entry steps avoided;
- first-pass/rework/exception rates.

No target reduction percentage is hard-coded before this baseline exists.

## Commercial interpretation

SolidPrivacy should not optimise for 'cheapest consultant'. The target is **privacy assurance per euro**: materially lower cost and faster cycle time while maintaining stronger evidence lineage, source governance, repeatability and human accountability.

The potential moat is not the underlying LLM. It is the combination of:

- canonical privacy state;
- governed legal sources;
- evidence provenance;
- deterministic workflow/validation gates;
- reusable client state;
- human decision records;
- regression/evaluation corpus;
- operational performance data over repeated cases.

## Anti-gaming rules

Metrics must not improve by:

- skipping required human review;
- silently downgrading missing evidence;
- using model confidence as legal truth;
- combining multiple outcomes into one denominator without explanation;
- excluding failed/blocked/rework cases from the operational dataset;
- shifting effort to the customer without tracking client minutes/wait states;
- treating generated but unapproved output as a completed outcome.

Only **accepted/approved outcomes** count as completed for primary unit-economics reporting.
