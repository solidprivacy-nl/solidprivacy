# Mappings

Mappings connect external vocabularies, methodologies and schemas to SolidPrivacy canonical concepts without making external formats the internal product contract.

Examples:

- Dutch Government DPIA field -> canonical privacy concept -> DPV concept;
- EDPB template field -> canonical DPIA field;
- CNIL PIA concept -> canonical risk/control concept;
- future OSCAL control/evidence object -> SolidPrivacy control object.

Mappings must be versioned and testable. A source-model update should fail an evaluation when a mapped field disappears or changes meaning rather than silently changing workflow behaviour.
