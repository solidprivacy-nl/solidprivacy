from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from solidprivacy.runtime.ai_boundary import evaluate_model_call_policy
from solidprivacy.runtime.dpia_analysis import FixtureDpiaAnalysisProvider, run_dpia_analysis
from solidprivacy.runtime.fact_extraction import FixtureFactExtractionProvider, run_fact_extraction
from solidprivacy.runtime.facts import derive_readiness, validate_evidence_pack_integrity
from solidprivacy.runtime.integrity import validate_dpia_integrity
from solidprivacy.runtime.legal_context import resolve_legal_context, validate_rule_registry_integrity
from solidprivacy.runtime.prescan import evaluate_prescan
from solidprivacy.runtime.schema_validation import (
    validate_dpia,
    validate_evidence_pack,
    validate_prescan_decision,
    validate_prescan_input,
)


def _load(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _dump(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def _validate_dpia(path: str) -> int:
    payload = _load(path)
    validate_dpia(payload)
    validate_dpia_integrity(payload)
    _dump({"status": "valid", "contract": "dpia_assessment", "path": path})
    return 0


def _prescan(path: str) -> int:
    payload = _load(path)
    validate_prescan_input(payload)
    decision = evaluate_prescan(payload)
    validate_prescan_decision(decision)
    _dump(decision)
    return 0


def _validate_evidence_pack(path: str) -> int:
    payload = _load(path)
    validate_evidence_pack(payload)
    validate_evidence_pack_integrity(payload)
    _dump({"status": "valid", "contract": "evidence_pack", "path": path})
    return 0


def _evidence_readiness(path: str, stage: str) -> int:
    payload = _load(path)
    validate_evidence_pack(payload)
    validate_evidence_pack_integrity(payload)
    _dump(derive_readiness(payload, stage))
    return 0


def _check_model_call(request_path: str, policy_path: str) -> int:
    decision = evaluate_model_call_policy(_load(request_path), _load(policy_path))
    _dump({
        "allowed": decision.allowed,
        "policy_id": decision.policy_id,
        "provider": decision.provider,
        "model": decision.model,
        "reasons": list(decision.reasons),
    })
    return 0 if decision.allowed else 2


def _fixture_extract(request_path: str, policy_path: str, result_path: str) -> int:
    request = _load(request_path)
    policy = _load(policy_path)
    result = _load(result_path)
    provider = FixtureFactExtractionProvider(
        provider_name=result["provider"],
        model_name=result["model"],
        results={request["id"]: result},
    )
    _dump(run_fact_extraction(request, policy, provider))
    return 0


def _resolve_legal_context(path: str) -> int:
    bundle = resolve_legal_context(_load(path))
    _dump(bundle)
    return 0 if bundle["status"] == "ready" else 2


def _validate_legal_rules() -> int:
    errors = validate_rule_registry_integrity()
    _dump({"status": "valid" if not errors else "invalid", "errors": errors})
    return 0 if not errors else 2


def _fixture_draft_dpia(request_path: str, policy_path: str, result_path: str) -> int:
    request = _load(request_path)
    policy = _load(policy_path)
    result = _load(result_path)
    provider = FixtureDpiaAnalysisProvider(
        provider_name=result["provider"],
        model_name=result["model"],
        results={request["id"]: result},
    )
    analysis, legal_context = run_dpia_analysis(request, policy, provider)
    _dump({"legal_context": legal_context, "analysis": analysis})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="solidprivacy")
    sub = parser.add_subparsers(dest="command", required=True)

    dpia = sub.add_parser("validate-dpia", help="Validate a canonical DPIA JSON file")
    dpia.add_argument("path")
    prescan = sub.add_parser("prescan", help="Evaluate a Dutch DPIA pre-scan input")
    prescan.add_argument("path")
    evidence = sub.add_parser("validate-evidence-pack", help="Validate an evidence/fact provenance pack")
    evidence.add_argument("path")
    readiness = sub.add_parser("evidence-readiness", help="Derive deterministic evidence-pack readiness")
    readiness.add_argument("path")
    readiness.add_argument("--stage", choices=["analysis", "finalisation"], default="analysis")
    model_call = sub.add_parser("check-model-call", help="Evaluate a model-call request against a privacy policy")
    model_call.add_argument("request")
    model_call.add_argument("policy")
    fixture = sub.add_parser("fixture-extract-facts", help="Run deterministic fixture-provider fact extraction")
    fixture.add_argument("request")
    fixture.add_argument("policy")
    fixture.add_argument("result")
    legal = sub.add_parser("resolve-legal-context", help="Resolve a governed legal context request")
    legal.add_argument("path")
    sub.add_parser("validate-legal-rules", help="Validate curated legal rules against the source registry")
    draft = sub.add_parser("fixture-draft-dpia", help="Run deterministic fixture-provider governed DPIA analysis")
    draft.add_argument("request")
    draft.add_argument("policy")
    draft.add_argument("result")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate-dpia":
        return _validate_dpia(args.path)
    if args.command == "prescan":
        return _prescan(args.path)
    if args.command == "validate-evidence-pack":
        return _validate_evidence_pack(args.path)
    if args.command == "evidence-readiness":
        return _evidence_readiness(args.path, args.stage)
    if args.command == "check-model-call":
        return _check_model_call(args.request, args.policy)
    if args.command == "fixture-extract-facts":
        return _fixture_extract(args.request, args.policy, args.result)
    if args.command == "resolve-legal-context":
        return _resolve_legal_context(args.path)
    if args.command == "validate-legal-rules":
        return _validate_legal_rules()
    if args.command == "fixture-draft-dpia":
        return _fixture_draft_dpia(args.request, args.policy, args.result)
    raise AssertionError(f"unknown command {args.command!r}")
