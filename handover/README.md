# SolidPrivacy Handovers

This directory contains explicit ownership/lineage transitions for consequential work under `WORK_CLAIM_AND_BRANCH_LIFECYCLE_STANDARD_V1`.

A handover is a state transition, not a narrative convenience.

## Required fields

Every handover record must identify:

```text
handover_id
claim_id
from_owner_or_role
to_owner_or_role
repository
source_branch
exact_source_head_sha
exact_target_or_main_sha
scope_completed
artifacts_and_evidence
unresolved_items
next_action
disposition
created_at
```

Allowed dispositions:

```text
CLOSE
TRANSFER
SUPERSEDE
```

## Rules

- `CLOSE` makes the originating claim terminal `CLOSED`.
- `TRANSFER` continues the same claim under explicitly updated ownership/reconciliation state.
- `SUPERSEDE` makes the old claim terminal `SUPERSEDED` and names the successor claim/branch.
- An accepted handover may not leave an originating claim silently `ACTIVE`.
- A superseded branch is historical/donor evidence only; it may not continue receiving implementation work.
- Handover narrative cannot establish `PASS`; assurance reconstructs raw evidence independently.
- Real client data, direct identifiers, credentials, Scrub Keys or sensitive production payloads must not appear in handover records. Use opaque evidence IDs/hashes and private assurance references where needed.

## Naming

Preferred pattern:

```text
handover/<handover_id>.md
```

Example:

```text
handover/SP-HO-0008.md
```

## Minimum template

```markdown
# <handover_id>

claim_id: <claim>
disposition: CLOSE | TRANSFER | SUPERSEDE
from: <owner/role>
to: <owner/role>
source_branch: <branch>
exact_source_head_sha: <sha>
exact_target_or_main_sha: <sha>
created_at: <timestamp>

## Scope completed

...

## Artifacts and evidence

...

## Unresolved items

...

## Next action

...
```

No handover is required merely because a chat/session ends. It is required when consequential ownership or branch lineage closes, transfers or is superseded.
