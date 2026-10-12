from __future__ import annotations

from copy import deepcopy

import pytest

from solidprivacy.runtime.schema_validation import ContractValidationError, load_json, repository_root, validate_contract


FIXTURE = repository_root() / "evals" / "synthetic_cases" / "pilot_readiness_ready.json"
SCHEMA = "pilot_readiness.schema.json"


def _ready() -> dict:
    return load_json(FIXTURE)


def test_synthetic_pilot_readiness_is_valid() -> None:
    validate_contract(SCHEMA, _ready())


@pytest.mark.parametrize(
    "gate_id",
    [
        "workflow_model",
        "evidence_provenance",
        "human_professional_review",
        "source_lineage",
        "synthetic_pilot_validation",
    ],
)
def test_ready_fails_closed_when_any_required_gate_is_not_pass(gate_id: str) -> None:
    assessment = _ready()
    assessment["gates"][gate_id]["status"] = "BLOCKED"
    with pytest.raises(ContractValidationError):
        validate_contract(SCHEMA, assessment)


def test_every_gate_requires_evidence() -> None:
    assessment = _ready()
    assessment["gates"]["evidence_provenance"]["evidence_refs"] = []
    with pytest.raises(ContractValidationError):
        validate_contract(SCHEMA, assessment)


def test_ready_fails_closed_with_remaining_blocker() -> None:
    assessment = _ready()
    assessment["blockers"] = [
        {
            "id": "missing-proof",
            "description": "Required pilot evidence is absent.",
            "owner": "SolidPrivacy governance",
            "evidence_refs": ["tests/test_pilot_readiness.py"],
        }
    ]
    with pytest.raises(ContractValidationError):
        validate_contract(SCHEMA, assessment)


def test_ready_fails_closed_with_open_decision() -> None:
    assessment = _ready()
    assessment["decisions"][0]["status"] = "OPEN"
    with pytest.raises(ContractValidationError):
        validate_contract(SCHEMA, assessment)


def test_not_ready_keeps_blockers_and_open_decisions_explicit() -> None:
    assessment = deepcopy(_ready())
    assessment["status"] = "NOT_READY"
    assessment["gates"]["synthetic_pilot_validation"]["status"] = "UNKNOWN"
    assessment["blockers"] = [
        {
            "id": "pilot-proof-pending",
            "description": "Synthetic pilot validation has not completed.",
            "owner": "SolidPrivacy governance",
            "evidence_refs": ["evals/synthetic_cases/dpia_nl_basic.json"],
        }
    ]
    assessment["decisions"][0]["status"] = "OPEN"
    validate_contract(SCHEMA, assessment)
