# SolidPrivacy Project Control Architecture

## Purpose

This document defines how SolidPrivacy development, roadmap execution, release state and agent coordination are controlled. It applies the canonical doctrine in `market-predictions/control-plane` to this project without copying or forking that doctrine.

It is deliberately separate from privacy/legal runtime decision-making. Project governance decides how SolidPrivacy is built and released; it does **not** replace the Privacy Officer / DPO/FG / legal accountability gates inside SolidPrivacy workflows.

## Governing architecture

```text
PRINCIPAL
   |
   v
portfolio_control / project coordinator
   |-- implementation_operations
   `-- governance_release_assurance

          reads / reconciles
                 |
                 v
SOLIDPRIVACY PROJECT AUTHORITY
  control/PROJECT_STATE.json
  ROADMAP.md
  WORKPACKAGES.md + docs/workpackages/
  control/WORK_CLAIMS.json
  DECISION_LOG.md / CHANGELOG.md
  handover/
  live GitHub branches / PRs / issues / Actions / assurance
```

`market-predictions/control-plane` owns shared operating doctrine, lifecycle/freshness semantics and cross-project coordination. `solidprivacy-nl/solidprivacy` owns project-specific truth. Central Control summaries are freshness-bound cache views and never outrank project-local authority or live GitHub evidence.

## Authority hierarchy

For SolidPrivacy project/release state, use this order:

1. project-local machine-readable control contracts and durable project decisions;
2. live GitHub repository evidence: branches, PRs, issues, Actions, exact candidate heads, assurance and receipts;
3. project-local human-readable views such as `CURRENT_STATE.md`, when reconciled;
4. central Control cache when its freshness contract is `CURRENT`;
5. central narrative summaries as convenience projections only.

When sources conflict, lower-ranked narrative/cache material is stale. Do not silently select the convenient version.

## Machine-first project state

`control/PROJECT_STATE.json` is the project-local machine-readable coordination state. It records the last semantic reconciliation, active objective, scope class, active claim/integration line, next gate, owner and principal-decision requirement.

It is **not self-referential**. A Git commit cannot truthfully contain its own SHA before it exists. Therefore recorded SHAs are observations made at reconciliation; the live branch/PR head is always reconstructed from GitHub at mandatory reconciliation gates.

`CURRENT_STATE.md` is the human-readable projection/explanation of this state. It must not evolve into an independently maintained competing state database.

## Freshness semantics

Project coordination uses the canonical Control freshness vocabulary:

```text
CURRENT
STALE
RECONCILIATION_REQUIRED
INDETERMINATE
```

A material status statement may be reused only when it is still `CURRENT` or has been freshly reconstructed. Immediate reconciliation events include at least:

- target/default branch movement that affects the active line;
- active PR state/head changes at a mandatory gate;
- dependency merge;
- work-claim open/transfer/supersede/close;
- assurance verdict;
- required Actions/gate result that changes the next action;
- handover acceptance;
- deployment/data-plane/post-action evidence;
- contradiction between project-local state and live GitHub.

Automation may detect/invalidate freshness. It may not infer semantic outcomes such as `PASS`, `RELEASE_READY`, `DELIVERED` or `OUTCOME_CONFIRMED` from branch movement alone.

## One objective and scope protection

Each execution cycle has one primary objective. New findings are classified into:

```text
CURRENT_RELEASE
NEXT_RELEASE
PARKING_LOT
```

- `CURRENT_RELEASE`: required for the currently agreed outcome, safety or correctness.
- `NEXT_RELEASE`: valid improvement with a defined future dependency/value, but not required to close the current objective.
- `PARKING_LOT`: useful idea without current sequencing authority.

Discovery does not equal activation. A new architecture insight may update durable architecture/roadmap records when needed, but implementation is not silently added to the current release unless it is required for the stated outcome or safety/correctness.

For the current program, the control-governance refinement closes within PR #8; it does not expand M1. After PR #8 assurance/closeout, M1 remains the next product execution gate.

## Decision planes must remain separate

### Project/control decisions

The canonical Control D0–D3 classes apply to development and project operation:

- `D0`: routine reversible work, tests, documentation and diagnostics;
- `D1`: delegated recorded implementation/scope decisions;
- `D2`: material product/business direction requiring a principal decision after controller recommendation;
- `D3`: principal-only expenditure, irreversible action, material risk acceptance or authority explicitly reserved by project contract.

### Privacy/legal workflow decisions

These are **not** D0–D3 shortcuts. Runtime conclusions remain governed by SolidPrivacy's privacy decision architecture, for example:

```text
AI/deterministic candidate
 -> evidence/provenance validation
 -> governed legal context
 -> Privacy Officer review
 -> DPO/FG/legal escalation where required
 -> accountable decision
```

A project controller cannot classify residual DPIA risk, breach notification, DSAR exemption, transfer conclusion or comparable rights-affecting judgement as D0/D1 merely because the project-control decision is operationally routine.

## Candidate identity and exact-head assurance

SolidPrivacy distinguishes three identities that must not be conflated:

```text
implementation_candidate_sha
  exact product/architecture candidate prepared by implementation

live_branch_head
  current GitHub branch head reconstructed live

administrative_descendant
  later commit that may only record handover/state/claim metadata
```

Independent assurance binds to an **exact candidate**. A functional repair or semantic architecture change creates a new implementation candidate and requires fresh assurance.

An administrative descendant may record the handover of a previously tested implementation candidate, but it does not retroactively change which SHA the implementation evidence covered. If the administrative descendant itself is proposed for merge, the project-specific assurance contract decides which structural/exact-head checks must also run on that descendant.

No PR description, handover narrative or recorded claim head substitutes for live reconstruction.

## Work-claim and handover lifecycle

Consequential work has one repository-backed claim lineage. At mandatory gates the coordinator reconstructs:

- claim owner and state;
- source branch and live head;
- target branch and last reconciled target SHA;
- dependencies and dependency changes;
- PR state and mergeability/drift;
- candidate identity;
- handover disposition;
- one surviving release-integration line.

Materially stale integration lines stop accumulating. Reconcile them when trivial; otherwise supersede with a clean successor and explicit handover, then rerun exact-head validation/assurance.

A handover is a state transition, not an essay. `CLOSE`, `TRANSFER` and `SUPERSEDE` must leave claim ownership and lineage unambiguous.

## Next-gate routing contract

At any material point, project state should make these fields recoverable without chat memory:

```text
current_objective
active_claim
current_release_scope
next_gate
next_gate_owner
principal_decision_required
after_success
freshness_status
```

`portfolio_control` may route work from this state only after freshness reconciliation. It coordinates implementation and assurance but may not certify work it directed.

## Relationship to central Control

After the project bootstrap exists on the authoritative/default branch, SolidPrivacy should be enrolled in the canonical control-plane governance/freshness audit (tracked by issue #9).

The central layer may cache:

- mode and priority;
- current objective;
- next gate;
- tracked PR/issues;
- principal-attention requirement;
- last reconciliation evidence.

It may not silently override SolidPrivacy's project-local roadmap, claims, candidate identity, assurance result, data-plane state or production authority.

## Machine enforcement

`.github/workflows/project-governance-gate.yml` and `tools/validate_project_governance.py` provide a structural gate. They should verify at minimum:

- required authority files exist;
- `control/PROJECT_STATE.json` contains the required machine state fields and valid freshness/scope values;
- work-claim contracts remain valid and one integration line survives;
- control architecture/freshness/candidate semantics remain anchored;
- forbidden customer-data/secrets paths remain absent.

This gate detects structural drift only. Live reconciliation, security testing, product/eval gates and independent assurance remain separate obligations.

## Anti-patterns

Do not:

- treat central Control Markdown as fresher than live project evidence;
- maintain `CURRENT_STATE.md` and `PROJECT_STATE.json` as independent truths;
- use chat memory as authority;
- allow multiple active release-integration claims for one line;
- let a stale branch keep accumulating after dependency drift;
- treat an administrative descendant as proof that product tests covered it;
- turn every new insight into current-release scope;
- let portfolio/project governance make privacy/legal decisions reserved for accountable professionals;
- let implementation certify its own candidate.

## Compact governing rule

> Reconstruct live state before acting. Keep project truth local, Control freshness-bound, scope explicitly classified, candidate identity exact, implementation separate from assurance, and project-governance decisions separate from privacy/legal accountability.
