# Skill — Extract privacy facts

Status: WP4 executable detector/validator boundary.

## Purpose

Convert scrubbed/minimised source material into candidate privacy facts without turning model output into accepted truth.

```text
fact extraction request
  -> model-call privacy policy gate
  -> provider detector
  -> detector-result contract
  -> provenance validator
  -> contradiction detector
  -> evidence pack
  -> deterministic readiness
  -> human review / downstream analysis
```

Every provider call must pass `contracts/model_call_policy.schema.json`. `scrubbed=true` never means automatically safe for external egress. The WP4 boundary rejects the Scrub Key and direct identifiers from external calls and requires explicit permission for scrubbed-personal-data egress.

The detector proposes candidate facts, missing information, abstentions and support proofs. It must not invent evidence locators/quotes, self-accept/reject facts, self-declare user confirmation, self-validate provenance, verify AP-list applicability, decide final DPIA necessity or accept residual risk.

Observed/inferred candidates require an exact support proof inside registered evidence. Passing provenance validation changes only `validation_status`; it is not factual/legal approval. Conflicts remain explicit contradictions.

CI uses a deterministic fixture provider with no network access. Production-provider enablement is separate and requires an approved model-call policy first.
