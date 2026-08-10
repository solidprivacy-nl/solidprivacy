from __future__ import annotations

import json
from pathlib import Path

import pytest

from solidprivacy.runtime.ai_boundary import ModelCallPolicyError, enforce_model_call_policy
from solidprivacy.runtime.fact_extraction import FactExtractionValidationError, FixtureFactExtractionProvider, run_fact_extraction, validate_detector_result
from solidprivacy.runtime.schema_validation import validate_fact_extraction_request, validate_fact_extraction_result, validate_model_call_policy

ROOT=Path(__file__).resolve().parents[1]
FIXTURES=ROOT/"evals"/"ai_fact_extraction"

def load(name: str) -> dict: return json.loads((FIXTURES/name).read_text(encoding="utf-8"))
def provider_for(*results: dict) -> FixtureFactExtractionProvider:
    return FixtureFactExtractionProvider("fixture","fixture-privacy-extractor-v1",{r["request_id"]:r for r in results})

def test_contract_fixtures_validate() -> None:
    validate_model_call_policy(load("policy_fixture_external.json")); validate_fact_extraction_request(load("request_ready.json")); validate_fact_extraction_result(load("result_ready.json"))

def test_safe_scrubbed_request_is_allowed() -> None:
    assert enforce_model_call_policy(load("request_ready.json"),load("policy_fixture_external.json")).allowed is True

def test_scrub_key_is_never_allowed() -> None:
    r=load("request_ready.json"); r["privacy_context"]["scrub_key_present"]=True
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(r,load("policy_fixture_external.json"))
    assert "scrub_key_must_never_be_sent_to_model" in exc.value.reasons

def test_unscrubbed_input_is_blocked() -> None:
    r=load("request_ready.json"); r["privacy_context"]["scrubbed"]=False
    with pytest.raises(ModelCallPolicyError): enforce_model_call_policy(r,load("policy_fixture_external.json"))

def test_special_category_external_egress_is_blocked() -> None:
    r=load("request_ready.json"); r["privacy_context"]["content_classification"]="special_category"
    p=load("policy_fixture_external.json"); p["max_content_classification"]="special_category"
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(r,p)
    assert "special_category_egress_not_allowed" in exc.value.reasons

def test_unknown_provider_training_use_blocks_external_call() -> None:
    p=load("policy_fixture_external.json"); p["provider_training_use"]="unknown"
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(load("request_ready.json"),p)
    assert "provider_training_use_not_safely_resolved" in exc.value.reasons

def test_detector_cannot_self_accept_fact() -> None:
    result=load("result_ready.json"); result["facts"][0]["review_status"]="accepted"
    with pytest.raises(FactExtractionValidationError) as exc: validate_detector_result(load("request_ready.json"),result)
    assert any("detector_cannot_set_review_outcome" in e for e in exc.value.errors)

def test_detector_support_quote_must_exist_in_evidence() -> None:
    result=load("result_ready.json"); result["support_proofs"][0]["excerpt"]="invented quote not present in evidence"
    with pytest.raises(FactExtractionValidationError) as exc: validate_detector_result(load("request_ready.json"),result)
    assert any("support_excerpt_not_found" in e for e in exc.value.errors)

def test_detector_cannot_self_confirm_user_fact() -> None:
    result=load("result_ready.json"); result["facts"][0]["epistemic_status"]="user_confirmed"
    with pytest.raises(FactExtractionValidationError): validate_detector_result(load("request_ready.json"),result)

def test_ready_extraction_becomes_provenance_validated_pack_needing_review() -> None:
    request=load("request_ready.json"); result=load("result_ready.json")
    pack=run_fact_extraction(request,load("policy_fixture_external.json"),provider_for(result))
    assert pack["readiness"]["status"]=="needs_review"
    assert all(f["validation_status"]=="provenance_validated" for f in pack["facts"])
    assert pack["human_review"]["required"] is True

def test_conflicting_retention_candidates_are_detected_and_block_analysis() -> None:
    request=load("request_conflict.json"); result=load("result_conflict.json")
    pack=run_fact_extraction(request,load("policy_fixture_external.json"),provider_for(result))
    assert pack["readiness"]["status"]=="blocked"; assert len(pack["contradictions"])==1
    c=pack["contradictions"][0]; assert c["severity"]=="high"; assert set(c["fact_ids"])=={"F-FX-101","F-FX-102"}

def test_runtime_provider_mismatch_is_blocked() -> None:
    request=load("request_ready.json"); result=load("result_ready.json")
    provider=FixtureFactExtractionProvider("wrong-provider","fixture-privacy-extractor-v1",{request["id"]:result})
    with pytest.raises(FactExtractionValidationError): run_fact_extraction(request,load("policy_fixture_external.json"),provider)

def test_scrubbed_personal_data_requires_explicit_egress_permission() -> None:
    p=load("policy_fixture_external.json"); p["allow_scrubbed_personal_data_egress"]=False
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(load("request_ready.json"),p)
    assert "scrubbed_personal_data_egress_not_allowed" in exc.value.reasons

def test_direct_identifiers_never_cross_external_wp4_boundary() -> None:
    r=load("request_ready.json"); r["privacy_context"]["contains_direct_identifiers"]=True
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(r,load("policy_fixture_external.json"))
    assert "direct_identifiers_must_not_leave_scrub_boundary" in exc.value.reasons

def test_unknown_direct_identifier_status_blocks_sensitive_external_call() -> None:
    r=load("request_ready.json"); r["privacy_context"]["contains_direct_identifiers"]=None
    with pytest.raises(ModelCallPolicyError) as exc: enforce_model_call_policy(r,load("policy_fixture_external.json"))
    assert "direct_identifier_status_not_safely_resolved" in exc.value.reasons
