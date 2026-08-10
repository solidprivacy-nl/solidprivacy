from __future__ import annotations

import copy
import json
from pathlib import Path
import pytest

from solidprivacy.runtime.ai_boundary import ModelCallPolicyError
from solidprivacy.runtime.dpia_analysis import DpiaAnalysisValidationError, FixtureDpiaAnalysisProvider, run_dpia_analysis, validate_analysis_result
from solidprivacy.runtime.legal_context import resolve_legal_context
from solidprivacy.runtime.schema_validation import validate_dpia_analysis_result

ROOT=Path(__file__).resolve().parents[1]; FIXTURES=ROOT/"evals"/"dpia_analysis"
def load(name:str)->dict: return json.loads((FIXTURES/name).read_text(encoding="utf-8"))
def provider_for(request:dict,result:dict)->FixtureDpiaAnalysisProvider: return FixtureDpiaAnalysisProvider(result["provider"],result["model"],{request["id"]:result})

class CountingProvider:
    provider_name="fixture"; model_name="fixture-dpia-analyst-v1"
    def __init__(self,result:dict): self.result=result; self.calls=0
    def analyse(self,request:dict,legal_context:dict)->dict: self.calls+=1; return copy.deepcopy(self.result)

def test_valid_fixture_analysis_is_traceability_validated() -> None:
    request,policy,result=load("request_ready.json"),load("policy_fixture_external.json"),load("result_ready.json"); validated,legal=run_dpia_analysis(request,policy,provider_for(request,result))
    assert legal["status"]=="ready"; assert validated["validation_status"]=="traceability_validated"; assert validated["residual_risk_status"]=="requires_human_assessment"; assert validated["human_review_required"] is True

def test_blocked_evidence_pack_prevents_provider_call() -> None:
    request,policy,result=load("request_ready.json"),load("policy_fixture_external.json"),load("result_ready.json"); request["evidence_pack"]["readiness"]["status"]="blocked"; request["evidence_pack"]["readiness"]["blockers"]=["missing:TEST"]; provider=CountingProvider(result)
    with pytest.raises(Exception): run_dpia_analysis(request,policy,provider)
    assert provider.calls==0

def test_stale_legal_context_prevents_provider_call() -> None:
    request,policy,result=load("request_ready.json"),load("policy_fixture_external.json"),load("result_ready.json"); request["legal_context_request"]["as_of"]="2027-01-15"; request["legal_context_request"]["max_verification_age_days"]=30; provider=CountingProvider(result)
    with pytest.raises(DpiaAnalysisValidationError) as exc: run_dpia_analysis(request,policy,provider)
    assert "legal_context_blocked" in exc.value.errors; assert provider.calls==0

def test_nonfinal_edpb_template_cannot_support_legal_claim() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["claims"][0]["rule_ids"]=["edpb-dpia-template-2026"]
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("unknown_or_non_authoritative_rule:edpb-dpia-template-2026" in e for e in exc.value.errors)

def test_guidance_rule_cannot_support_law_required_classification() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["claims"][2]["claim"]["classification"]="LAW_REQUIRED"
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("classification_not_supported_by_rule" in e for e in exc.value.errors)

def test_invented_fact_reference_is_rejected() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["sections"][0]["fact_ids"]=["F-INVENTED"]
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("unknown_fact:F-INVENTED" in e for e in exc.value.errors)

def test_claim_source_must_match_governed_rule() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["claims"][0]["claim"]["source_id"]="edpb-dpia-guidelines-wp248"
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("source_not_supported_by_rule" in e for e in exc.value.errors)

def test_provider_cannot_self_validate_analysis() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["validation_status"]="traceability_validated"
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert "provider_cannot_self_validate_analysis" in exc.value.errors

def test_residual_risk_cannot_be_finalised_by_provider_contract() -> None:
    bad=load("result_ready.json"); bad["residual_risk_status"]="low"
    with pytest.raises(Exception): validate_dpia_analysis_result(bad)

def test_direct_identifier_policy_gate_blocks_analysis_before_provider() -> None:
    request,policy,result=load("request_ready.json"),load("policy_fixture_external.json"),load("result_ready.json"); request["privacy_context"]["contains_direct_identifiers"]=True; provider=CountingProvider(result)
    with pytest.raises(ModelCallPolicyError): run_dpia_analysis(request,policy,provider)
    assert provider.calls==0

def test_unreviewed_facts_must_remain_explicit_in_section() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["sections"][0]["unresolved_fact_ids"]=[]
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("unresolved_fact_ids_do_not_match_review_state" in e for e in exc.value.errors)

def test_claim_citation_must_bind_to_rule_locator() -> None:
    request,result=load("request_ready.json"),load("result_ready.json"); legal=resolve_legal_context(request["legal_context_request"]); bad=copy.deepcopy(result); bad["claims"][0]["claim"]["citation"]="Article 99"
    with pytest.raises(DpiaAnalysisValidationError) as exc: validate_analysis_result(request,legal,bad)
    assert any("citation_not_bound_to_rule_locator" in e for e in exc.value.errors)
