# Client Dossier Data Model V1

Status: candidate architecture contract for Mission `SOLID_PRIVACY_PLATFORM` / `SPP-GAP-20`.

## Purpose

Define the minimum governed domain model needed for client onboarding and dossier work without creating a second platform, a database-per-client design, or production infrastructure. The model is intentionally small and maps to `contracts/client_dossier.schema.json`.

## Core model

Use one shared multi-client application data model. `tenant_id` is the mandatory isolation boundary and must be carried by every persisted domain record in an implementation.

The minimum relationships are:

`Tenant -> Client -> Engagement -> Dossier`

A dossier references, rather than duplicates, governed evidence, controls and workflow records:

`Dossier -> EvidenceReference[]`

`Dossier -> ControlReference[]`

`Dossier -> WorkflowReference[]`

The repository already has a canonical evidence reference contract in `contracts/evidence.schema.json`; implementations should reuse that identity rather than inventing a second evidence store model.

## Entity responsibilities

| Entity | Minimum responsibility |
| --- | --- |
| Tenant | Isolation boundary for all client-domain records. |
| Client | Stable organization/customer identity and lifecycle status. |
| Engagement | Purpose-bounded piece of work for exactly one client. |
| Dossier | Onboarding, assessment, review or remediation container for exactly one engagement. |
| Evidence reference | Immutable/reference-style link to evidence identity and provenance. |
| Control reference | Link to the applicable control or obligation in the existing control model. |
| Workflow reference | Optional link to governed workflow state without copying workflow authority into the dossier. |

## Isolation and authorization

A shared database is the preferred default. Isolation is enforced by both data constraints and application authorization:

1. Every table/entity carries `tenant_id`.
2. Parent/child lookups include `tenant_id`; cross-tenant joins are invalid.
3. `engagement.client_id` must resolve to a client in the same tenant.
4. `dossier.engagement_id` must resolve to an engagement in the same tenant.
5. Evidence/control/workflow references are resolved only inside the current tenant or to explicitly global, immutable catalogue records.
6. JSON Schema validates shape; it is not itself an authorization boundary.

A practical relational implementation should use composite uniqueness/foreign-key constraints such as `(tenant_id, client_id)`, `(tenant_id, engagement_id)` and `(tenant_id, dossier_id)` and apply tenant-scoped authorization or row-level security at the persistence boundary. This avoids database-per-client operational complexity while keeping isolation explicit and testable.

## Auditability

Every mutable domain record requires creation/update timestamps and actor identity. Evidence itself is referenced by stable evidence IDs and existing provenance contracts; the dossier should not silently copy or rewrite evidence content. Material state transitions should remain reconstructable from application audit/event records in an eventual implementation.

## Retention

Retention is policy-driven, not hard-coded per client. Each dossier carries a `policy_ref`, a mandatory `review_at`, an optional `delete_after`, and a `legal_hold` flag. Deletion/retention execution is outside this schema contract and requires separate governed implementation. Evidence retention must additionally respect the evidence source and applicable legal/contractual policy.

## Backup assumption

The simplest safe baseline is a shared encrypted datastore with a standard encrypted off-site backup. `STANDARD_ENCRYPTED_OFFSITE` in the schema is only an architecture/planning classification; it does not provision backup infrastructure, define production recovery objectives, or authorize deployment. Detailed backup tooling is deferred until production infrastructure is explicitly authorized.

## Explicit non-authority

This contract does **not** authorize:

- processing or importing real client data;
- production database creation or deployment;
- per-client databases or custom key-management infrastructure;
- autonomous deletion or retention decisions;
- autonomous final legal, compliance or certification decisions.

Those remain separate governed work and authority boundaries.

## Review surface

Independent assurance for this candidate only needs to establish that the two-file contract is internally coherent, reuses the existing evidence-reference concept, explicitly models client/engagement/dossier/evidence/control/workflow relationships, provides a credible shared-database tenant-isolation boundary, addresses audit/retention/backup assumptions, and does not introduce production or real-client-data authority.
