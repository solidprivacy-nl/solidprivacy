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

## Methodology output is not a legal conclusion

Official templates, questionnaires and assessment methods can be operationally authoritative as methodologies without making every field or calculated outcome a binding legal rule.

When a workflow uses such a methodology:

1. preserve the methodology result separately;
2. identify the legal or regulator source supporting any material legal conclusion;
3. do not upgrade a methodology threshold into `LAW_REQUIRED` unless an approved legal source supports the upgrade;
4. return `NEEDS_REVIEW` when a methodology says an action is required but the legal basis for that requirement is unresolved.

The Dutch Rijksmodel pre-scan is the first production implementation of this separation.

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

## Deterministic decision gates

Legal decision engines must fail conservatively:

- a direct mandatory outcome may be emitted only when its required factual/legal trigger is explicit;
- missing context may not be coerced to `false`;
- an unverified AP-list selection may not be treated as a verified mandatory-list match;
- an AP-list verification must assess the full conditions of the listed processing type, not only a matching category label;
- regulator criteria may produce recommendations/review gates without being mislabeled as binding law;
- high-impact conclusions retain human-review metadata.

## Legal update process

When a legal source changes:

1. update `source_registry.yaml` metadata if necessary;
2. identify affected framework rules;
3. rerun legal-accuracy evaluations;
4. rerun workflow regressions;
5. version affected skills/workflows;
6. record the change and human approval before production promotion.
