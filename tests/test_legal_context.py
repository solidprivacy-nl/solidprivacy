from __future__ import annotations

import copy
import json
from pathlib import Path

from solidprivacy.runtime.legal_context import load_rule_registry, load_source_registry, resolve_legal_context, validate_rule_registry_integrity

ROOT = Path(__file__).resolve().parents[1]

def load_request() -> dict:
    return json.loads((ROOT / "evals/legal_context/request_dpia.json").read_text(encoding="utf-8"))

def test_rule_registry_is_integrity_clean() -> None:
    assert validate_rule_registry_integrity() == []

def test_dpia_legal_context_is_ready_and_nonfinal_template_is_forward_only() -> None:
    bundle=resolve_legal_context(load_request()); assert bundle["status"]=="ready"; assert len(bundle["rules"])==6
    modes={item["source_id"]:item["use_mode"] for item in bundle["context_sources"]}
    assert modes["nl-government-par-dpia-model"]=="official_methodology"
    assert modes["edpb-dpia-template-2026"]=="forward_context_only"
    assert any("non_final_source_must_not_support_legal_claims" in item for item in bundle["warnings"])

def test_nonfinal_context_can_be_excluded() -> None:
    request=load_request(); request["include_nonfinal_context"]=False; bundle=resolve_legal_context(request)
    source=next(item for item in bundle["context_sources"] if item["source_id"]=="edpb-dpia-template-2026")
    assert source["use_mode"]=="excluded"

def test_stale_required_rules_block_bundle() -> None:
    request=load_request(); request["as_of"]="2027-01-15"; request["max_verification_age_days"]=30; bundle=resolve_legal_context(request)
    assert bundle["status"]=="blocked"; assert any("verification_stale" in item for item in bundle["blockers"])

def test_unknown_required_rule_blocks_bundle() -> None:
    request=load_request(); request["required_rule_ids"].append("unknown-rule"); bundle=resolve_legal_context(request)
    assert bundle["status"]=="blocked"; assert "required_rule_missing:unknown-rule" in bundle["blockers"]

def test_methodology_source_cannot_back_law_required_rule() -> None:
    source_registry=load_source_registry(); rule_registry=copy.deepcopy(load_rule_registry()); bad=copy.deepcopy(rule_registry["rules"][0]); bad["id"]="bad-methodology-law"; bad["source_id"]="nl-government-par-dpia-model"; rule_registry["rules"].append(bad)
    errors=validate_rule_registry_integrity(source_registry,rule_registry)
    assert "law_rule_not_backed_by_binding_or_decision_source:bad-methodology-law" in errors
