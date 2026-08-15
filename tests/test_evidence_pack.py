from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from solidprivacy.runtime.facts import (
    EvidencePackIntegrityError,
    derive_readiness,
    validate_evidence_pack_integrity,
)
from solidprivacy.runtime.schema_validation import validate_evidence_pack


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "evidence_packs"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_ready_pack_validates_and_is_ready_for_analysis() -> None:
    pack = load("dpia_evidence_ready.json")
    validate_evidence_pack(pack)
    validate_evidence_pack_integrity(pack)
    result = derive_readiness(pack, "analysis")
    assert result["status"] == "ready"
    assert result["blockers"] == []


def test_blocked_pack_validates_and_is_blocked_for_analysis() -> None:
    pack = load("dpia_evidence_blocked.json")
    validate_evidence_pack(pack)
    validate_evidence_pack_integrity(pack)
    result = derive_readiness(pack, "analysis")
    assert result["status"] == "blocked"
    assert "contradiction:C-101" in result["blockers"]
    assert "missing:MI-101" in result["blockers"]


def test_unknown_evidence_reference_fails_integrity() -> None:
    pack = load("dpia_evidence_ready.json")
    pack["facts"][0]["evidence_ids"] = ["EV-DOES-NOT-EXIST"]
    with pytest.raises(EvidencePackIntegrityError):
        validate_evidence_pack_integrity(pack)


def test_duplicate_fact_id_fails_integrity() -> None:
    pack = load("dpia_evidence_ready.json")
    duplicate = copy.deepcopy(pack["facts"][0])
    pack["facts"].append(duplicate)
    with pytest.raises(EvidencePackIntegrityError):
        validate_evidence_pack_integrity(pack)


def test_assumption_blocks_finalisation() -> None:
    pack = load("dpia_evidence_blocked.json")
    pack["contradictions"][0]["status"] = "resolved"
    pack["contradictions"][0]["resolution"] = "Retention policy owner confirmed seven years."
    pack["missing_information"][0]["status"] = "resolved"
    pack["missing_information"][0]["resolution"] = "Public task basis confirmed by legal owner."
    for fact in pack["facts"]:
        if fact["review_status"] in {"pending", "needs_clarification"}:
            fact["review_status"] = "accepted" if fact["epistemic_status"] != "assumption" else "pending"

    result = derive_readiness(pack, "finalisation")
    assert result["status"] == "blocked"
    assert "assumption:F-103" in result["blockers"]


def test_false_ready_claim_fails_integrity() -> None:
    pack = load("dpia_evidence_blocked.json")
    pack["readiness"] = {
        "stage": "analysis",
        "status": "ready",
        "blockers": [],
        "rationale": "Incorrect claim for negative test.",
    }
    with pytest.raises(EvidencePackIntegrityError):
        validate_evidence_pack_integrity(pack)


def test_assumption_cannot_be_accepted_as_established_fact() -> None:
    pack = load("dpia_evidence_blocked.json")
    fact = next(item for item in pack["facts"] if item["epistemic_status"] == "assumption")
    fact["review_status"] = "accepted"
    with pytest.raises(EvidencePackIntegrityError):
        validate_evidence_pack_integrity(pack)


def test_inferred_fact_without_basis_summary_fails_contract() -> None:
    pack = load("dpia_evidence_ready.json")
    fact = pack["facts"][0]
    fact["epistemic_status"] = "inferred"
    fact["basis_summary"] = None
    with pytest.raises(Exception):
        validate_evidence_pack(pack)
