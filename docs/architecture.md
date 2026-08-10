# SolidPrivacy AI Workflow Architecture

## Purpose

This repository is the controlled AI workflow and privacy-officer automation layer for SolidPrivacy. It is intentionally **not** a dump of third-party prompt/skill repositories.

The design separates:

1. reusable task skills;
2. legal and management-system framework knowledge;
3. end-to-end workflows;
4. machine-readable contracts;
5. evaluation and regression evidence;
6. authoritative legal-source governance; and
7. provenance and licensing.

The architectural goal is to make privacy automation testable, auditable, updateable, and safe to combine with SolidPrivacy Scrub.

## Target repository structure

```text
solidprivacy/
├── skills/
│   ├── document_processing/
│   │   ├── classify_document/
│   │   ├── extract_privacy_facts/
│   │   ├── detect_sensitive_content/
│   │   ├── analyse_scrubbed_document/
│   │   └── validate_ai_output/
│   └── privacy_officer/
│       ├── dsar/
│       ├── dpia/
│       ├── ropa/
│       ├── breach_assessment/
│       ├── retention/
│       ├── vendor_assessment/
│       ├── international_transfers/
│       └── ai_privacy_assessment/
├── frameworks/
│   ├── gdpr/
│   ├── iso27701/
│   └── eu_ai_act/
├── workflows/
│   ├── document_to_dpia/
│   ├── document_to_ropa/
│   ├── vendor_documents_to_assessment/
│   ├── incident_to_breach_assessment/
│   └── dsar_document_review/
├── contracts/
│   ├── skill_input.schema.json
│   ├── skill_output.schema.json
│   ├── evidence.schema.json
│   ├── legal_claim.schema.json
│   └── human_review.schema.json
├── evals/
│   ├── synthetic_cases/
│   ├── assertions/
│   ├── regression/
│   └── legal_accuracy/
├── legal_sources/
│   ├── source_registry.yaml
│   └── verification_policy.md
├── provenance/
│   ├── upstream_manifest.yaml
│   └── THIRD_PARTY_NOTICES.md
└── docs/
    └── architecture.md
```

## Core design decision: framework knowledge is separate from workflows

A workflow defines **what happens and in which order**. A framework defines **which legal or governance rules apply**.

For example, a DSAR workflow may orchestrate intake, identity checks, scope determination, search, exemptions, compilation, quality assurance, response and closure. It must not hard-code every GDPR rule in its own prompt. Instead, it consumes current rules from the GDPR framework layer and records which version/source supported each legal conclusion.

This avoids duplicating stale law across many skills and makes legal updates centrally maintainable.

## Common execution contract

Every production-oriented skill or workflow should be able to emit a normalized result containing at least:

```yaml
status: completed | blocked | needs_review
facts: []
findings: []
legal_basis: []
evidence: []
assumptions: []
missing_information: []
confidence: 0.0
requires_human_review: true
source_versions: []
```

The JSON Schemas in `contracts/` are the machine-readable source of truth for these interfaces.

## Legal-claim classification

Legal and compliance statements must be classified. The initial taxonomy is:

- `LAW_REQUIRED`: directly required by binding law/regulation;
- `REGULATOR_GUIDANCE`: non-binding regulator or supervisory-authority guidance;
- `ORGANISATION_POLICY`: rule chosen by the organisation;
- `BEST_PRACTICE`: recommended control or practice not itself legally mandatory;
- `ASSUMPTION`: unresolved premise used for analysis.

A workflow must not silently promote guidance, policy, best practice, or assumptions into legal requirements.

## Human review

Privacy workflows are decision-support systems. High-impact outputs require explicit human review. Examples include:

- final DPIA risk acceptance;
- legal exemptions or refusal of a data-subject request;
- breach-notification decisions;
- international-transfer conclusions;
- advice materially affecting rights of data subjects;
- outputs with missing or conflicting legal authority.

The `human_review.schema.json` contract records reviewer status, rationale and unresolved issues.

## Evidence model

Findings should be traceable to evidence. Evidence can originate from:

- source documents;
- extracted facts;
- structured user input;
- authoritative legal sources;
- framework rules;
- automated checks.

Evidence references should be precise enough to reproduce the conclusion without requiring access to unredacted personal data when that is not necessary.

## Integration with SolidPrivacy Scrub

The intended privacy-preserving workflow is:

```text
ORIGINAL DOCUMENT
  -> SolidPrivacy Scrub
       local detection
       human review
       local Scrub Key
  -> SCRUBBED DOCUMENT
  -> SolidPrivacy AI Workflow
       DPIA / DSAR / RoPA / vendor / breach / other analysis
  -> SCRUBBED AI RESULT
  -> controlled Reinsert
  -> Export / Audit
```

The Scrub Key and original identifiers should remain outside the AI workflow unless a separately approved use case explicitly requires otherwise.

Introducing cloud processing of documents is a separate architectural/security decision and is not implied by this repository structure.

## Third-party skill ingestion policy

Third-party privacy/GRC skill repositories are treated as **raw material**, not legal authority.

Before upstream content is promoted into a SolidPrivacy-native skill:

1. record upstream repository, path, commit/version and license in `provenance/upstream_manifest.yaml`;
2. separate workflow logic from legal assertions;
3. verify material legal assertions against authoritative sources;
4. classify legal claims using `contracts/legal_claim.schema.json`;
5. remove organisation-specific, jurisdiction-specific or cloud-specific assumptions unless intentionally retained;
6. adapt the skill to the common input/output/evidence contracts;
7. add synthetic evaluation cases and regression assertions;
8. define explicit human-review gates.

## Initial implementation priority

The first production-oriented workflow tranche should be deliberately small:

1. DPIA;
2. DSAR;
3. RoPA;
4. breach assessment.

Only after these pass legal-accuracy and regression evaluations should the library expand to retention, vendor assessment, international transfers, ISO/IEC 27701 overlays and EU AI Act workflows.

## Non-goals

This repository is not intended to:

- replace a qualified privacy professional or DPO;
- treat third-party prompts as authoritative law;
- embed sensitive source documents in tests;
- create uncontrolled autonomous legal decisions;
- duplicate the Scrub anonymisation engine;
- introduce cloud document processing by default.
