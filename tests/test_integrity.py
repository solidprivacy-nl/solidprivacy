from __future__ import annotations

import copy

from solidprivacy.runtime.integrity import dpia_integrity_errors


def _minimal_dpia() -> dict:
    return {
        "processing_activities": [{
            "id": "PA-1",
            "purposes": [{"id": "PUR-1"}],
            "personal_data": [{"id": "PD-1", "data_subject_ids": ["DS-1"]}],
            "data_subjects": [{"id": "DS-1"}],
            "parties": [{"id": "PTY-1"}],
            "retention": [{
                "purpose_ids": ["PUR-1"],
                "data_subject_ids": ["DS-1"],
                "personal_data_ids": ["PD-1"],
            }],
        }],
        "risks": [{
            "id": "R-1",
            "processing_activity_ids": ["PA-1"],
            "affected_data_subjects": ["DS-1"],
        }],
        "measures": [{
            "id": "M-1",
            "risk_ids": ["R-1"],
            "evidence_refs": [],
        }],
        "special_data_assessment": [],
        "purpose_compatibility": [{"processing_activity_id": "PA-1"}],
        "evidence": [],
        "residual_risk_conclusion": {"level": "low", "prior_consultation_required": False},
        "human_review": {"required": True, "status": "pending"},
    }


def test_integrity_accepts_resolved_references() -> None:
    assert dpia_integrity_errors(_minimal_dpia()) == []


def test_integrity_rejects_broken_nested_reference() -> None:
    payload = _minimal_dpia()
    payload["processing_activities"][0]["personal_data"][0]["data_subject_ids"] = ["MISSING"]
    errors = dpia_integrity_errors(payload)
    assert any("unknown reference 'MISSING'" in error for error in errors)


def test_integrity_rejects_measure_to_missing_risk() -> None:
    payload = _minimal_dpia()
    payload["measures"][0]["risk_ids"] = ["R-MISSING"]
    errors = dpia_integrity_errors(payload)
    assert any("R-MISSING" in error for error in errors)


def test_high_residual_risk_cannot_be_false_consultation_and_approved() -> None:
    payload = _minimal_dpia()
    payload["residual_risk_conclusion"]["level"] = "high"
    payload["residual_risk_conclusion"]["prior_consultation_required"] = False
    payload["human_review"] = {"required": False, "status": "approved"}
    errors = dpia_integrity_errors(payload)
    assert len(errors) == 3


def test_integrity_rejects_globally_ambiguous_nested_ids() -> None:
    payload = _minimal_dpia()
    second = copy.deepcopy(payload["processing_activities"][0])
    second["id"] = "PA-2"
    payload["processing_activities"].append(second)
    errors = dpia_integrity_errors(payload)
    assert any("globally duplicate id 'DS-1'" in error for error in errors)
    assert any("globally duplicate id 'PD-1'" in error for error in errors)
    assert any("globally duplicate id 'PUR-1'" in error for error in errors)
    assert any("globally duplicate id 'PTY-1'" in error for error in errors)
