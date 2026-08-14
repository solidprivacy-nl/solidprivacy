# Vocabularies

Canonical privacy semantics live here.

## Initial strategy

Use W3C Data Privacy Vocabulary (DPV) as the preferred external semantic reference for concepts such as personal data, purpose, processing, entities, roles, legal bases, rights, risks, measures and technologies.

SolidPrivacy should generally **map to** DPV rather than vendor the complete vocabulary. Any vendored subset requires explicit license/provenance review.

## Rules

- vocabulary terms do not constitute legal advice or legal authority;
- preserve stable SolidPrivacy identifiers where product contracts require them;
- maintain explicit mappings from external terms to canonical internal concepts;
- jurisdiction-specific meanings belong in `jurisdictions/`, not here;
- new enums should be introduced only when an existing canonical concept cannot represent the requirement.
