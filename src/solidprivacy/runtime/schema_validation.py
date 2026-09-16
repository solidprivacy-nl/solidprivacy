from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class ContractValidationError(ValueError):
    """Raised when a SolidPrivacy JSON contract is invalid."""

    def __init__(self, schema_name: str, errors: list[str]):
        self.schema_name = schema_name
        self.errors = errors
        super().__init__(f"{schema_name} validation failed: " + "; ".join(errors))


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def contracts_dir() -> Path:
    return repository_root() / "contracts"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(schema_name: str) -> dict[str, Any]:
    return load_json(contracts_dir() / schema_name)


def build_registry() -> Registry:
    registry = Registry()
    for path in sorted(contracts_dir().glob("*.schema.json")):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def validation_errors(schema_name: str, instance: Any) -> list[str]:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema, registry=build_registry())
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        path = "$"
        if error.absolute_path:
            path += "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}"
                for part in error.absolute_path
            )
        errors.append(f"{path}: {error.message}")
    return errors


def validate_contract(schema_name: str, instance: Any) -> None:
    errors = validation_errors(schema_name, instance)
    if errors:
        raise ContractValidationError(schema_name, errors)


def reviewable_content_sha256(instance: dict[str, Any]) -> str:
    """Stable identity for the professional content, excluding mutable review/state metadata."""
    payload = {
        key: value
        for key, value in instance.items()
        if key not in {"human_review", "status"}
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _structured_source_reference_ids(value: Any) -> set[str]:
    """Collect IDs only from full SourceReference-shaped objects, not loose source_id fields."""
    found: set[str] = set()
    if isinstance(value, dict):
        source_fields = {"source_id", "source_status", "jurisdiction", "version", "verified_at", "locator"}
        if source_fields.issubset(value):
            source_id = value.get("source_id")
            if isinstance(source_id, str) and source_id:
                found.add(source_id)
        for child in value.values():
            found.update(_structured_source_reference_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_structured_source_reference_ids(child))
    return found


def _dpia_provenance_errors(instance: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    evidence = instance.get("evidence", [])
    evidence_ids = [
        item.get("id")
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("$.evidence: evidence ids must be unique")
    known_evidence_ids = set(evidence_ids)

    for index, measure in enumerate(instance.get("measures", [])):
        if not isinstance(measure, dict):
            continue
        for evidence_ref in measure.get("evidence_refs", []):
            if evidence_ref not in known_evidence_ids:
                errors.append(
                    f"$.measures[{index}].evidence_refs: unresolved evidence reference {evidence_ref!r}"
                )

    source_ids = _structured_source_reference_ids({
        key: value
        for key, value in instance.items()
        if key != "human_review"
    })
    for index, claim in enumerate(instance.get("legal_claims", [])):
        if not isinstance(claim, dict):
            continue
        source_id = claim.get("source_id")
        if source_id not in source_ids:
            errors.append(
                f"$.legal_claims[{index}].source_id: unresolved structured source reference {source_id!r}"
            )

    return errors


def _dpia_review_errors(instance: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    review = instance.get("human_review")
    if not isinstance(review, dict):
        return errors

    review_required = review.get("required") is True
    review_status = review.get("status")
    review_complete = review_status in {"approved", "approved_with_changes"}
    final_approved = review_status == "approved"

    if review_required and review_status == "not_required":
        errors.append("$.human_review: required review cannot be marked not_required")

    if instance.get("status") == "final" and not (review_required and final_approved):
        errors.append("$.human_review: final DPIA requires approved human professional review")

    if not review_complete:
        return errors

    artifact_id = instance.get("id")
    artifact_version = instance.get("artifact_version")
    if not isinstance(artifact_version, str) or not artifact_version:
        errors.append("$.artifact_version: approved review requires an exact artifact version")
    if review.get("reviewed_artifact_id") != artifact_id:
        errors.append("$.human_review.reviewed_artifact_id: does not match DPIA id")
    if review.get("reviewed_artifact_version") != artifact_version:
        errors.append("$.human_review.reviewed_artifact_version: does not match current artifact version")

    expected_hash = reviewable_content_sha256(instance)
    if review.get("reviewed_content_sha256") != expected_hash:
        errors.append("$.human_review.reviewed_content_sha256: stale or mismatched reviewed content")

    evidence_ids = {
        item.get("id")
        for item in instance.get("evidence", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    reviewed_evidence_ids = review.get("evidence_ids")
    if not isinstance(reviewed_evidence_ids, list) or set(reviewed_evidence_ids) != evidence_ids:
        errors.append("$.human_review.evidence_ids: must exactly bind current evidence provenance")

    source_ids = _structured_source_reference_ids({
        key: value
        for key, value in instance.items()
        if key != "human_review"
    })
    reviewed_source_ids = review.get("source_reference_ids")
    if not isinstance(reviewed_source_ids, list) or set(reviewed_source_ids) != source_ids:
        errors.append("$.human_review.source_reference_ids: must exactly bind current source provenance")

    return errors


def validate_dpia(instance: Any) -> None:
    validate_contract("dpia_assessment.schema.json", instance)
    if not isinstance(instance, dict):
        return
    errors = _dpia_provenance_errors(instance) + _dpia_review_errors(instance)
    if errors:
        raise ContractValidationError("dpia_assessment.schema.json", errors)


def validate_prescan_input(instance: Any) -> None:
    validate_contract("prescan_input.schema.json", instance)


def validate_prescan_decision(instance: Any) -> None:
    validate_contract("prescan_decision.schema.json", instance)
