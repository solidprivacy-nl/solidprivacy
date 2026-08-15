# Skill — Extract privacy facts

Status: contract boundary for WP3; executable AI implementation belongs to WP4.

## Purpose

Convert scrubbed/minimised source material into **candidate privacy facts** without turning model output into accepted truth.

## Input

Use `contracts/skill_input.schema.json`. Expected production input is normally scrubbed document or mixed scrubbed/structured questionnaire material with evidence identifiers and locators, jurisdiction and explicit privacy constraints.

## Output boundary

The extractor proposes objects conforming to `contracts/privacy_fact.schema.json` inside an `contracts/evidence_pack.schema.json` evidence pack.

The extractor must attach evidence IDs to observed/inferred/user-confirmed facts, label inference separately from observation, label assumptions explicitly, provide a concise basis summary for inferred facts, preserve contradictory candidates, emit missing-information items and abstain rather than invent canonical values.

## Prohibited behaviour

The skill must not invent evidence locators or quotations, treat an assumption as observed, infer a legal requirement merely from a methodology field, verify a Dutch AP mandatory-DPIA list condition from keyword similarity, decide final DPIA necessity, accept residual risk, or erase conflicting facts.

## Detector → validator

WP4 must implement extraction as two separate stages:

1. **detector** — high-recall candidate facts and gaps;
2. **validator** — challenge provenance, contradiction, canonical mapping and evidence support.

Only validated candidate facts may progress to DPIA analysis.
