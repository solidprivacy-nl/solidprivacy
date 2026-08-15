from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from solidprivacy.runtime.integrity import validate_dpia_integrity
from solidprivacy.runtime.prescan import evaluate_prescan
from solidprivacy.runtime.schema_validation import (
    validate_dpia,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="solidprivacy")
    sub = parser.add_subparsers(dest="command", required=True)

    dpia = sub.add_parser("validate-dpia", help="Validate a canonical DPIA JSON file")
    dpia.add_argument("path")

    prescan = sub.add_parser("prescan", help="Evaluate a Dutch DPIA pre-scan input")
    prescan.add_argument("path")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate-dpia":
        return _validate_dpia(args.path)
    if args.command == "prescan":
        return _prescan(args.path)
    raise AssertionError(f"unknown command {args.command!r}")
