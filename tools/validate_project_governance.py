#!/usr/bin/env python3
"""Static project-governance structure gate for SolidPrivacy.

This gate prevents obvious source-of-truth drift. It deliberately does not replace
live GitHub reconciliation, exact-head product tests, security testing or
independent governance_release_assurance.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "control" / "GOVERNANCE_MANIFEST.json"
CLAIMS_PATH = ROOT / "control" / "WORK_CLAIMS.json"

REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "workpackage_id",
    "repository",
    "owner_role",
    "scope",
    "branch",
    "base_or_target_branch",
    "last_reconciled_target_sha",
    "current_claim_head_sha",
    "status",
    "opened_at",
    "last_reconciled_at",
    "pull_request_or_issue_reference",
    "dependencies",
}


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"GOVERNANCE_ERROR: {error}")
    return 1


def main() -> int:
    errors: list[str] = []

    if not MANIFEST_PATH.is_file():
        return fail(["missing control/GOVERNANCE_MANIFEST.json"])

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for raw_path in manifest.get("required_paths", []):
        if not (ROOT / raw_path).exists():
            errors.append(f"required path missing: {raw_path}")

    for raw_path in manifest.get("required_workpackage_specs", []):
        if not (ROOT / raw_path).is_file():
            errors.append(f"required workpackage spec missing: {raw_path}")

    for raw_path in manifest.get("forbidden_repository_paths", []):
        if (ROOT / raw_path).exists():
            errors.append(
                f"forbidden client-data/secrets repository path exists: {raw_path}"
            )

    if not CLAIMS_PATH.is_file():
        errors.append("missing control/WORK_CLAIMS.json")
    else:
        claims_document = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
        claims = claims_document.get("claims", [])
        allowed_statuses = set(manifest.get("allowed_claim_statuses", []))
        seen_ids: set[str] = set()
        active_release_integration = 0

        for idx, claim in enumerate(claims):
            missing = REQUIRED_CLAIM_FIELDS - set(claim)
            if missing:
                errors.append(
                    f"claim[{idx}] missing fields: {', '.join(sorted(missing))}"
                )

            claim_id = claim.get("claim_id")
            if claim_id in seen_ids:
                errors.append(f"duplicate claim_id: {claim_id}")
            if claim_id:
                seen_ids.add(claim_id)

            status = claim.get("status")
            if allowed_statuses and status not in allowed_statuses:
                errors.append(f"claim {claim_id} has invalid status: {status}")

            if (
                claim.get("claim_type") == "release_integration"
                and status in {"ACTIVE", "BLOCKED", "HANDOVER_READY"}
            ):
                active_release_integration += 1

            if claim.get("repository") != manifest.get("repository"):
                errors.append(
                    f"claim {claim_id} repository mismatch: {claim.get('repository')}"
                )

        if active_release_integration > 1:
            errors.append(
                "more than one open release_integration claim exists for this repository"
            )

    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8") if (ROOT / "ROADMAP.md").is_file() else ""
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8") if (ROOT / "docs" / "architecture.md").is_file() else ""
    workpackages = (ROOT / "WORKPACKAGES.md").read_text(encoding="utf-8") if (ROOT / "WORKPACKAGES.md").is_file() else ""

    for marker in ("Client Data Plane", "M1", "M2", "HMPO"):
        if marker not in roadmap:
            errors.append(f"ROADMAP.md missing governance-critical marker: {marker}")

    for marker in ("Client Data Plane", "GitHub", "governance"):
        if marker not in architecture:
            errors.append(f"docs/architecture.md missing governance-critical marker: {marker}")

    for marker in ("WP8", "SP-WC-0008"):
        if marker not in workpackages:
            errors.append(f"WORKPACKAGES.md missing current index marker: {marker}")

    if errors:
        return fail(errors)

    print("SolidPrivacy project-governance structure: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
