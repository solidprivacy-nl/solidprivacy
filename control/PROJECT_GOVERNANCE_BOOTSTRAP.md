# SolidPrivacy — Project Governance Bootstrap

```text
charter_id=CROSS_PROJECT_PRINCIPAL_AGENT_OPERATING_CHARTER_V1
canonical_charter_location=https://github.com/market-predictions/control-plane/blob/main/control/CROSS_PROJECT_PRINCIPAL_AGENT_OPERATING_CHARTER_V1.md
standard_id=CROSS_PROJECT_TWO_ROLE_GOVERNANCE_V1
canonical_standard_location=https://github.com/market-predictions/control-plane/blob/main/control/CROSS_PROJECT_TWO_ROLE_GOVERNANCE_STANDARD_V1.md
work_claim_standard=WORK_CLAIM_AND_BRANCH_LIFECYCLE_STANDARD_V1
work_claim_standard_location=https://github.com/market-predictions/control-plane/blob/main/control/WORK_CLAIM_AND_BRANCH_LIFECYCLE_STANDARD_V1.md
state_freshness_standard=CONTROL_STATE_FRESHNESS_STANDARD_V1
state_freshness_standard_location=https://github.com/market-predictions/control-plane/blob/main/control/CONTROL_STATE_FRESHNESS_STANDARD_V1.md
project_control_architecture=docs/PROJECT_CONTROL_ARCHITECTURE.md
project_machine_state=control/PROJECT_STATE.json
project_repository=solidprivacy-nl/solidprivacy
project_risk_class=privacy_sensitive_ai_processing_and_client_record_decision_support
adoption_status=enforced_for_consequential_work
enforcement_maturity=LEVEL_1_CHECKLIST_PLUS_MACHINE_GOVERNANCE_GATE
target_enforcement_maturity=LEVEL_2_MACHINE_EVIDENCE
implementation_role=implementation_operations
assurance_role=governance_release_assurance
project_specific_assurance_contract=control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md
project_specific_assurance_contract_status=ENFORCED
production_action=merge_to_authoritative_branch_and_enable_approved_runtime_capability
post_action_confirmation=exact_main_ci_plus_target_runtime_or_data_plane_verification_when_applicable
```

## Authority model

Three repositories/data domains have different authority and must not be conflated:

1. `market-predictions/control-plane` owns shared cross-project governance doctrine, freshness rules and work-claim lifecycle standards.
2. `solidprivacy-nl/solidprivacy` owns SolidPrivacy product decisions, roadmap, architecture, schemas, workflow logic, tests, work records, release state and assurance evidence.
3. The private Client Data Plane owns real client evidence and operational client privacy state. Client data never becomes project-governance material in this public/shared repository.

The project repository links to canonical control-plane standards; it does not fork/copy their doctrine beyond project-local adaptations.

For project-specific state the authority order is:

```text
project-local machine/durable authority
  > live GitHub evidence
  > reconciled human-readable project views
  > central Control cache when CURRENT
  > central narrative summaries
```

A lower-ranked stale narrative never wins a conflict with live/project-local evidence.

## Mandatory session start

For consequential planning, implementation, assurance, release or roadmap work:

1. Read and apply the canonical operating method beginning at `market-predictions/control-plane/control/SYSTEM_INDEX.md`, including the current freshness/lifecycle standards.
2. Read this bootstrap and `docs/PROJECT_CONTROL_ARCHITECTURE.md`.
3. Read `control/PROJECT_STATE.json` and determine whether its recorded coordination state is usable or requires live reconciliation.
4. Read `CURRENT_STATE.md` as the human-readable projection/context, never as independent authority over machine/live state.
5. Read `ROADMAP.md`.
6. Read `WORKPACKAGES.md` and the relevant detailed workpackage(s) in `docs/workpackages/`.
7. Read `CHANGELOG.md` and `DECISION_LOG.md` for durable changes affecting the assignment.
8. Read `control/WORK_CLAIMS.json` and live-reconcile relevant claims/branches/PRs under the canonical lifecycle standard.
9. Read relevant records under `handover/`.
10. Read `docs/architecture.md`, `docs/DATA_ARCHITECTURE.md` and other architecture contracts relevant to scope.
11. Inspect actual source, live GitHub branches/PRs/issues, tests, Actions and exact-head evidence; narrative completion claims are insufficient.

Do not ask the principal to restate information reconstructable from these sources.

## GitHub source-of-truth discipline

- `ROADMAP.md` is authoritative for product sequencing and milestone dependencies.
- `WORKPACKAGES.md` is the authoritative workpackage index; detailed workpackage specifications live in `docs/workpackages/`.
- `control/PROJECT_STATE.json` is the machine-readable project coordination state: current objective/scope, next gate/owner, active integration line and freshness metadata.
- `CURRENT_STATE.md` is the human-readable project-state projection/explanation. It must converge with machine/live state and may not become a competing state database.
- `control/WORK_CLAIMS.json` is the machine-readable claim/ownership register; live branch/PR state outranks stale recorded heads.
- `DECISION_LOG.md` records durable architecture/product/governance decisions and why they were made.
- `CHANGELOG.md` records material repository/product changes; it is not a substitute for the decision log.
- `handover/` records explicit CLOSE/TRANSFER/SUPERSEDE transitions and unresolved next actions.
- GitHub Actions/raw exact-head evidence outranks implementation handovers and work claims for verification status.
- No chat message, assistant memory, PR body or external planning document may silently override repository/live state.

## Freshness and reconciliation

Use the canonical freshness vocabulary:

```text
CURRENT
STALE
RECONCILIATION_REQUIRED
INDETERMINATE
```

Before consequential status reporting, routing, assurance, handover acceptance or merge/closeout, reconstruct affected live state when required. Changes in candidate/target heads, dependencies, PR/issue state, claim lifecycle, assurance, required CI gates or post-action evidence are reconciliation events.

`control/PROJECT_STATE.json` deliberately does not promise that a SHA embedded in a commit equals that commit's own SHA. Recorded SHAs are reconciliation observations; the live branch head must be retrieved from GitHub at mandatory gates.

Automation may detect or invalidate freshness. It may not infer `PASS`, `RELEASE_READY`, `DELIVERED` or comparable semantic outcomes from branch movement alone.

## Scope protection

Every active cycle has one primary objective and classifies discovered work as:

```text
CURRENT_RELEASE
NEXT_RELEASE
PARKING_LOT
```

New insight does not automatically become current implementation scope. Only safety/correctness requirements, explicit reprioritisation or work required for the stated outcome may interrupt the primary objective. Valid deferrable work is recorded rather than silently absorbed.

The current control-governance refinement belongs to PR #8 closeout. It must not expand the M1 privacy-engine implementation; M1 remains the next product gate after PR #8 assurance/closeout.

## Role and decision-plane boundary

`implementation_operations` may produce/revise candidates and report implementation state, but may not issue release assurance `PASS`.

`governance_release_assurance` independently reconstructs the candidate and may issue only:

```text
PASS
FAIL
INDETERMINATE
```

Assurance may not silently repair the candidate it is reviewing. Any semantic/product repair creates a new candidate requiring a fresh assurance cycle.

The Control D0–D3 decision classes govern **project/development operation only**. They do not replace SolidPrivacy runtime privacy/legal accountability. Residual DPIA risk, prior consultation, breach notification, DSAR exemptions, transfer conclusions and comparable rights-affecting decisions remain subject to the workflow's Privacy Officer/DPO/FG/legal review contracts even if the surrounding project-management choice would otherwise be D0/D1.

## Candidate identity

Do not conflate:

```text
implementation_candidate_sha
live_branch_head
administrative_descendant_sha
```

The implementation candidate is the exact semantic/product candidate produced by implementation and covered by its product evidence. The live branch head is reconstructed from GitHub. A later administrative descendant may record claim/state/handover metadata without retroactively changing which SHA earlier implementation evidence covered.

Independent assurance binds to an exact candidate. Any functional or semantic architecture change produces a new implementation candidate and requires fresh assurance. The project-specific assurance contract determines which structural checks are also required on any administrative descendant proposed for merge.

## Blind assurance

For material privacy/legal/data-plane/release work, the reviewer should reach its initial verdict from:

- user outcome/acceptance criteria;
- roadmap/workpackage/decision architecture;
- candidate source/diff;
- schemas/tests/workflow definitions;
- raw Actions/machine evidence;
- live target-state evidence where applicable.

Before its initial verdict it should not rely on implementation self-assessment, narrative handover conclusions or claims that tests 'should' pass.

After the initial verdict, implementation handover may be inspected for administrative completeness and undisclosed scope.

## Work-claim lifecycle

Every consequential active workpackage must have a repository-backed claim or equivalent machine-readable record meeting `WORK_CLAIM_AND_BRANCH_LIFECYCLE_STANDARD_V1`.

The coordinator must reconcile claims:

- at session start/resume;
- after dependency merges;
- before assurance;
- before merge/closeout;
- when branch/PR evidence shows drift/conflict/orphaned work.

A materially stale integration line stops accumulating functional work. Reconcile it when trivial; otherwise supersede it from the current target with explicit handover and rerun exact-head validation.

## Roadmap/workpackage discipline

Roadmap items are strategic sequencing units; workpackages are executable units.

A consequential workpackage must define at least:

- outcome;
- scope and explicit non-goals;
- dependencies;
- contracts/files likely affected;
- acceptance criteria;
- test/evidence requirements;
- security/privacy/legal constraints;
- required documentation updates;
- assurance route;
- definition of done.

`COMPLETE` in the roadmap means the applicable workpackage, exact-head evidence, claim lifecycle and handover/closeout are consistent. Implementation completion alone is insufficient.

## Data-handling governance

Project governance records must use synthetic/non-sensitive examples. Never place real client evidence, direct identifiers, passwords, secrets, model payloads containing customer data, Scrub Keys or replacement mappings in:

- issues;
- pull-request descriptions/comments;
- work claims;
- handovers;
- Actions logs/artifacts;
- eval fixtures;
- changelog/decision records.

Client-specific production evidence belongs only in the private Client Data Plane and may be referenced here only by non-sensitive opaque IDs/hashes where a release/incident genuinely requires that linkage.

## Required machine gate

`.github/workflows/project-governance-gate.yml` must validate the static project-governance manifest, `control/PROJECT_STATE.json`, mandatory source-of-truth files and the basic work-claim contract on consequential branches/PRs.

Machine governance does not replace live branch reconciliation, product/security tests or independent assurance; it prevents obvious structural drift.
