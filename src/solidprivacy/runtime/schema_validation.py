from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class ContractValidationError(ValueError):
    def __init__(self, schema_name: str, errors: list[str]):
        self.schema_name = schema_name
        self.errors = errors
        super().__init__(f"{schema_name} validation failed: " + "; ".join(errors))


def repository_root() -> Path: return Path(__file__).resolve().parents[3]
def contracts_dir() -> Path: return repository_root() / "contracts"
def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle: return json.load(handle)
def load_schema(schema_name: str) -> dict[str, Any]: return load_json(contracts_dir() / schema_name)
def build_registry() -> Registry:
    registry = Registry()
    for path in sorted(contracts_dir().glob("*.schema.json")):
        schema = load_json(path)
        if schema.get("$id"): registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry

def validation_errors(schema_name: str, instance: Any) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_name), registry=build_registry())
    errors=[]
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        path="$"
        if error.absolute_path: path += "".join(f"[{part}]" if isinstance(part,int) else f".{part}" for part in error.absolute_path)
        errors.append(f"{path}: {error.message}")
    return errors

def validate_contract(schema_name: str, instance: Any) -> None:
    errors=validation_errors(schema_name, instance)
    if errors: raise ContractValidationError(schema_name, errors)
def validate_dpia(instance: Any) -> None: validate_contract("dpia_assessment.schema.json", instance)
def validate_prescan_input(instance: Any) -> None: validate_contract("prescan_input.schema.json", instance)
def validate_prescan_decision(instance: Any) -> None: validate_contract("prescan_decision.schema.json", instance)
def validate_privacy_fact(instance: Any) -> None: validate_contract("privacy_fact.schema.json", instance)
def validate_evidence_pack(instance: Any) -> None: validate_contract("evidence_pack.schema.json", instance)
def validate_model_call_policy(instance: Any) -> None: validate_contract("model_call_policy.schema.json", instance)
def validate_fact_extraction_request(instance: Any) -> None: validate_contract("fact_extraction_request.schema.json", instance)
def validate_fact_extraction_result(instance: Any) -> None: validate_contract("fact_extraction_result.schema.json", instance)
def validate_model_call_request(instance: Any) -> None: validate_contract("model_call_request.schema.json", instance)
def validate_legal_rule(instance: Any) -> None: validate_contract("legal_rule.schema.json", instance)
def validate_legal_context_request(instance: Any) -> None: validate_contract("legal_context_request.schema.json", instance)
def validate_legal_context_bundle(instance: Any) -> None: validate_contract("legal_context_bundle.schema.json", instance)
def validate_dpia_analysis_request(instance: Any) -> None: validate_contract("dpia_analysis_request.schema.json", instance)
def validate_dpia_analysis_result(instance: Any) -> None: validate_contract("dpia_analysis_result.schema.json", instance)
