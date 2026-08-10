from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from solidprivacy.runtime.dpia_analysis import FixtureDpiaAnalysisProvider, run_dpia_analysis
from solidprivacy.runtime.review import (
    ReviewValidationError,
    build_review_request,
    finalize_dpia_review,
    verify_audit_record,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def context() -> tuple[dict, dict, dict, dict]:
    request = load("evals/dpia_analysis/request_ready.json")
    policy = load("evals/dpia_analysis/policy_fixture_external.json")
    result = load("evals/dpia_analysis/result_ready.json")
    decisions = load("evals/dpia_review/decisions_approved.json")
    provider = FixtureDpiaAnalysisProvider(result["provider"], result["model"], {request["id"]: result})
    analysis, legal = run_dpia_analysis(request, policy, provider)
    review_request = build_review_request(request, analysis, legal, generated_at=decisions["signed_at"])
    return review_request, decisions, analysis, request


def test_review_request_freezes_all_material_inputs_and_targets() -> None:
    review_request, _, _, _ = context()
    targets = {(item["target_type"], item["target_id"]) for item in review_request["required_review_targets"]}
    assert targets == {
        ("fact", "F-FX-001"), ("fact", "F-FX-002"),
        ("claim", "CL-001"), ("claim", "CL-002"), ("claim", "CL-003"),
        ("risk", "R-DRAFT-001"), ("measure", "M-DRAFT-001"),
        ("section", "SEC-001"), ("section", "SEC-002"),
    }
    assert all(len(value) == 64 for value in review_request["snapshot_hashes"].values())


def test_approved_review_generates_scrubbed_report_handoff_and_audit() -> None:
    review_request, decisions, _, _ = context()
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "approved_with_changes"
    assert package["report"] is not None
    assert package["reinsert_handoff"] is not None
    assert package["report"]["privacy_context"] == {
        "scrubbed": True, "scrub_key_present": False, "contains_direct_identifiers": False
    }
    assert package["reinsert_handoff"]["scrub_key_included"] is False
    assert package["reinsert_handoff"]["replacement_mapping_included"] is False
    assert "role-based access control" in package["report"]["body"].lower()
    verify_audit_record(package["audit_record"], review_request, decisions)


def test_source_and_evidence_appendices_are_derived_not_free_text() -> None:
    review_request, decisions, _, _ = context()
    package = finalize_dpia_review(review_request, decisions)
    source_ids = {item["rule_id"] for item in package["source_appendix"]}
    evidence_ids = {item["evidence_id"] for item in package["evidence_appendix"]}
    assert "gdpr-art36-1-prior-consultation" in source_ids
    assert "edpb-wp248-two-criteria" in source_ids
    assert {"EV-FX-001", "EV-FX-002", "EV-REV-001", "EV-REV-002"}.issubset(evidence_ids)


def test_missing_required_decision_prevents_approval_and_report() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["decisions"] = [item for item in decisions["decisions"] if item["target_id"] != "CL-001"]
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "needs_revision"
    assert "missing_decision:claim:CL-001" in package["unresolved_issues"]
    assert package["report"] is None and package["reinsert_handoff"] is None


def test_request_for_evidence_prevents_approval() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    target = next(item for item in decisions["decisions"] if item["target_id"] == "R-DRAFT-001")
    target.update({"action": "request_evidence", "rationale": "Technische effectiviteit moet nog worden aangetoond.", "replacement": None})
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "needs_revision"
    assert "evidence_requested:risk:R-DRAFT-001" in package["unresolved_issues"]


def test_open_question_prevents_approval() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["question_resolutions"][0]["status"] = "open"
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "needs_revision"
    assert any(item.startswith("open_question:") for item in package["unresolved_issues"])


def test_high_residual_risk_cannot_be_approved_as_no_prior_consultation() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["residual_risk"]["level"] = "high"
    decisions["residual_risk"]["prior_consultation_disposition"] = "not_required"
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "needs_revision"
    assert "high_residual_risk_cannot_skip_prior_consultation_review" in package["unresolved_issues"]


def test_high_residual_risk_with_required_consultation_gets_pending_status() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["residual_risk"]["level"] = "high"
    decisions["residual_risk"]["prior_consultation_disposition"] = "required"
    decisions["residual_risk"]["prior_consultation_rationale"] = "De menselijke reviewer concludeert dat voorafgaande raadpleging nodig is voordat de verwerking doorgaat."
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "approved_pending_prior_consultation"
    assert package["report"] is not None


def test_unknown_dpo_status_prevents_final_approval() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["dpo_consultation"] = {"status": "unknown", "advice_summary": None, "evidence_ids": []}
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "needs_revision"
    assert "dpo_status_unknown" in package["unresolved_issues"]


def test_snapshot_tampering_is_detected() -> None:
    review_request, decisions, _, _ = context()
    review_request = copy.deepcopy(review_request)
    review_request["analysis"]["sections"][0]["narrative"] += " tampered"
    with pytest.raises(ReviewValidationError) as exc:
        finalize_dpia_review(review_request, decisions)
    assert any("snapshot_hash_mismatch:analysis" in item for item in exc.value.errors)


def test_unknown_review_target_is_rejected() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["decisions"].append({"target_type":"claim","target_id":"CL-INVENTED","action":"accept","rationale":None,"replacement":None,"evidence_ids":[],"decided_at":decisions["signed_at"]})
    with pytest.raises(ReviewValidationError) as exc:
        finalize_dpia_review(review_request, decisions)
    assert "unknown_review_target:claim:CL-INVENTED" in exc.value.errors


def test_unknown_decision_evidence_is_rejected() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["decisions"][0]["evidence_ids"] = ["EV-INVENTED"]
    with pytest.raises(ReviewValidationError):
        finalize_dpia_review(review_request, decisions)


def test_review_input_privacy_context_cannot_contain_direct_identifiers() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["review_input_privacy_context"]["contains_direct_identifiers"] = True
    with pytest.raises(Exception):
        finalize_dpia_review(review_request, decisions)


def test_reviewer_can_reject_without_generating_a_report() -> None:
    review_request, decisions, _, _ = context()
    decisions = copy.deepcopy(decisions)
    decisions["overall_disposition"] = "reject"
    decisions["overall_rationale"] = "De reviewer wijst de draft af en verlangt een nieuwe analyse."
    decisions["decisions"] = decisions["decisions"][:1]
    package = finalize_dpia_review(review_request, decisions)
    assert package["status"] == "rejected"
    assert package["report"] is None and package["reinsert_handoff"] is None


def test_audit_tampering_is_detected() -> None:
    review_request, decisions, _, _ = context()
    package = finalize_dpia_review(review_request, decisions)
    audit = copy.deepcopy(package["audit_record"])
    audit["analysis_hash"] = "0" * 64
    with pytest.raises(ReviewValidationError):
        verify_audit_record(audit, review_request, decisions)


def test_direct_identifier_analysis_request_cannot_enter_review_request() -> None:
    review_request, _, analysis, analysis_request = context()
    analysis_request = copy.deepcopy(analysis_request)
    analysis_request["privacy_context"]["contains_direct_identifiers"] = True
    with pytest.raises(ReviewValidationError):
        build_review_request(analysis_request, analysis, review_request["legal_context"], generated_at=review_request["generated_at"])
