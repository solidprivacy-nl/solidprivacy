from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_prescan_rule_source_ids_exist_in_legal_registry() -> None:
    rules = json.loads(
        (ROOT / "methodologies" / "nl_rijksmodel_dpia" / "prescan_rules.json")
        .read_text(encoding="utf-8")
    )
    registry = (ROOT / "legal_sources" / "source_registry.yaml").read_text(encoding="utf-8")

    source_ids = {rules["methodology_source"]["source_id"]}
    for item in rules["legal_gate"]["required_when"]:
        source_ids.add(item["source_id"])
    for item in rules["legal_gate"]["recommend_when"]:
        source_ids.add(item["source_id"])

    for source_id in source_ids:
        assert f"- id: {source_id}\n" in registry, source_id
