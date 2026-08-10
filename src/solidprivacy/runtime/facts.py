from __future__ import annotations

from collections import Counter
from typing import Any


class EvidencePackIntegrityError(ValueError):
    """Raised when an evidence pack is structurally valid but semantically inconsistent."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def evidence_pack_integrity_errors(pack: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    evidence = pack.get("evidence", [])
    facts = pack.get("facts", [])
    contradictions = pack.get("contradictions", [])
    missing = pack.get("missing_information", [])

    evidence_ids = [item.get("id") for item in evidence if item.get("id")]
    fact_ids = [item.get("id") for item in facts if item.get("id")]
    contradiction_ids = [item.get("id") for item in contradictions if item.get("id")]
    missing_ids = [item.get("id") for item in missing if item.get("id")]

    for label, values in (
        ("evidence", evidence_ids),
        ("facts", fact_ids),
        ("contradictions", contradiction_ids),
        ("missing_information", missing_ids),
    ):
        for duplicate in _duplicates(values):
            errors.append(f"{label}: duplicate id {duplicate!r}")

    evidence_id_set = set(evidence_ids)
    fact_id_set = set(fact_ids)

    for index, fact in enumerate(facts):
        for evidence_id in fact.get("evidence_ids", []):
            if evidence_id not in evidence_id_set:
                errors.append(
                    f"facts[{index}].evidence_ids: unknown evidence reference {evidence_id!r}"
                )

        epistemic = fact.get("epistemic_status")
        review = fact.get("review_status")
        if epistemic == "assumption" and review == "accepted":
            errors.append(
                f"facts[{index}].review_status: assumptions may not be accepted as established facts"
            )

    for index, contradiction in enumerate(contradictions):
        for fact_id in contradiction.get("fact_ids", []):
            if fact_id not in fact_id_set:
                errors.append(
                    f"contradictions[{index}].fact_ids: unknown fact reference {fact_id!r}"
                )
        if contradiction.get("status") == "resolved" and not contradiction.get("resolution"):
            errors.append(
                f"contradictions[{index}].resolution: resolved contradiction requires a resolution"
            )

    for index, item in enumerate(missing):
        if item.get("status") == "resolved" and not item.get("resolution"):
            errors.append(
                f"missing_information[{index}].resolution: resolved item requires a resolution"
            )

    claimed = pack.get("readiness", {})
    stage = claimed.get("stage")
    if stage in {"analysis", "finalisation"}:
        derived = derive_readiness(pack, stage)
        if claimed.get("status") != derived["status"]:
            errors.append(
                "readiness.status: claimed "
                f"{claimed.get('status')!r} but deterministic status is {derived['status']!r}"
            )
        if sorted(claimed.get("blockers", [])) != sorted(derived["blockers"]):
            errors.append(
                "readiness.blockers: claimed blockers do not match deterministic blockers"
            )

    return errors


def derive_readiness(pack: dict[str, Any], stage: str) -> dict[str, Any]:
    if stage not in {"analysis", "finalisation"}:
        raise ValueError(f"unsupported readiness stage {stage!r}")

    blockers: list[str] = []
    review_signals: list[str] = []

    for contradiction in pack.get("contradictions", []):
        token = f"contradiction:{contradiction.get('id')}"
        if contradiction.get("status") == "open":
            if contradiction.get("severity") in {"high", "critical"}:
                blockers.append(token)
            else:
                review_signals.append(token)
        elif contradiction.get("status") == "accepted_uncertainty":
            review_signals.append(token)

    for item in pack.get("missing_information", []):
        if item.get("status") != "open":
            continue
        blocks_stage = item.get("blocks_stage", "none")
        applies = (
            blocks_stage == "analysis"
            or (stage == "finalisation" and blocks_stage == "finalisation")
        )
        token = f"missing:{item.get('id')}"
        if applies and item.get("criticality") in {"high", "critical"}:
            blockers.append(token)
        else:
            review_signals.append(token)

    for fact in pack.get("facts", []):
        fact_id = fact.get("id")
        review_status = fact.get("review_status")
        epistemic = fact.get("epistemic_status")
        if review_status in {"pending", "needs_clarification"}:
            review_signals.append(f"fact-review:{fact_id}")
        if stage == "finalisation" and epistemic == "assumption":
            blockers.append(f"assumption:{fact_id}")
        if stage == "finalisation" and review_status == "rejected":
            blockers.append(f"rejected-fact:{fact_id}")

    blockers = sorted(set(blockers))
    review_signals = sorted(set(review_signals))

    if blockers:
        status = "blocked"
        rationale = "Unresolved blockers prevent progression to this stage."
    elif review_signals:
        status = "needs_review"
        rationale = "No hard blocker remains, but unresolved review signals require attention."
    else:
        status = "ready"
        rationale = "Evidence, facts and known uncertainties satisfy the deterministic readiness gate."

    return {
        "stage": stage,
        "status": status,
        "blockers": blockers,
        "review_signals": review_signals,
        "rationale": rationale,
    }


def validate_evidence_pack_integrity(pack: dict[str, Any]) -> None:
    errors = evidence_pack_integrity_errors(pack)
    if errors:
        raise EvidencePackIntegrityError(errors)
