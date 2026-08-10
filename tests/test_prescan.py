from __future__ import annotations

import json
from pathlib import Path

import pytest

from solidprivacy.runtime.prescan import evaluate_prescan
from solidprivacy.runtime.schema_validation import (
    validate_prescan_decision,
    validate_prescan_input,
)

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evals" / "prescan_cases.json").read_text(encoding="utf-8"))
BY_NAME = {case["name"]: case for case in CASES}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["name"])
def test_prescan_cases(case: dict) -> None:
    payload = case["input"]
    validate_prescan_input(payload)
    decision = evaluate_prescan(payload)
    validate_prescan_decision(decision)
    assert decision["methodology"]["level"] == case["expected"]["methodology_level"]
    assert decision["legal"]["decision"] == case["expected"]["legal_decision"]


def test_two_edpb_criteria_are_not_silently_promoted_to_binding_law() -> None:
    decision = evaluate_prescan(BY_NAME["edpb_two"]["input"])
    assert decision["methodology"]["level"] == "required"
    assert decision["legal"]["decision"] == "DPIA_RECOMMENDED"
    assert decision["legal"]["reasons"][0]["classification"] == "REGULATOR_GUIDANCE"


def test_unverified_ap_selection_requires_review() -> None:
    decision = evaluate_prescan(BY_NAME["ap_unverified"]["input"])
    assert decision["legal"]["decision"] == "NEEDS_REVIEW"
    assert decision["human_review"]["required"] is True


def test_verified_ap_selection_is_required() -> None:
    decision = evaluate_prescan(BY_NAME["ap_verified"]["input"])
    assert decision["legal"]["decision"] == "DPIA_REQUIRED"
    assert decision["legal"]["reasons"][0]["source_id"] == "nl-ap-dpia-mandatory-list-2019"
