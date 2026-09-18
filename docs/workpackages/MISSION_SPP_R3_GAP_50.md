# MISSION SPP R3 GAP-50 — evidence-based pilot readiness

## Mission binding

- Mission: `SOLID_PRIVACY_PLATFORM`
- Revision: `2026-09-02-r3`
- Gap: `SPP-GAP-50`
- Repository: `solidprivacy-nl/solidprivacy`
- Authoritative baseline: `main@9a5d66020a1cce373a04241a2b65f1e4bbf83341`

## Outcome

GAP-50 adds one small, explicit readiness contract on top of the already-integrated GAP-30 workflow model and GAP-40 evidence/review provenance controls. It does not create a new workflow engine, state plane, evidence store, scheduler, queue or professional-review framework.

The readiness rule is fail-closed: `READY` is valid only when every required pilot gate is `PASS`, every gate cites concrete repository evidence, no blocker remains, and every recorded decision is resolved.

## Canonical readiness gates

`contracts/pilot_readiness.schema.json` defines exactly five required gates:

1. `workflow_model` — recurring and standalone assignments use the governed workflow model;
2. `evidence_provenance` — evidence identity, binding and stale-review prevention are proven;
3. `human_professional_review` — material final conclusions remain attributable to a HUMAN reviewer;
4. `source_lineage` — current source provenance is explicit and machine-validatable;
5. `synthetic_pilot_validation` — synthetic cases prove the governed path without introducing real-client data.

Each gate must contain at least one `evidence_ref` and a non-empty rationale. An empty evidence list is invalid rather than an implicit pass.

## Fail-closed readiness

The contract has only two overall states: `NOT_READY` and `READY`.

For `READY`:

- all five required gates must be exactly `PASS`;
- `blockers` must be empty;
- every recorded decision must be `RESOLVED`.

Any missing/blocked/unknown gate, missing evidence, remaining blocker or open decision makes a claimed `READY` object invalid under the existing JSON-schema validation path.

`NOT_READY` remains a valid and explicit state. It may carry blocked/unknown gates, concrete blockers and open decisions so remaining work is visible rather than hidden or converted into narrative green status.

## Evidence and decisions

The readiness contract references existing repository evidence only. It does not copy or reinterpret that evidence into a second source of truth. A readiness assessment points to the current governed artifacts, tests, contracts and synthetic cases that prove each gate.

Remaining blockers are explicit objects with an id, description, owner and evidence references. Remaining decisions are explicit objects with an id, status, description and owner. This keeps unresolved governance visible without granting the readiness contract authority to resolve professional or principal decisions itself.

## Synthetic proof

`evals/synthetic_cases/pilot_readiness_ready.json` is a synthetic positive fixture bound only to repository evidence. `tests/test_pilot_readiness.py` proves that:

- the synthetic positive assessment validates;
- every required gate is mandatory for `READY`;
- every gate requires evidence;
- a remaining blocker invalidates `READY`;
- an open decision invalidates `READY`;
- `NOT_READY` can truthfully preserve blockers and open decisions.

The existing schema-validation and pytest path is reused; no second validator is introduced.

## Explicit non-authority

This candidate does not authorize:

- real-client data processing;
- production deployment or release;
- client delivery;
- autonomous final legal/privacy/compliance/risk decisions;
- bypass of the existing human professional-review gate;
- standing Control integration authority.

`READY` means only that the scoped synthetic pilot-readiness evidence satisfies this contract. Any real-client or production step remains separately governed.

## Acceptance mapping

- **Pilot readiness is evidence-based and fail-closed on missing gates:** the schema requires exact PASS status plus evidence on all five current gates and rejects blockers/open decisions for READY.
- **Remaining blockers and decisions are explicit:** NOT_READY preserves typed blocker and decision records rather than hiding them in prose.
