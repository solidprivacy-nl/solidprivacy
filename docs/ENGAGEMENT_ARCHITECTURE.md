# SolidPrivacy Engagement Architecture

## Purpose

SolidPrivacy must support both **bounded professional-service assignments** and **continuous managed privacy services** without creating separate legal logic, separate workflow engines or separate customer truth models.

The engagement layer answers four questions before a governed privacy workflow runs:

1. **What has the client contracted SolidPrivacy to do?**
2. **What organisation/process/data scope may the workflow use?**
3. **How long may evidence and resulting state persist?**
4. **Does completion end the service, or must later changes trigger ongoing reassessment/work?**

The engagement mode changes orchestration and state lifecycle. It does **not** change the governed legal sources, methodologies, evidence/provenance rules, validators or human-accountability gates used by the underlying privacy workflow.

## Core rule — one governed engine, multiple engagement modes

```text
                         SOLIDPRIVACY GOVERNED ENGINE
                sources / methods / skills / workflows / evals
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
              PROJECT                       MANAGED_SERVICE
        bounded assignment                continuous service
                    |                           |
          DPIA / vendor / DSAR          POaaS / recurring privacy
          breach / transfer / etc.      operating responsibility
                    |                           |
                    +-------------+-------------+
                                  |
                           SAME PRIVACY CORE
```

A standalone DPIA and a DPIA performed within POaaS must execute the **same DPIA workflow contracts and legal/evidence controls** for equivalent facts. Engagement mode may determine input scope, persistence, delivery and follow-up behavior; it may never fork legal truth.

## Engagement modes

### `PROJECT`

Use for a bounded professional-service assignment with an agreed deliverable or outcome.

Typical examples:

- standalone DPIA;
- processor / Article 28 review;
- personal-data-breach assessment;
- DSAR support;
- international-transfer assessment;
- AI/privacy assessment;
- targeted privacy baseline or remediation review.

Default characteristics:

```text
scope                  bounded to contracted assignment
continuous_monitoring  false
state_scope             ENGAGEMENT_SCOPED unless explicitly promoted
change_propagation      only while engagement is active, unless separately contracted
completion              deliverable acceptance + deterministic closeout
retention               explicit per evidence/state/artifact/audit class
```

A project engagement must not silently become an organisation-wide managed privacy dossier merely because SolidPrivacy learned useful facts while executing the assignment.

### `MANAGED_SERVICE`

Use when SolidPrivacy has an ongoing service obligation over an organisation or defined portfolio of privacy responsibilities.

Typical example:

- Privacy Officer as a Service (POaaS).

Default characteristics:

```text
scope                  organisation/service-package defined
continuous_monitoring  true for contracted domains
state_scope             ORGANISATION_SCOPED for accepted reusable facts
change_propagation      active according to service commitments/dependencies
completion              service-period/offboarding event, not one deliverable
retention               service + legal/audit policy with explicit offboarding
```

Managed service does not remove workflow-specific scope controls. A DPIA inside POaaS still receives only the evidence/state required for that DPIA task.

## Engagement mode is separate from service/workflow type

Do not encode service semantics into engagement persistence.

Conceptually:

```text
engagement_mode:
  PROJECT | MANAGED_SERVICE

service_type:
  DPIA
  VENDOR_ASSESSMENT
  BREACH_ASSESSMENT
  DSAR
  TRANSFER_ASSESSMENT
  PRIVACY_BASELINE
  POAAS
  ...
```

For example, `DPIA` can occur under either `PROJECT` or `MANAGED_SERVICE`. This avoids a second "POaaS DPIA" implementation diverging from a "standalone DPIA" implementation.

## Canonical engagement envelope

The eventual production contract should make at least the following semantics explicit:

```text
engagement_id
organisation_id
engagement_mode
service_type / service_package
jurisdiction
start / end or service period
scope / exclusions
designated client contacts / reviewers
promised deliverables
persistence_policy
retention_policy
continuous_monitoring_policy
state_promotion_policy
```

This is an architectural contract now. The generalized production schema belongs to WP9, after the Client Data Plane is implemented and independently assured.

M1 may use a **minimal synthetic engagement envelope** sufficient to prove standalone execution; M1 must not pull the full WP9 production engagement platform forward.

## State scopes

SolidPrivacy must distinguish at least three logical state scopes:

### `RUN_SCOPED`

Temporary execution material for one workflow/run.

Examples:

- intermediate candidate facts;
- model context;
- validator scratch state;
- stage-local generated content.

This state is not durable customer truth merely because a workflow completed.

### `ENGAGEMENT_SCOPED`

Reviewed evidence/facts/assessments/deliverables that belong to a bounded assignment and may need to persist through delivery, warranty/review or agreed retention.

Examples for a standalone DPIA:

- processing scope used for the DPIA;
- evidence and support references;
- accepted DPIA facts;
- risk/measure assessment;
- review decisions;
- final deliverable and audit lineage.

Engagement-scoped state does not imply continuous organisation-wide maintenance.

### `ORGANISATION_SCOPED`

Durable reusable state that SolidPrivacy is authorised/contracted to maintain across workflows and service periods.

Examples:

- accepted processing activities;
- systems;
- processors/recipients;
- retention rules;
- accepted organisation facts;
- controls/findings/actions;
- dependency relationships used for reassessment.

This is the normal reusable state domain for a managed service such as POaaS.

## Promotion is explicit

Useful facts learned during a standalone assignment may later be reused, but they do not automatically become organisation-scoped managed state.

Conceptually:

```text
ENGAGEMENT_SCOPED accepted state
            |
            | explicit contractual/client/PO-authorised promotion
            v
ORGANISATION_SCOPED accepted state
```

Promotion must preserve:

- original evidence/provenance;
- review/approval lineage;
- effective dates;
- scope limitations;
- contradiction status;
- retention/legal basis for continued storage;
- dependency links created by the promotion.

Promotion is a governed state transition, not a database copy convenience.

## Workflow execution context

Every generalized production workflow should be able to recover an execution context equivalent to:

```yaml
engagement_mode: PROJECT | MANAGED_SERVICE
service_type: DPIA | ...
scope_reference: ...
state_read_scope: ...
state_write_scope: RUN_SCOPED | ENGAGEMENT_SCOPED | ORGANISATION_SCOPED
continuous_monitoring: true | false
retention_policy_reference: ...
promotion_policy_reference: ...
```

The workflow's legal/evidence pipeline remains the same:

```text
authorised scoped input
 -> evidence/provenance
 -> governed legal/methodology context
 -> deterministic + AI-assisted analysis
 -> validators
 -> accountable human review
 -> accepted result
```

Only the pre/post orchestration differs:

```text
PROJECT
  -> accepted engagement result
  -> deliver
  -> closeout / retain / archive / delete according to policy

MANAGED_SERVICE
  -> accepted result
  -> update authorised organisation state
  -> dependency impact propagation
  -> continuing work/monitoring according to service scope
```

## Change propagation is engagement-aware

Continuous change propagation is not a property of the DPIA algorithm itself. It is a property of the service obligation and persisted state.

### Active managed service

```text
processor changed
  -> affected processing state
  -> RoPA projection stale
  -> vendor/transfer assessment impact
  -> DPIA facts/review potentially stale
  -> work items created
```

### Closed standalone project

```text
PROJECT engagement closed
  -> no implicit monitoring obligation
  -> retained records follow retention policy
  -> no new work item merely because the world changed
```

A separately contracted watch/review service may create new monitoring obligations, but must be represented explicitly rather than inferred from historic data possession.

## Retention and offboarding

Every engagement requires deterministic closeout semantics for each major data class:

```text
original evidence
structured engagement state
derived chunks/embeddings
model-call records where retained
workflow/audit evidence
delivery artifacts
backups
```

Permitted post-completion outcomes include, subject to contract/legal policy:

```text
DELETE
RETAIN_UNTIL
ARCHIVE_RESTRICTED
LEGAL_HOLD
PROMOTE_TO_ORGANISATION_STATE
RETURN_OR_EXPORT_THEN_DELETE
```

Different data classes may have different outcomes. "Keep the customer dossier" is not an acceptable implicit default.

## Client Data Plane relationship

Both engagement modes use the same private Client Data Plane security boundary when real client data is processed.

The data plane must therefore support:

```text
client/tenant boundary
   |
   +-- engagement-scoped evidence/state/artifacts
   |
   +-- organisation-scoped managed state (only where authorised)
   |
   +-- workflow/audit lineage linking both scopes
```

A customer may have multiple project engagements without SolidPrivacy maintaining a complete organisation privacy state. Conversely, a managed-service engagement may reuse explicitly accepted organisation-scoped state across many workflows.

Dedicated-per-client versus pooled infrastructure is an independent physical-isolation decision; it does not determine whether logical state is engagement-scoped or organisation-scoped.

## Standalone DPIA reference path

A `PROJECT + DPIA` engagement should be executable as:

```text
agreed DPIA assignment/scope
  -> minimal engagement envelope
  -> evidence request/intake
  -> Scrub/minimisation/egress policy
  -> facts + provenance + contradictions/gaps
  -> targeted questions
  -> DPIA pre-scan / governed methodology
  -> governed legal context
  -> DPIA analysis / risk / measures
  -> Privacy Officer review
  -> final reviewed DPIA + appendices
  -> delivery acceptance
  -> engagement audit package
  -> retention/offboarding
```

No full RoPA, organisation-wide processing inventory or continuous-monitoring layer is required unless it is part of the contracted scope.

## M1 architectural interpretation

M1 remains the next product milestone and should prove the first **standalone professional-service execution** over the governed engine.

M1 uses synthetic/non-personal evidence and a minimal synthetic envelope similar to:

```yaml
engagement_mode: PROJECT
service_type: DPIA
continuous_monitoring: false
state_scope: ENGAGEMENT_SCOPED
```

M1 acceptance should demonstrate:

- one positive standalone DPIA assignment from bounded scope/evidence through reviewed deliverable/audit;
- one blocked/adversarial path;
- no hidden manual handoff between technical stages;
- no accidental promotion into organisation-wide managed state;
- an explicit synthetic closeout/retention disposition;
- the existing HMPO/cycle-time/compute measurement primitives.

M1 does **not** production-enable real client persistence and does not require the generalized WP9 engagement schema. Production real-client storage remains gated by WP8 Client Data Plane assurance.

## Managed-service interpretation

The existing POaaS reference flow is the managed-service specialization of this architecture:

```text
MANAGED_SERVICE + POAAS
  -> persistent organisation state
  -> reusable evidence/facts
  -> multiple governed workflows
  -> dependency propagation
  -> continuing PO work queue
  -> recurring deliverables/reporting
```

M2 remains the first broad synthetic managed-service acceptance milestone after the shared execution, data and client-state substrate has been implemented.

## Non-goals

This architecture does not:

- create separate standalone and POaaS versions of legal workflows;
- permit a project engagement to retain data indefinitely by default;
- make every fact discovered during a project organisation-wide truth;
- introduce continuous monitoring when it was not contracted;
- pull the generalized production client/engagement platform before WP8/WP9;
- change the requirement for accountable human review of material privacy/legal conclusions.

## Governing rule

> Engagement mode governs scope, persistence, retention and continuation. The governed privacy workflow governs evidence, legal/methodological reasoning, validation and human accountability. A standalone assignment and a managed service share one engine and diverge only where the service contract requires them to.
