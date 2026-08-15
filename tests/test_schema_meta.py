from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from solidprivacy.runtime.schema_validation import contracts_dir


def test_all_contract_schemas_are_valid_draft_2020_12() -> None:
    for path in sorted(contracts_dir().glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
