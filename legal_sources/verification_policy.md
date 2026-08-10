# Legal Source Verification Policy

## Principle

SolidPrivacy workflows may use third-party skills, model knowledge and practitioner material to discover issues, but those materials are not the authoritative source for material legal conclusions.

## Source hierarchy

For legal or regulatory claims, prefer in this order where applicable:

1. binding legislation and official consolidated legal text;
2. judgments and official decisions;
3. competent supervisory-authority or regulator guidance;
4. official standards documentation where SolidPrivacy has lawful access;
5. reputable secondary commentary for interpretation and discovery only;
6. third-party AI skills/prompts as workflow inspiration only.

## Required claim metadata

A material legal claim must record:

- claim classification;
- jurisdiction;
- authority;
- source identifier;
- citation or locator where available;
- verification timestamp;
- effective date where material.

Use `contracts/legal_claim.schema.json`.

## Freshness

Time-sensitive rules must be reverified before a workflow version is promoted to production. A skill must not rely on an upstream repository's publication date as proof that the underlying law is current.

## Conflicts

If sources conflict, are ambiguous, or do not support the proposed conclusion, the workflow must:

1. preserve the conflict as evidence;
2. lower confidence;
3. mark missing/uncertain information;
4. require human review where the conclusion is material.

## Jurisdiction

Never silently transfer a rule from one jurisdiction to another. UK GDPR, EU GDPR, national implementation law, sector-specific law and organisational policy must remain distinguishable.

## Standards

Standards such as ISO/IEC 27701 may be copyrighted/licensed. This repository should record mappings and implementation metadata without copying normative standard text unless licensing explicitly permits it.

## Legal update process

When a legal source changes:

1. update `source_registry.yaml` metadata if necessary;
2. identify affected framework rules;
3. rerun legal-accuracy evaluations;
4. rerun workflow regressions;
5. version affected skills/workflows;
6. record the change and human approval before production promotion.
