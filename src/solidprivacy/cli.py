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
from solidprivacy.runtime.schema_validation import validate_dpia, validate_evidence_pack, validate_prescan_decision, validate_prescan_input


def _load(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle: return json.load(handle)
def _dump(value: Any) -> None: print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
def _validate_dpia(path: str) -> int:
    payload=_load(path); validate_dpia(payload); validate_dpia_integrity(payload); _dump({"status":"valid","contract":"dpia_assessment","path":path}); return 0
def _prescan(path: str) -> int:
    payload=_load(path); validate_prescan_input(payload); decision=evaluate_prescan(payload); validate_prescan_decision(decision); _dump(decision); return 0
def _validate_evidence_pack(path: str) -> int:
    payload=_load(path); validate_evidence_pack(payload); validate_evidence_pack_integrity(payload); _dump({"status":"valid","contract":"evidence_pack","path":path}); return 0
def _evidence_readiness(path: str, stage: str) -> int:
    payload=_load(path); validate_evidence_pack(payload); validate_evidence_pack_integrity(payload); _dump(derive_readiness(payload,stage)); return 0
def _check_model_call(request_path: str, policy_path: str) -> int:
    d=evaluate_model_call_policy(_load(request_path),_load(policy_path)); _dump({"allowed":d.allowed,"policy_id":d.policy_id,"provider":d.provider,"model":d.model,"reasons":list(d.reasons)}); return 0 if d.allowed else 2
def _fixture_extract(request_path: str, policy_path: str, result_path: str) -> int:
    request=_load(request_path); policy=_load(policy_path); result=_load(result_path); provider=FixtureFactExtractionProvider(result["provider"],result["model"],{request["id"]:result}); _dump(run_fact_extraction(request,policy,provider)); return 0
def _resolve_legal_context(path: str) -> int:
    b=resolve_legal_context(_load(path)); _dump(b); return 0 if b["status"]=="ready" else 2
def _validate_legal_rules() -> int:
    errors=validate_rule_registry_integrity(); _dump({"status":"valid" if not errors else "invalid","errors":errors}); return 0 if not errors else 2
def _fixture_draft_dpia(request_path: str, policy_path: str, result_path: str) -> int:
    request=_load(request_path); policy=_load(policy_path); result=_load(result_path); provider=FixtureDpiaAnalysisProvider(result["provider"],result["model"],{request["id"]:result}); analysis,legal=run_dpia_analysis(request,policy,provider); _dump({"legal_context":legal,"analysis":analysis}); return 0

def build_parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(prog="solidprivacy"); sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("validate-dpia"); p.add_argument("path")
    p=sub.add_parser("prescan"); p.add_argument("path")
    p=sub.add_parser("validate-evidence-pack"); p.add_argument("path")
    p=sub.add_parser("evidence-readiness"); p.add_argument("path"); p.add_argument("--stage",choices=["analysis","finalisation"],default="analysis")
    p=sub.add_parser("check-model-call"); p.add_argument("request"); p.add_argument("policy")
    p=sub.add_parser("fixture-extract-facts"); p.add_argument("request"); p.add_argument("policy"); p.add_argument("result")
    p=sub.add_parser("resolve-legal-context"); p.add_argument("path")
    sub.add_parser("validate-legal-rules")
    p=sub.add_parser("fixture-draft-dpia"); p.add_argument("request"); p.add_argument("policy"); p.add_argument("result")
    return parser

def main() -> int:
    args=build_parser().parse_args()
    if args.command=="validate-dpia": return _validate_dpia(args.path)
    if args.command=="prescan": return _prescan(args.path)
    if args.command=="validate-evidence-pack": return _validate_evidence_pack(args.path)
    if args.command=="evidence-readiness": return _evidence_readiness(args.path,args.stage)
    if args.command=="check-model-call": return _check_model_call(args.request,args.policy)
    if args.command=="fixture-extract-facts": return _fixture_extract(args.request,args.policy,args.result)
    if args.command=="resolve-legal-context": return _resolve_legal_context(args.path)
    if args.command=="validate-legal-rules": return _validate_legal_rules()
    if args.command=="fixture-draft-dpia": return _fixture_draft_dpia(args.request,args.policy,args.result)
    raise AssertionError(f"unknown command {args.command!r}")
