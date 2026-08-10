# Dutch Government DPIA methodology adapter

Status: WP1 canonical adapter implemented; no upstream questionnaire or application code vendored.

Primary references:

- `https://github.com/MinBZK/par-dpia-form`
- `https://modellen.jenvgegevens.nl/dpia/`

## Current pinned baseline

The adapter is pinned in `source_manifest.yaml` to MinBZK commit `d8d690989da03287b8879ba1319f78ca8a404bd5`.

At that baseline:

- `sources/dpia.yaml` declares `urn:nl:dpia`, model version `3.0`;
- `sources/prescan.yaml` declares `urn:nl:prescan`, model version `2.0`;
- the assessment definitions use structured IDs, repeatable groups, dependencies and explicit pre-scan/DPIA references;
- the Dutch Government information model is tracked separately as a semantic/reference source.

## Adapter artefacts

- `source_manifest.yaml` — exact upstream provenance and reuse posture;
- `canonical_mapping.yaml` — Rijksmodel field IDs to SolidPrivacy canonical contract paths;
- `../../contracts/privacy_processing_activity.schema.json` — reusable processing object;
- `../../contracts/dpia_assessment.schema.json` — DPIA-specific assessment contract;
- `../../vocabularies/dpv/canonical_mapping.yaml` — canonical-to-DPV semantics.

## Classification rule

A Rijksmodel field is an `OFFICIAL_METHODOLOGY` element by default. It is **not** automatically a binding legal requirement.

Where a field requires a legal conclusion — for example legal basis, special-category exception, purpose compatibility, data-subject-right restriction or prior consultation — the workflow must obtain and cite separately approved legal/regulator sources.

## Licensing posture

The MinBZK repository is EUPL-1.2. WP1 does not copy the questionnaire text or application implementation. It references source identifiers, versions and relationships for interoperability and traceability. Any later vendoring or adaptation of EUPL-covered content must undergo explicit license/provenance review.

## Next boundary

The next workpackage should implement an executable validator and pre-scan decision engine. AI-generated DPIA prose should only be added after deterministic contract/evaluation gates exist.
