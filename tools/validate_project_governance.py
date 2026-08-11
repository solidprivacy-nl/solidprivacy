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
PROJECT_STATE_PATH = ROOT / "control" / "PROJECT_STATE.json"

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

REQUIRED_PROJECT_STATE_FIELDS = {
    "schema_version",
    "project_id",
    "repository",
    "state_authority",
    "mode",
    "freshness",
    "current_objective",
    "active_claim",
    "integration_line",
    "candidate_identity",
    "scope",
    "next_gate",
    "decision_plane_boundary",
    "central_control",
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

    if not PROJECT_STATE_PATH.is_file():
        errors.append("missing control/PROJECT_STATE.json")
    else:
        project_state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
        missing = REQUIRED_PROJECT_STATE_FIELDS - set(project_state)
        if missing:
            errors.append(
                "control/PROJECT_STATE.json missing fields: "
                + ", ".join(sorted(missing))
            )

        if project_state.get("repository") != manifest.get("repository"):
            errors.append("PROJECT_STATE repository does not match governance manifest")

        freshness = project_state.get("freshness", {})
        freshness_status = freshness.get("status")
        allowed_freshness = set(manifest.get("allowed_freshness_statuses", []))
        if allowed_freshness and freshness_status not in allowed_freshness:
            errors.append(f"invalid project freshness status: {freshness_status}")
        for field in (
            "last_reconciled_at",
            "observed_target_sha",
            "observed_claim_head_sha",
            "live_head_policy",
        ):
            if field not in freshness:
                errors.append(f"PROJECT_STATE freshness missing field: {field}")

        scope = project_state.get("scope", {})
        for scope_class in manifest.get("required_scope_classes", []):
            if scope_class not in scope:
                errors.append(f"PROJECT_STATE scope missing class: {scope_class}")
            elif not isinstance(scope.get(scope_class), list):
                errors.append(f"PROJECT_STATE scope {scope_class} must be a list")

        next_gate = project_state.get("next_gate", {})
        for field in ("name", "owner_role", "principal_decision_required", "after_success"):
            if field not in next_gate:
                errors.append(f"PROJECT_STATE next_gate missing field: {field}")

        candidate = project_state.get("candidate_identity", {})
        for field in (
            "implementation_candidate_sha",
            "live_branch_head",
            "administrative_descendant_sha",
            "rule",
        ):
            if field not in candidate:
                errors.append(f"PROJECT_STATE candidate_identity missing field: {field}")

        boundary = project_state.get("decision_plane_boundary", {})
        if "project_control" not in boundary or "privacy_runtime" not in boundary:
            errors.append("PROJECT_STATE must separate project_control and privacy_runtime decisions")

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

        if PROJECT_STATE_PATH.is_file():
            project_state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
            active_claim = project_state.get("active_claim")
            if active_claim and active_claim not in seen_ids:
                errors.append(
                    f"PROJECT_STATE active_claim not found in WORK_CLAIMS: {active_claim}"
                )

    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8") if (ROOT / "ROADMAP.md").is_file() else ""
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8") if (ROOT / "docs" / "architecture.md").is_file() else ""
    control_architecture = (ROOT / "docs" / "PROJECT_CONTROL_ARCHITECTURE.md").read_text(encoding="utf-8") if (ROOT / "docs" / "PROJECT_CONTROL_ARCHITECTURE.md").is_file() else ""
    workpackages = (ROOT / "WORKPACKAGES.md").read_text(encoding="utf-8") if (ROOT / "WORKPACKAGES.md").is_file() else ""

    for marker in ("Client Data Plane", "M1", "M2", "HMPO"):
        if marker not in roadmap:
            errors.append(f"ROADMAP.md missing governance-critical marker: {marker}")

    for marker in ("Client Data Plane", "GitHub", "governance"):
        if marker not in architecture:
            errors.append(f"docs/architecture.md missing governance-critical marker: {marker}")

    for marker in (
        "freshness",
        "CURRENT_RELEASE",
        "NEXT_RELEASE",
        "PARKING_LOT",
        "implementation_candidate_sha",
        "privacy/legal",
    ):
        if marker not in control_architecture:
            errors.append(
                "docs/PROJECT_CONTROL_ARCHITECTURE.md missing governance-critical marker: "
                + marker
            )

    for marker in ("WP8", "SP-WC-0008"):
        if marker not in workpackages:
            errors.append(f"WORKPACKAGES.md missing current index marker: {marker}")

    if errors:
        return fail(errors)

    print("SolidPrivacy project-governance structure: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
