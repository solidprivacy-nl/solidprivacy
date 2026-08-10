from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Protocol

from solidprivacy.runtime.ai_boundary import enforce_model_call_policy
from solidprivacy.runtime.facts import validate_evidence_pack_integrity
from solidprivacy.runtime.legal_context import resolve_legal_context
from solidprivacy.runtime.schema_validation import validate_dpia_analysis_request, validate_dpia_analysis_result, validate_evidence_pack


class DpiaAnalysisProvider(Protocol):
    provider_name: str
    model_name: str
    def analyse(self, request: dict[str, Any], legal_context: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class FixtureDpiaAnalysisProvider:
    provider_name: str
    model_name: str
    results: dict[str, dict[str, Any]]
    def analyse(self, request: dict[str, Any], legal_context: dict[str, Any]) -> dict[str, Any]:
        try:
            return copy.deepcopy(self.results[request["id"]])
        except KeyError as exc:
            raise KeyError(f"no fixture analysis result for request {request['id']!r}") from exc


class DpiaAnalysisValidationError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def validate_analysis_result(request: dict[str, Any], legal_context: dict[str, Any], result: dict[str, Any]) -> None:
    validate_dpia_analysis_result(result)
    errors: list[str] = []
    if result["request_id"] != request["id"]: errors.append("request_id_mismatch")
    if result["provider"] != request["requested_provider"]: errors.append("provider_mismatch")
    if result["model"] != request["requested_model"]: errors.append("model_mismatch")
    if result["model_metadata"]["prompt_version"] != request["prompt_version"]: errors.append("prompt_version_mismatch")
    if result["validation_status"] != "unvalidated": errors.append("provider_cannot_self_validate_analysis")
    if result["human_review_required"] is not True: errors.append("human_review_must_remain_required")
    facts = {item["id"]: item for item in request["evidence_pack"]["facts"]}
    rules = {item["id"]: item for item in legal_context["rules"]}
    claims = {item["id"]: item for item in result["claims"]}
    risks = {item["id"]: item for item in result["risks"]}
    def check_fact_ids(values: list[str], path: str) -> None:
        for fact_id in values:
            fact = facts.get(fact_id)
            if not fact:
                errors.append(f"{path}:unknown_fact:{fact_id}"); continue
            if fact.get("validation_status") != "provenance_validated": errors.append(f"{path}:fact_not_provenance_validated:{fact_id}")
            if fact.get("review_status") == "rejected": errors.append(f"{path}:rejected_fact:{fact_id}")
    def check_rule_ids(values: list[str], path: str) -> None:
        for rule_id in values:
            if rule_id not in rules: errors.append(f"{path}:unknown_or_non_authoritative_rule:{rule_id}")
    for section in result["sections"]:
        check_fact_ids(section["fact_ids"], f"section:{section['id']}")
        check_rule_ids(section["legal_rule_ids"], f"section:{section['id']}")
        unresolved_expected = sorted(fact_id for fact_id in section["fact_ids"] if fact_id in facts and facts[fact_id].get("review_status") != "accepted")
        if sorted(section["unresolved_fact_ids"]) != unresolved_expected: errors.append(f"section:{section['id']}:unresolved_fact_ids_do_not_match_review_state")
        for fact_id in section["unresolved_fact_ids"]:
            if fact_id not in section["fact_ids"]: errors.append(f"section:{section['id']}:unresolved_fact_not_in_section:{fact_id}")
        for claim_id in section["claim_ids"]:
            if claim_id not in claims: errors.append(f"section:{section['id']}:unknown_claim:{claim_id}")
    for supported in result["claims"]:
        claim = supported["claim"]
        check_fact_ids(supported["fact_ids"], f"claim:{supported['id']}")
        check_rule_ids(supported["rule_ids"], f"claim:{supported['id']}")
        supporting_rules = [rules[rid] for rid in supported["rule_ids"] if rid in rules]
        if supporting_rules:
            if not all(rule["classification"] == claim["classification"] for rule in supporting_rules): errors.append(f"claim:{supported['id']}:classification_not_supported_by_rule")
            if not all(rule["source_id"] == claim["source_id"] for rule in supporting_rules): errors.append(f"claim:{supported['id']}:source_not_supported_by_rule")
            if not all(rule["authority"] == claim["authority"] for rule in supporting_rules): errors.append(f"claim:{supported['id']}:authority_not_supported_by_rule")
            if not all(rule["jurisdiction"] == claim["jurisdiction"] for rule in supporting_rules): errors.append(f"claim:{supported['id']}:jurisdiction_not_supported_by_rule")
            if claim.get("citation") not in {rule["locator"] for rule in supporting_rules}: errors.append(f"claim:{supported['id']}:citation_not_bound_to_rule_locator")
            claim_date = datetime.fromisoformat(claim["verified_at"]).date()
            as_of = date.fromisoformat(legal_context["as_of"])
            if claim_date > as_of: errors.append(f"claim:{supported['id']}:verified_after_context_as_of")
            latest_rule_date = max(date.fromisoformat(rule["rule_last_verified"]) for rule in supporting_rules)
            if claim_date < latest_rule_date: errors.append(f"claim:{supported['id']}:verified_before_rule_verification")
    for risk in result["risks"]:
        check_fact_ids(risk["fact_ids"], f"risk:{risk['id']}")
        check_rule_ids(risk["legal_rule_ids"], f"risk:{risk['id']}")
    for measure in result["measures"]:
        for risk_id in measure["risk_ids"]:
            if risk_id not in risks: errors.append(f"measure:{measure['id']}:unknown_risk:{risk_id}")
    if errors: raise DpiaAnalysisValidationError(sorted(set(errors)))


def run_dpia_analysis(request: dict[str, Any], policy: dict[str, Any], provider: DpiaAnalysisProvider) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_dpia_analysis_request(request)
    validate_evidence_pack(request["evidence_pack"])
    validate_evidence_pack_integrity(request["evidence_pack"])
    if request["evidence_pack"]["readiness"]["status"] == "blocked": raise DpiaAnalysisValidationError(["evidence_pack_blocked_for_analysis"])
    legal_context = resolve_legal_context(request["legal_context_request"])
    if legal_context["status"] != "ready": raise DpiaAnalysisValidationError(["legal_context_blocked"] + [f"legal_context:{item}" for item in legal_context["blockers"]])
    enforce_model_call_policy(request, policy)
    if provider.provider_name != request["requested_provider"]: raise DpiaAnalysisValidationError(["runtime_provider_mismatch"])
    if provider.model_name != request["requested_model"]: raise DpiaAnalysisValidationError(["runtime_model_mismatch"])
    result = provider.analyse(request, legal_context)
    validate_analysis_result(request, legal_context, result)
    validated = copy.deepcopy(result)
    validated["validation_status"] = "traceability_validated"
    validated["validator_notes"] = ["all_fact_references_provenance_validated","all_legal_claims_supported_by_governed_rules","residual_risk_reserved_for_human_assessment"]
    validate_dpia_analysis_result(validated)
    return validated, legal_context
