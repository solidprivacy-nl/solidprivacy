from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from solidprivacy import __version__
from solidprivacy.runtime.schema_validation import (
    validate_dpia_analysis_request,
    validate_dpia_analysis_result,
    validate_dpia_review_decision_set,
    validate_dpia_review_package,
    validate_dpia_review_request,
    validate_evidence_pack,
    validate_legal_context_bundle,
    validate_review_audit_record,
)


class ReviewValidationError(ValueError):
    """Raised when a review package violates deterministic review invariants."""

    def __init__(self, errors: list[str]):
        self.errors = sorted(set(errors))
        super().__init__("; ".join(self.errors))


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _required_targets(analysis: dict[str, Any]) -> list[dict[str, str]]:
    unresolved_facts = sorted(
        {
            fact_id
            for section in analysis.get("sections", [])
            for fact_id in section.get("unresolved_fact_ids", [])
        }
    )
    targets: list[dict[str, str]] = []
    targets.extend({"target_type": "fact", "target_id": value} for value in unresolved_facts)
    targets.extend({"target_type": "claim", "target_id": item["id"]} for item in analysis.get("claims", []))
    targets.extend({"target_type": "risk", "target_id": item["id"]} for item in analysis.get("risks", []))
    targets.extend({"target_type": "measure", "target_id": item["id"]} for item in analysis.get("measures", []))
    targets.extend({"target_type": "section", "target_id": item["id"]} for item in analysis.get("sections", []))
    order = {"fact": 0, "claim": 1, "risk": 2, "measure": 3, "section": 4}
    return sorted(targets, key=lambda item: (order[item["target_type"]], item["target_id"]))


def build_review_request(
    analysis_request: dict[str, Any],
    analysis: dict[str, Any],
    legal_context: dict[str, Any],
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    validate_dpia_analysis_request(analysis_request)
    validate_dpia_analysis_result(analysis)
    validate_legal_context_bundle(legal_context)
    validate_evidence_pack(analysis_request["evidence_pack"])

    errors: list[str] = []
    if analysis.get("request_id") != analysis_request["id"]:
        errors.append("analysis_request_id_mismatch")
    if analysis.get("validation_status") != "traceability_validated":
        errors.append("analysis_not_traceability_validated")
    if analysis.get("human_review_required") is not True:
        errors.append("analysis_does_not_require_human_review")
    if legal_context.get("status") != "ready":
        errors.append("legal_context_not_ready")
    if legal_context.get("request_id") != analysis_request["legal_context_request"]["id"]:
        errors.append("legal_context_request_id_mismatch")

    privacy = analysis_request["privacy_context"]
    if privacy.get("scrubbed") is not True:
        errors.append("review_input_not_scrubbed")
    if privacy.get("scrub_key_present") is not False:
        errors.append("scrub_key_must_not_enter_review_package")
    if privacy.get("contains_direct_identifiers") is not False:
        errors.append("direct_identifier_status_must_be_false_for_review_package")
    if errors:
        raise ReviewValidationError(errors)

    request = {
        "id": f"RR-{analysis_request['id']}",
        "case_id": analysis_request["case_id"],
        "analysis_request": copy.deepcopy(analysis_request),
        "analysis": copy.deepcopy(analysis),
        "legal_context": copy.deepcopy(legal_context),
        "required_review_targets": _required_targets(analysis),
        "snapshot_hashes": {
            "analysis_request": canonical_hash(analysis_request),
            "evidence_pack": canonical_hash(analysis_request["evidence_pack"]),
            "legal_context": canonical_hash(legal_context),
            "analysis": canonical_hash(analysis),
        },
        "generated_at": generated_at or _now(),
    }
    validate_dpia_review_request(request)
    return request


def verify_review_request_snapshot(review_request: dict[str, Any]) -> None:
    validate_dpia_review_request(review_request)
    expected = {
        "analysis_request": canonical_hash(review_request["analysis_request"]),
        "evidence_pack": canonical_hash(review_request["analysis_request"]["evidence_pack"]),
        "legal_context": canonical_hash(review_request["legal_context"]),
        "analysis": canonical_hash(review_request["analysis"]),
    }
    errors = [
        f"snapshot_hash_mismatch:{key}"
        for key, value in expected.items()
        if review_request["snapshot_hashes"].get(key) != value
    ]
    if errors:
        raise ReviewValidationError(errors)


def _evidence_index(review_request: dict[str, Any], decision_set: dict[str, Any]) -> dict[str, dict[str, Any]]:
    evidence = {}
    errors: list[str] = []
    for item in review_request["analysis_request"]["evidence_pack"].get("evidence", []):
        if item["id"] in evidence:
            errors.append(f"duplicate_original_evidence:{item['id']}")
        evidence[item["id"]] = item
    for item in decision_set.get("supplemental_evidence", []):
        if item["id"] in evidence:
            errors.append(f"supplemental_evidence_id_collision:{item['id']}")
        evidence[item["id"]] = item
    if errors:
        raise ReviewValidationError(errors)
    return evidence


def validate_review_decision_set(review_request: dict[str, Any], decision_set: dict[str, Any]) -> None:
    verify_review_request_snapshot(review_request)
    validate_dpia_review_decision_set(decision_set)
    errors: list[str] = []
    if decision_set["review_request_id"] != review_request["id"]:
        errors.append("review_request_id_mismatch")

    required = {(item["target_type"], item["target_id"]) for item in review_request["required_review_targets"]}
    seen: set[tuple[str, str]] = set()
    evidence = _evidence_index(review_request, decision_set)
    for decision in decision_set["decisions"]:
        key = (decision["target_type"], decision["target_id"])
        if key in seen:
            errors.append(f"duplicate_review_target:{key[0]}:{key[1]}")
        seen.add(key)
        if key not in required:
            errors.append(f"unknown_review_target:{key[0]}:{key[1]}")
        for evidence_id in decision.get("evidence_ids", []):
            if evidence_id not in evidence:
                errors.append(f"decision_unknown_evidence:{key[0]}:{key[1]}:{evidence_id}")
        if key[0] == "section" and decision["action"] == "change" and not isinstance(decision["replacement"], str):
            errors.append(f"section_change_requires_text_replacement:{key[1]}")

    analysis = review_request["analysis"]
    questions = set(analysis.get("open_questions", []))
    seen_questions: set[str] = set()
    for resolution in decision_set["question_resolutions"]:
        question = resolution["question"]
        if question in seen_questions:
            errors.append(f"duplicate_question_resolution:{question}")
        seen_questions.add(question)
        if question not in questions:
            errors.append(f"unknown_question_resolution:{question}")
        for evidence_id in resolution["evidence_ids"]:
            if evidence_id not in evidence:
                errors.append(f"question_resolution_unknown_evidence:{evidence_id}")
        if resolution["status"] == "resolved" and not resolution["evidence_ids"]:
            errors.append(f"resolved_question_requires_evidence:{question}")

    assumptions = set(analysis.get("assumptions", []))
    seen_assumptions: set[str] = set()
    for resolution in decision_set["assumption_resolutions"]:
        assumption = resolution["assumption"]
        if assumption in seen_assumptions:
            errors.append(f"duplicate_assumption_resolution:{assumption}")
        seen_assumptions.add(assumption)
        if assumption not in assumptions:
            errors.append(f"unknown_assumption_resolution:{assumption}")
        for evidence_id in resolution["evidence_ids"]:
            if evidence_id not in evidence:
                errors.append(f"assumption_resolution_unknown_evidence:{evidence_id}")

    for evidence_id in decision_set["dpo_consultation"]["evidence_ids"]:
        if evidence_id not in evidence:
            errors.append(f"dpo_consultation_unknown_evidence:{evidence_id}")
    if decision_set["dpo_consultation"]["status"] in {"not_designated", "designated_and_consulted"} and not decision_set["dpo_consultation"]["evidence_ids"]:
        errors.append("resolved_dpo_status_requires_evidence")

    legal_rules = {item["id"] for item in review_request["legal_context"]["rules"]}
    for rule_id in decision_set["residual_risk"]["source_rule_ids"]:
        if rule_id not in legal_rules:
            errors.append(f"residual_risk_unknown_rule:{rule_id}")

    if errors:
        raise ReviewValidationError(errors)


def _derive_status_and_issues(review_request: dict[str, Any], decision_set: dict[str, Any]) -> tuple[str, list[str]]:
    disposition = decision_set["overall_disposition"]
    if disposition == "reject":
        return "rejected", ["reviewer_rejected_draft"]

    issues: list[str] = []
    if disposition == "request_revision":
        issues.append("reviewer_requested_revision")

    required = {(item["target_type"], item["target_id"]) for item in review_request["required_review_targets"]}
    decisions = {(item["target_type"], item["target_id"]): item for item in decision_set["decisions"]}
    if disposition == "approve":
        for target in sorted(required):
            if target not in decisions:
                issues.append(f"missing_decision:{target[0]}:{target[1]}")
        for key, decision in decisions.items():
            if decision["action"] == "reject":
                issues.append(f"rejected:{key[0]}:{key[1]}")
            elif decision["action"] == "request_evidence":
                issues.append(f"evidence_requested:{key[0]}:{key[1]}")

        questions = set(review_request["analysis"].get("open_questions", []))
        resolutions = {item["question"]: item for item in decision_set["question_resolutions"]}
        for question in sorted(questions):
            if question not in resolutions:
                issues.append(f"missing_question_resolution:{question}")
            elif resolutions[question]["status"] == "open":
                issues.append(f"open_question:{question}")

        assumptions = set(review_request["analysis"].get("assumptions", []))
        assumption_resolutions = {item["assumption"]: item for item in decision_set["assumption_resolutions"]}
        for assumption in sorted(assumptions):
            if assumption not in assumption_resolutions:
                issues.append(f"missing_assumption_resolution:{assumption}")
            elif assumption_resolutions[assumption]["status"] == "open":
                issues.append(f"open_assumption:{assumption}")

        residual = decision_set["residual_risk"]
        if residual["level"] == "unknown":
            issues.append("residual_risk_unknown")
        if residual["prior_consultation_disposition"] == "needs_legal_review":
            issues.append("prior_consultation_needs_legal_review")
        if residual["level"] == "high" and residual["prior_consultation_disposition"] == "not_required":
            issues.append("high_residual_risk_cannot_skip_prior_consultation_review")
        if decision_set["dpo_consultation"]["status"] == "unknown":
            issues.append("dpo_status_unknown")

    if issues:
        return "needs_revision", sorted(set(issues))

    changed = any(item["action"] == "change" for item in decision_set["decisions"])
    if decision_set["residual_risk"]["prior_consultation_disposition"] == "required":
        return "approved_pending_prior_consultation", []
    return ("approved_with_changes" if changed else "approved"), []


def _source_appendix(review_request: dict[str, Any], decision_set: dict[str, Any]) -> list[dict[str, Any]]:
    analysis = review_request["analysis"]
    rule_ids = {
        rule_id
        for section in analysis.get("sections", [])
        for rule_id in section.get("legal_rule_ids", [])
    }
    rule_ids.update(
        rule_id
        for claim in analysis.get("claims", [])
        for rule_id in claim.get("rule_ids", [])
    )
    rule_ids.update(
        rule_id
        for risk in analysis.get("risks", [])
        for rule_id in risk.get("legal_rule_ids", [])
    )
    rule_ids.update(decision_set["residual_risk"]["source_rule_ids"])
    rules = {item["id"]: item for item in review_request["legal_context"]["rules"]}
    appendix = []
    for rule_id in sorted(rule_ids):
        rule = rules[rule_id]
        appendix.append({
            "rule_id": rule_id,
            "source_id": rule["source_id"],
            "title": rule["source_title"],
            "authority": rule["authority"],
            "locator": rule["locator"],
            "canonical_url": rule["canonical_url"],
            "classification": rule["classification"],
        })
    return appendix


def _evidence_appendix(review_request: dict[str, Any], decision_set: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = _evidence_index(review_request, decision_set)
    analysis = review_request["analysis"]
    fact_ids = {
        fact_id
        for section in analysis.get("sections", [])
        for fact_id in section.get("fact_ids", [])
    }
    fact_ids.update(
        fact_id for claim in analysis.get("claims", []) for fact_id in claim.get("fact_ids", [])
    )
    fact_ids.update(
        fact_id for risk in analysis.get("risks", []) for fact_id in risk.get("fact_ids", [])
    )
    facts = {item["id"]: item for item in review_request["analysis_request"]["evidence_pack"]["facts"]}
    used_evidence = {
        evidence_id
        for fact_id in fact_ids
        if fact_id in facts
        for evidence_id in facts[fact_id].get("evidence_ids", [])
    }
    used_evidence.update(
        evidence_id for decision in decision_set["decisions"] for evidence_id in decision.get("evidence_ids", [])
    )
    used_evidence.update(
        evidence_id for item in decision_set["question_resolutions"] for evidence_id in item["evidence_ids"]
    )
    used_evidence.update(
        evidence_id for item in decision_set["assumption_resolutions"] for evidence_id in item["evidence_ids"]
    )
    used_evidence.update(decision_set["dpo_consultation"]["evidence_ids"])
    return [
        {
            "evidence_id": evidence_id,
            "kind": evidence[evidence_id]["kind"],
            "source": evidence[evidence_id]["source"],
            "locator": evidence[evidence_id]["locator"],
            "contains_personal_data": evidence[evidence_id].get("contains_personal_data", False),
        }
        for evidence_id in sorted(used_evidence)
    ]


def _report_body(review_request: dict[str, Any], decision_set: dict[str, Any], source_appendix: list[dict[str, Any]], evidence_appendix: list[dict[str, Any]]) -> str:
    analysis = review_request["analysis"]
    decisions = {(item["target_type"], item["target_id"]): item for item in decision_set["decisions"]}
    lines = ["# DPIA — reviewed draft", "", "## Management summary", "", decision_set["management_summary"], "", "## Reviewed sections", ""]
    for section in analysis["sections"]:
        decision = decisions.get(("section", section["id"]))
        narrative = section["narrative"]
        if decision and decision["action"] == "change":
            narrative = decision["replacement"]
        lines.extend([f"### {section['title']}", "", narrative, ""])
    residual = decision_set["residual_risk"]
    lines.extend([
        "## Human residual-risk conclusion", "",
        f"Level: {residual['level']}", "",
        residual["rationale"], "",
        f"Prior consultation: {residual['prior_consultation_disposition']}", "",
        residual["prior_consultation_rationale"], "",
        "## Review decisions", "",
    ])
    for decision in decision_set["decisions"]:
        text = f"- {decision['target_type']} `{decision['target_id']}`: **{decision['action']}**"
        if decision.get("rationale"):
            text += f" — {decision['rationale']}"
        lines.append(text)
    lines.extend(["", "## Governed legal sources", ""])
    for item in source_appendix:
        lines.append(f"- {item['rule_id']} — {item['title']}, {item['locator']}")
    lines.extend(["", "## Evidence references", ""])
    for item in evidence_appendix:
        lines.append(f"- {item['evidence_id']} — {item['source']} ({item['locator']})")
    return "\n".join(lines).strip() + "\n"


def _build_audit_record(review_request: dict[str, Any], decision_set: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": f"AUDIT-{review_request['id']}",
        "review_request_id": review_request["id"],
        "review_request_hash": canonical_hash(review_request),
        "analysis_request_hash": review_request["snapshot_hashes"]["analysis_request"],
        "evidence_pack_hash": review_request["snapshot_hashes"]["evidence_pack"],
        "legal_context_hash": review_request["snapshot_hashes"]["legal_context"],
        "analysis_hash": review_request["snapshot_hashes"]["analysis"],
        "decision_set_hash": canonical_hash(decision_set),
        "reviewer_id": decision_set["reviewer"]["reviewer_id"],
        "reviewer_role": decision_set["reviewer"]["role"],
        "signed_at": decision_set["signed_at"],
        "runtime_version": __version__,
    }
    record["record_hash"] = canonical_hash(record)
    validate_review_audit_record(record)
    return record


def verify_audit_record(audit_record: dict[str, Any], review_request: dict[str, Any], decision_set: dict[str, Any]) -> None:
    validate_review_audit_record(audit_record)
    expected = _build_audit_record(review_request, decision_set)
    if audit_record != expected:
        raise ReviewValidationError(["audit_record_does_not_match_review_inputs"])


def finalize_dpia_review(review_request: dict[str, Any], decision_set: dict[str, Any]) -> dict[str, Any]:
    validate_review_decision_set(review_request, decision_set)
    status, unresolved_issues = _derive_status_and_issues(review_request, decision_set)
    source_appendix = _source_appendix(review_request, decision_set)
    evidence_appendix = _evidence_appendix(review_request, decision_set)
    report = None
    handoff = None
    if status in {"approved", "approved_with_changes", "approved_pending_prior_consultation"}:
        report_id = f"REPORT-{review_request['case_id']}"
        report = {
            "id": report_id,
            "format": "markdown",
            "management_summary": decision_set["management_summary"],
            "body": _report_body(review_request, decision_set, source_appendix, evidence_appendix),
            "privacy_context": {
                "scrubbed": True,
                "scrub_key_present": False,
                "contains_direct_identifiers": False,
            },
            "generated_at": decision_set["signed_at"],
        }
        handoff = {
            "id": f"REINSERT-{review_request['case_id']}",
            "mode": "local_scrub_reinsert",
            "scrubbed_report_id": report_id,
            "local_reinsert_required": True,
            "scrub_key_included": False,
            "replacement_mapping_included": False,
            "contains_direct_identifiers": False,
        }
    package = {
        "id": f"REVIEWED-{review_request['case_id']}",
        "review_request_id": review_request["id"],
        "case_id": review_request["case_id"],
        "status": status,
        "reviewer": copy.deepcopy(decision_set["reviewer"]),
        "decisions": copy.deepcopy(decision_set["decisions"]),
        "overall_rationale": decision_set["overall_rationale"],
        "unresolved_issues": unresolved_issues,
        "residual_risk": copy.deepcopy(decision_set["residual_risk"]),
        "dpo_consultation": copy.deepcopy(decision_set["dpo_consultation"]),
        "source_appendix": source_appendix,
        "evidence_appendix": evidence_appendix,
        "report": report,
        "reinsert_handoff": handoff,
        "audit_record": _build_audit_record(review_request, decision_set),
        "signed_at": decision_set["signed_at"],
    }
    validate_dpia_review_package(package)
    return package
