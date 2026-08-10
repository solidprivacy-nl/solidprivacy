# WP1 — Canonical Privacy Model + Dutch DPIA Adapter

Status: implemented foundation; ready for review

Branch: `agent/canonical-dpia-model`
Base: `agent/architecture-foundation`

## Goal

Create the first production-oriented vertical slice of the SolidPrivacy privacy operating architecture by representing a Dutch DPIA in a SolidPrivacy-native canonical model, while keeping methodology, semantics and legal authority separate.

## Source baseline

- MinBZK `par-dpia-form` pinned at `d8d690989da03287b8879ba1319f78ca8a404bd5`.
- `sources/dpia.yaml`: declared Rijksmodel version `3.0`, blob `aecc3699ecdb87c98587d77b7cc5bb42b04ab5d1`.
- `sources/prescan.yaml`: declared pre-scan version `2.0`.
- Dutch DPIA information model: published version `1.0.0`, 1 June 2025.
- DPV mapping reference: repository commit `c85ffacc97041b90a7a3afb3b6417f0b4d9fafbc`, vocabulary path `2.1/dpv/dpv.csv`.

No upstream questionnaire text or application code is vendored in this workpackage.

## Delivered

1. `contracts/privacy_processing_activity.schema.json`
   - reusable processing-activity object for DPIA, RoPA, DSAR, vendor and transfer workflows;
   - purposes, personal data, data subjects, parties, operations, technologies, locations/transfers, legal bases, retention and rights procedures.

2. `contracts/dpia_assessment.schema.json`
   - DPIA-specific assessment envelope;
   - necessity/proportionality, special-data assessment, purpose compatibility, risks, measures, residual risk, evidence, legal claims and human review.

3. `methodologies/nl_rijksmodel_dpia/source_manifest.yaml`
   - pins upstream source/version/blob identifiers;
   - records reuse mode and classification policy.

4. `methodologies/nl_rijksmodel_dpia/canonical_mapping.yaml`
   - maps Rijksmodel sections/field identifiers to canonical contract paths;
   - explicitly flags fields that still require legal validation.

5. `vocabularies/dpv/canonical_mapping.yaml`
   - maps core canonical concepts to DPV semantics;
   - explicitly states that DPV does not constitute legal authority.

6. Synthetic evaluations
   - low-risk employee-portal case;
   - unresolved high-risk AI/health-data case;
   - assertions for schema/source/human-review and uncertainty behaviour.

## Key design decisions

### One reusable processing model

DPIA does not get its own duplicate definition of processing activity. The same canonical processing object should later feed RoPA and other workflows. This is intentional to prevent semantic drift between products.

### Source field is not law

A field in the Rijksmodel is classified as `OFFICIAL_METHODOLOGY`. A binding claim must separately reference an approved legal source such as GDPR/EUR-Lex. Regulator interpretations must be classified as guidance.

### Risk and measure linkage is explicit

Each measure references one or more risk IDs and stores implementation status plus residual level. This creates the bridge to the control/evidence model and makes later audit/evidence collection possible.

### High residual risk blocks autonomous completion

The high-risk synthetic case intentionally leaves prior consultation unresolved and human review pending. The evaluation suite treats silent resolution of that uncertainty as a failure.

## Acceptance criteria

- [x] exact MinBZK source is pinned;
- [x] no EUPL-covered questionnaire/application content is copied into SolidPrivacy;
- [x] canonical processing contract exists;
- [x] DPIA contract exists;
- [x] Rijksmodel field mapping exists;
- [x] DPV semantic mapping exists;
- [x] methodology vs legal authority is explicitly separated;
- [x] low-risk synthetic case exists;
- [x] high-risk/unresolved synthetic case exists;
- [x] human-review gate is represented;
- [ ] executable JSON-Schema/eval runner — next workpackage;
- [ ] full pre-scan decision/trigger engine — next workpackage;
- [ ] production AI DPIA skill — after executable eval gate.

## Recommended next workpackage

`WP2 — Executable DPIA Contract + Pre-scan Decision Engine`

It should add a deterministic validator/eval runner, encode the pre-scan-to-DPIA relationships, and expose a machine-readable decision result such as `DPIA_REQUIRED | DPIA_RECOMMENDED | DPIA_NOT_INDICATED | NEEDS_REVIEW`, without allowing the AI layer to invent legal trigger rules.
