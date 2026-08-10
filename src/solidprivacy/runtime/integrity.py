from __future__ import annotations

from collections import Counter
from typing import Any


class IntegrityError(ValueError):
    """Raised when references inside a canonical privacy object do not resolve."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _check_refs(errors: list[str], values: list[str] | None, valid: set[str], path: str) -> None:
    for value in values or []:
        if value not in valid:
            errors.append(f"{path}: unknown reference {value!r}")


def dpia_integrity_errors(dpia: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    activities = dpia.get("processing_activities", [])
    activity_ids = [item.get("id") for item in activities if item.get("id")]
    for duplicate in _duplicates(activity_ids):
        errors.append(f"processing_activities: duplicate id {duplicate!r}")
    activity_id_set = set(activity_ids)

    global_subject_ids: set[str] = set()
    global_personal_data_ids: set[str] = set()

    for index, activity in enumerate(activities):
        prefix = f"processing_activities[{index}]"
        subjects = activity.get("data_subjects", [])
        personal_data = activity.get("personal_data", [])
        purposes = activity.get("purposes", [])
        parties = activity.get("parties", [])

        subject_ids = [item.get("id") for item in subjects if item.get("id")]
        personal_data_ids = [item.get("id") for item in personal_data if item.get("id")]
        purpose_ids = [item.get("id") for item in purposes if item.get("id")]
        party_ids = [item.get("id") for item in parties if item.get("id")]

        for label, values in (
            ("data_subjects", subject_ids),
            ("personal_data", personal_data_ids),
            ("purposes", purpose_ids),
            ("parties", party_ids),
        ):
            for duplicate in _duplicates(values):
                errors.append(f"{prefix}.{label}: duplicate id {duplicate!r}")

        local_subjects = set(subject_ids)
        local_personal_data = set(personal_data_ids)
        local_purposes = set(purpose_ids)

        for pd_index, item in enumerate(personal_data):
            _check_refs(errors, item.get("data_subject_ids"), local_subjects, f"{prefix}.personal_data[{pd_index}].data_subject_ids")

        for retention_index, item in enumerate(activity.get("retention", [])):
            _check_refs(errors, item.get("purpose_ids"), local_purposes, f"{prefix}.retention[{retention_index}].purpose_ids")
            _check_refs(errors, item.get("data_subject_ids"), local_subjects, f"{prefix}.retention[{retention_index}].data_subject_ids")
            _check_refs(errors, item.get("personal_data_ids"), local_personal_data, f"{prefix}.retention[{retention_index}].personal_data_ids")

        global_subject_ids.update(local_subjects)
        global_personal_data_ids.update(local_personal_data)

    risk_ids = [item.get("id") for item in dpia.get("risks", []) if item.get("id")]
    for duplicate in _duplicates(risk_ids):
        errors.append(f"risks: duplicate id {duplicate!r}")
    risk_id_set = set(risk_ids)

    for index, risk in enumerate(dpia.get("risks", [])):
        _check_refs(errors, risk.get("processing_activity_ids"), activity_id_set, f"risks[{index}].processing_activity_ids")
        _check_refs(errors, risk.get("affected_data_subjects"), global_subject_ids, f"risks[{index}].affected_data_subjects")

    evidence_ids = {item.get("id") for item in dpia.get("evidence", []) if item.get("id")}

    for index, measure in enumerate(dpia.get("measures", [])):
        _check_refs(errors, measure.get("risk_ids"), risk_id_set, f"measures[{index}].risk_ids")
        _check_refs(errors, measure.get("evidence_refs"), evidence_ids, f"measures[{index}].evidence_refs")

    for index, item in enumerate(dpia.get("purpose_compatibility", [])):
        activity_id = item.get("processing_activity_id")
        if activity_id and activity_id not in activity_id_set:
            errors.append(f"purpose_compatibility[{index}].processing_activity_id: unknown reference {activity_id!r}")

    for index, item in enumerate(dpia.get("special_data_assessment", [])):
        _check_refs(errors, item.get("processing_activity_ids"), activity_id_set, f"special_data_assessment[{index}].processing_activity_ids")
        _check_refs(errors, item.get("personal_data_ids"), global_personal_data_ids, f"special_data_assessment[{index}].personal_data_ids")
        _check_refs(errors, item.get("data_subject_ids"), global_subject_ids, f"special_data_assessment[{index}].data_subject_ids")

    residual = dpia.get("residual_risk_conclusion", {})
    review = dpia.get("human_review", {})
    if residual.get("level") == "high":
        if residual.get("prior_consultation_required") is False:
            errors.append("residual_risk_conclusion.prior_consultation_required: must not be false while residual risk is high")
        if not review.get("required"):
            errors.append("human_review.required: must be true while residual risk is high")
        if review.get("status") in {"approved", "approved_with_changes"}:
            errors.append("human_review.status: high residual risk cannot be treated as approved without resolving the high-risk gate")

    return errors


def validate_dpia_integrity(dpia: dict[str, Any]) -> None:
    errors = dpia_integrity_errors(dpia)
    if errors:
        raise IntegrityError(errors)
