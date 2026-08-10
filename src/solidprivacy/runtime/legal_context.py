from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from solidprivacy.runtime.schema_validation import (
    validate_legal_context_bundle,
    validate_legal_context_request,
    validate_legal_rule,
)

LAW_SOURCE_KINDS = {"binding_law", "regulator_decision"}
GUIDANCE_SOURCE_KINDS = {"regulator_guidance"}


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def _normalise_yaml_scalars(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalise_yaml_scalars(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalise_yaml_scalars(item) for item in value]
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return _normalise_yaml_scalars(yaml.safe_load(handle))


def load_source_registry() -> dict[str, Any]:
    return _load_yaml(_root() / "legal_sources" / "source_registry.yaml")


def load_rule_registry() -> dict[str, Any]:
    return _load_yaml(_root() / "legal_sources" / "rules" / "dpia_core.yaml")


def _days_old(value: str, as_of: str) -> int:
    return (date.fromisoformat(as_of) - date.fromisoformat(value)).days


def _jurisdiction_allowed(item_jurisdiction: str, requested: set[str]) -> bool:
    if item_jurisdiction in requested:
        return True
    if item_jurisdiction == "EU/EEA" and any(j in requested for j in {"EU/EEA", "NL"}):
        return True
    return False


def validate_rule_registry_integrity(source_registry: dict[str, Any] | None = None, rule_registry: dict[str, Any] | None = None) -> list[str]:
    source_registry = source_registry or load_source_registry()
    rule_registry = rule_registry or load_rule_registry()
    sources = {item["id"]: item for item in source_registry.get("sources", [])}
    errors: list[str] = []
    seen: set[str] = set()
    for rule in rule_registry.get("rules", []):
        validate_legal_rule(rule)
        if rule["id"] in seen:
            errors.append(f"duplicate_rule_id:{rule['id']}")
        seen.add(rule["id"])
        source = sources.get(rule["source_id"])
        if not source:
            errors.append(f"unknown_rule_source:{rule['id']}:{rule['source_id']}")
            continue
        if rule["classification"] == "LAW_REQUIRED":
            if source.get("status") != "authoritative" or source.get("kind") not in LAW_SOURCE_KINDS:
                errors.append(f"law_rule_not_backed_by_binding_or_decision_source:{rule['id']}")
        elif rule["classification"] == "REGULATOR_GUIDANCE":
            if source.get("status") != "authoritative_guidance" or source.get("kind") not in GUIDANCE_SOURCE_KINDS:
                errors.append(f"guidance_rule_not_backed_by_guidance_source:{rule['id']}")
    return sorted(set(errors))


def _context_use_mode(source: dict[str, Any], include_nonfinal: bool) -> tuple[str, str | None]:
    status = source.get("status")
    if status in {"authoritative", "authoritative_guidance"}:
        return "authoritative_context", None
    if status == "official_methodology":
        return "official_methodology", None
    if status == "consultation_closed_pending_finalisation":
        if include_nonfinal:
            return "forward_context_only", "non_final_source_must_not_support_legal_claims"
        return "excluded", "non_final_context_not_requested"
    if status == "standard_reference":
        return "reference_only", "reference_source_is_not_eu_nl_legal_authority"
    if status == "licensed_standard_required_for_normative_detail":
        return "excluded", "licensed_normative_content_not_available_in_bundle"
    return "excluded", f"unsupported_source_status:{status}"


def resolve_legal_context(request: dict[str, Any]) -> dict[str, Any]:
    validate_legal_context_request(request)
    source_registry = load_source_registry()
    rule_registry = load_rule_registry()
    registry_errors = validate_rule_registry_integrity(source_registry, rule_registry)
    sources = {item["id"]: item for item in source_registry.get("sources", [])}
    rules = {item["id"]: item for item in rule_registry.get("rules", [])}
    requested_jurisdictions = set(request["jurisdiction"])
    blockers = list(registry_errors)
    warnings: list[str] = []
    resolved_rules: list[dict[str, Any]] = []
    for rule_id in request["required_rule_ids"]:
        rule = rules.get(rule_id)
        if not rule:
            blockers.append(f"required_rule_missing:{rule_id}")
            continue
        source = sources.get(rule["source_id"])
        if not source:
            blockers.append(f"required_rule_source_missing:{rule_id}:{rule['source_id']}")
            continue
        if not _jurisdiction_allowed(rule["jurisdiction"], requested_jurisdictions):
            blockers.append(f"rule_jurisdiction_not_applicable:{rule_id}:{rule['jurisdiction']}")
            continue
        if not _jurisdiction_allowed(source.get("jurisdiction", ""), requested_jurisdictions):
            blockers.append(f"source_jurisdiction_not_applicable:{rule_id}:{source.get('jurisdiction')}")
            continue
        for label, verified in (("source", source.get("last_verified")), ("rule", rule.get("last_verified"))):
            if not verified:
                blockers.append(f"{label}_verification_missing:{rule_id}")
                continue
            age = _days_old(str(verified), request["as_of"])
            if age < 0:
                blockers.append(f"{label}_verification_after_as_of:{rule_id}")
            elif age > request["max_verification_age_days"]:
                blockers.append(f"{label}_verification_stale:{rule_id}:{age}d")
        resolved_rules.append({"id":rule["id"],"source_id":source["id"],"source_title":source["title"],"authority":source["authority"],"source_kind":source["kind"],"source_status":source["status"],"jurisdiction":rule["jurisdiction"],"locator":rule["locator"],"classification":rule["classification"],"statement":rule["statement"],"canonical_url":source["canonical_url"],"source_last_verified":str(source["last_verified"]),"rule_last_verified":str(rule["last_verified"])})
    context_sources: list[dict[str, Any]] = []
    for source_id in request["optional_source_ids"]:
        source = sources.get(source_id)
        if not source:
            warnings.append(f"optional_source_missing:{source_id}")
            continue
        if not _jurisdiction_allowed(source.get("jurisdiction", ""), requested_jurisdictions):
            warnings.append(f"optional_source_jurisdiction_not_applicable:{source_id}")
            continue
        use_mode, reason = _context_use_mode(source, request["include_nonfinal_context"])
        verified = str(source.get("last_verified", ""))
        if not verified:
            warnings.append(f"optional_source_verification_missing:{source_id}")
        else:
            age = _days_old(verified, request["as_of"])
            if age < 0 or age > request["max_verification_age_days"]:
                warnings.append(f"optional_source_verification_outside_window:{source_id}:{age}d")
        if reason:
            warnings.append(f"{source_id}:{reason}")
        context_sources.append({"source_id":source["id"],"title":source["title"],"authority":source["authority"],"jurisdiction":source["jurisdiction"],"kind":source["kind"],"status":source["status"],"canonical_url":source["canonical_url"],"use_mode":use_mode,"last_verified":verified,"reason":reason})
    bundle = {"id":f"LCB-{request['id']}","request_id":request["id"],"status":"blocked" if blockers else "ready","jurisdiction":request["jurisdiction"],"as_of":request["as_of"],"rules":resolved_rules,"context_sources":context_sources,"warnings":sorted(set(warnings)),"blockers":sorted(set(blockers)),"registry_version":source_registry.get("version","unknown"),"rules_version":rule_registry.get("version","unknown")}
    validate_legal_context_bundle(bundle)
    return bundle
