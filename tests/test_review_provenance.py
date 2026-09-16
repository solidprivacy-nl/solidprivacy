from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from solidprivacy.runtime.schema_validation import (
    ContractValidationError,
    reviewable_content_sha256,
    validate_dpia,
)


FIXTURE = Path("evals/synthetic_cases/dpia_nl_basic.json")


def load_case() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def approved_case() -> dict:
    case = load_case()
    case["artifact_version"] = "v1"
    review = case["human_review"]
    review.update({
        "required": True,
        "status": "approved",
        "reviewer_id": "privacy-reviewer-01",
        "reviewer_actor_type": "HUMAN",
        "reviewer_role": "privacy_officer",
        "reviewed_at": "2026-09-02T11:00:00+02:00",
        "rationale": "Synthetic professional review completed for deterministic contract validation.",
        "reviewed_artifact_id": case["id"],
        "reviewed_artifact_version": case["artifact_version"],
        "evidence_ids": [],
        "source_reference_ids": ["nl-government-par-dpia-model"],
        "decision_ref": "synthetic-review-decision-01",
    })
    review["reviewed_content_sha256"] = reviewable_content_sha256(case)
    case["status"] = "final"
    return case


def test_existing_pending_fixture_remains_valid() -> None:
    validate_dpia(load_case())


def test_final_dpia_requires_approved_human_review() -> None:
    case = load_case()
    case["status"] = "final"
    with pytest.raises(ContractValidationError, match="final DPIA requires approved human professional review"):
        validate_dpia(case)


def test_exact_approved_review_package_is_valid() -> None:
    validate_dpia(approved_case())


def test_material_change_invalidates_prior_approval() -> None:
    case = approved_case()
    case["residual_risk_conclusion"]["rationale"] = "Materially changed conclusion after professional approval."
    with pytest.raises(ContractValidationError, match="stale or mismatched reviewed content"):
        validate_dpia(case)


def test_review_must_bind_all_current_source_provenance() -> None:
    case = approved_case()
    case["human_review"]["source_reference_ids"] = []
    case["human_review"]["reviewed_content_sha256"] = reviewable_content_sha256(case)
    with pytest.raises(ContractValidationError, match="must exactly bind current source provenance"):
        validate_dpia(case)


def test_review_must_bind_all_current_evidence_provenance() -> None:
    case = approved_case()
    case["evidence"] = [{
        "id": "EVID-REVIEW-01",
        "kind": "automated_check",
        "source": "synthetic-validator",
        "locator": "synthetic://review/01",
        "content_hash": "a" * 64,
        "contains_personal_data": False,
        "metadata": {},
    }]
    case["human_review"]["reviewed_content_sha256"] = reviewable_content_sha256(case)
    with pytest.raises(ContractValidationError, match="must exactly bind current evidence provenance"):
        validate_dpia(case)


def test_approved_review_is_human_and_exact_version_bound() -> None:
    case = approved_case()
    invalid_actor = deepcopy(case)
    invalid_actor["human_review"]["reviewer_actor_type"] = "AI"
    with pytest.raises(ContractValidationError):
        validate_dpia(invalid_actor)

    stale_version = deepcopy(case)
    stale_version["artifact_version"] = "v2"
    with pytest.raises(ContractValidationError, match="does not match current artifact version"):
        validate_dpia(stale_version)
