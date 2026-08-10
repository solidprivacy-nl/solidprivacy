from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Protocol

from solidprivacy.runtime.ai_boundary import enforce_model_call_policy
from solidprivacy.runtime.facts import derive_readiness, validate_evidence_pack_integrity
from solidprivacy.runtime.schema_validation import (
    validate_evidence_pack,
    validate_fact_extraction_request,
    validate_fact_extraction_result,
)


class FactExtractionProvider(Protocol):
    provider_name: str
    model_name: str

    def extract(self, request: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class FixtureFactExtractionProvider:
    """Deterministic test provider. It performs no network/model call."""

    provider_name: str
    model_name: str
    results: dict[str, dict[str, Any]]

    def extract(self, request: dict[str, Any]) -> dict[str, Any]:
        try:
            return copy.deepcopy(self.results[request["id"]])
        except KeyError as exc:
            raise KeyError(f"no fixture result for request {request['id']!r}") from exc


class FactExtractionValidationError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _normalise_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def validate_detector_result(request: dict[str, Any], result: dict[str, Any]) -> None:
    validate_fact_extraction_request(request)
    validate_fact_extraction_result(result)
    errors: list[str] = []
    evidence = {item["id"]: item for item in request["evidence"]}
    facts = {item["id"]: item for item in result["facts"]}

    if result["request_id"] != request["id"]: errors.append("request_id_mismatch")
    if result["provider"] != request["requested_provider"]: errors.append("provider_mismatch")
    if result["model"] != request["requested_model"]: errors.append("model_mismatch")
    if result["model_metadata"]["prompt_version"] != request["prompt_version"]: errors.append("prompt_version_mismatch")

    for duplicate in _duplicates([item["id"] for item in result["facts"]]):
        errors.append(f"duplicate_fact_id:{duplicate}")

    for fact in result["facts"]:
        if fact["review_status"] not in {"pending", "needs_clarification"}:
            errors.append(f"detector_cannot_set_review_outcome:{fact['id']}")
        if fact["epistemic_status"] == "user_confirmed":
            errors.append(f"detector_cannot_self_confirm_user_fact:{fact['id']}")
        if fact.get("validation_status") not in {None, "unvalidated"}:
            errors.append(f"detector_cannot_self_validate:{fact['id']}")
        if not fact["canonical_path"].startswith("processing_activities["):
            errors.append(f"unsupported_canonical_path:{fact['id']}")
        for evidence_id in fact["evidence_ids"]:
            if evidence_id not in evidence:
                errors.append(f"unknown_evidence:{fact['id']}:{evidence_id}")

    proof_keys: set[tuple[str, str, str]] = set()
    proofs_by_fact: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for proof in result["support_proofs"]:
        key = (proof["fact_id"], proof["evidence_id"], proof["excerpt"])
        if key in proof_keys: continue
        proof_keys.add(key)
        if proof["fact_id"] not in facts:
            errors.append(f"support_unknown_fact:{proof['fact_id']}"); continue
        if proof["evidence_id"] not in evidence:
            errors.append(f"support_unknown_evidence:{proof['evidence_id']}"); continue
        fact = facts[proof["fact_id"]]
        if proof["evidence_id"] not in fact["evidence_ids"]:
            errors.append(f"support_evidence_not_declared_on_fact:{proof['fact_id']}:{proof['evidence_id']}"); continue
        evidence_excerpt = evidence[proof["evidence_id"]].get("excerpt") or ""
        if proof["excerpt"] not in evidence_excerpt:
            errors.append(f"support_excerpt_not_found:{proof['fact_id']}:{proof['evidence_id']}"); continue
        proofs_by_fact[proof["fact_id"]].append(proof)

    for fact in result["facts"]:
        if fact["epistemic_status"] in {"observed", "inferred"} and not proofs_by_fact[fact["id"]]:
            errors.append(f"no_verified_support_proof:{fact['id']}")
    if errors: raise FactExtractionValidationError(sorted(set(errors)))


def validate_and_annotate_facts(request: dict[str, Any], result: dict[str, Any]) -> list[dict[str, Any]]:
    validate_detector_result(request, result)
    proofs_by_fact: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for proof in result["support_proofs"]: proofs_by_fact[proof["fact_id"]].append(proof)
    validated = []
    for candidate in result["facts"]:
        fact = copy.deepcopy(candidate)
        if fact["epistemic_status"] in {"observed", "inferred"}:
            fact["validation_status"] = "provenance_validated"
            fact["validator_notes"] = [f"support_proof:{p['evidence_id']}" for p in proofs_by_fact[fact["id"]]]
        else:
            fact["validation_status"] = "challenged"
            fact["validator_notes"] = ["assumption_not_treated_as_evidence_backed_fact"]
        validated.append(fact)
    return validated


def detect_fact_contradictions(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for fact in facts: grouped[fact["canonical_path"]].append(fact)
    contradictions = []
    high_types = {"legal_basis_candidate","retention_candidate","transfer","special_category_candidate","automated_decision_context"}
    sequence = 1
    for path in sorted(grouped):
        candidates = grouped[path]
        if len({_normalise_value(item["value"]) for item in candidates}) <= 1: continue
        severity = "high" if any(item["fact_type"] in high_types for item in candidates) else "normal"
        contradictions.append({"id":f"C-AUTO-{sequence:03d}","fact_ids":sorted(item["id"] for item in candidates),"severity":severity,"status":"open","description":f"Conflicting candidate facts target the same canonical path: {path}","resolution":None})
        sequence += 1
    return contradictions


def build_evidence_pack(request: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    facts = validate_and_annotate_facts(request, result)
    pack: dict[str, Any] = {
        "id": f"EP-{request['id']}",
        "case_id": request["case_id"],
        "jurisdiction": request["jurisdiction"],
        "evidence": copy.deepcopy(request["evidence"]),
        "facts": facts,
        "contradictions": detect_fact_contradictions(facts),
        "missing_information": copy.deepcopy(result["missing_information"]),
        "readiness": {"stage":"analysis","status":"needs_review","blockers":[],"rationale":"Placeholder before deterministic readiness derivation."},
        "human_review": {"required":True,"status":"pending","reviewer_role":"privacy_officer","reviewed_at":None,"rationale":None,"changes_required":[],"unresolved_issues":[]},
        "source_versions": [f"provider:{result['provider']}",f"model:{result['model']}",f"prompt:{result['model_metadata']['prompt_version']}"],
        "notes": "Generated from policy-gated fact extraction; model output remains decision support."
    }
    readiness = derive_readiness(pack, "analysis")
    pack["readiness"] = {"stage":"analysis","status":readiness["status"],"blockers":readiness["blockers"],"rationale":readiness["rationale"]}
    validate_evidence_pack(pack)
    validate_evidence_pack_integrity(pack)
    return pack


def run_fact_extraction(request: dict[str, Any], policy: dict[str, Any], provider: FactExtractionProvider) -> dict[str, Any]:
    enforce_model_call_policy(request, policy)
    if provider.provider_name != request["requested_provider"]: raise FactExtractionValidationError(["runtime_provider_mismatch"])
    if provider.model_name != request["requested_model"]: raise FactExtractionValidationError(["runtime_model_mismatch"])
    return build_evidence_pack(request, provider.extract(request))
