from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from solidprivacy.runtime.schema_validation import (
    validate_fact_extraction_request,
    validate_model_call_policy,
)


CLASSIFICATION_RANK = {
    "public": 0,
    "internal": 1,
    "scrubbed_personal_data": 2,
    "personal_data": 3,
    "special_category": 4,
}


class ModelCallPolicyError(ValueError):
    """Raised when a proposed model call violates the approved privacy boundary."""

    def __init__(self, reasons: list[str]):
        self.reasons = reasons
        super().__init__("; ".join(reasons))


@dataclass(frozen=True)
class ModelCallDecision:
    allowed: bool
    policy_id: str
    provider: str
    model: str
    reasons: tuple[str, ...]


def evaluate_model_call_policy(request: dict[str, Any], policy: dict[str, Any]) -> ModelCallDecision:
    validate_fact_extraction_request(request)
    validate_model_call_policy(policy)

    reasons: list[str] = []
    privacy = request["privacy_context"]
    classification = privacy["content_classification"]

    if not policy["approved"]:
        reasons.append("policy_not_approved")
    if request["task"] not in policy["allowed_tasks"]:
        reasons.append("task_not_allowed")
    if request["requested_provider"] != policy["provider"]:
        reasons.append("provider_not_approved")
    if request["requested_model"] != policy["model"]:
        reasons.append("model_not_approved")
    if privacy["scrub_key_present"]:
        reasons.append("scrub_key_must_never_be_sent_to_model")
    if policy["require_scrubbed"] and not privacy["scrubbed"]:
        reasons.append("input_not_scrubbed")
    if CLASSIFICATION_RANK[classification] > CLASSIFICATION_RANK[policy["max_content_classification"]]:
        reasons.append("content_classification_exceeds_policy")

    if policy["execution_mode"] == "external":
        direct_identifiers = privacy.get("contains_direct_identifiers")
        if direct_identifiers is True:
            reasons.append("direct_identifiers_must_not_leave_scrub_boundary")
        elif CLASSIFICATION_RANK[classification] >= CLASSIFICATION_RANK["scrubbed_personal_data"] and direct_identifiers is not False:
            reasons.append("direct_identifier_status_not_safely_resolved")

        if direct_identifiers is True and classification in {"public", "internal", "scrubbed_personal_data"}:
            reasons.append("content_classification_inconsistent_with_direct_identifiers")

        if classification == "scrubbed_personal_data" and not policy["allow_scrubbed_personal_data_egress"]:
            reasons.append("scrubbed_personal_data_egress_not_allowed")
        if classification in {"personal_data", "special_category"} and not policy["allow_personal_data_egress"]:
            reasons.append("personal_data_egress_not_allowed")
        if classification == "special_category" and not policy["allow_special_category_egress"]:
            reasons.append("special_category_egress_not_allowed")

        if policy["provider_training_use"] not in {"disabled", "contractually_disabled"}:
            reasons.append("provider_training_use_not_safely_resolved")
        if policy["provider_retention"] in {"unknown", "indefinite"}:
            reasons.append("provider_retention_not_safely_resolved")
        if classification in {"scrubbed_personal_data", "personal_data", "special_category"} and policy["logging_policy"] in {"content_allowed", "unknown"}:
            reasons.append("content_logging_not_allowed_for_sensitive_input")

    return ModelCallDecision(
        allowed=not reasons,
        policy_id=policy["id"],
        provider=policy["provider"],
        model=policy["model"],
        reasons=tuple(sorted(set(reasons))),
    )


def enforce_model_call_policy(request: dict[str, Any], policy: dict[str, Any]) -> ModelCallDecision:
    decision = evaluate_model_call_policy(request, policy)
    if not decision.allowed:
        raise ModelCallPolicyError(list(decision.reasons))
    return decision
