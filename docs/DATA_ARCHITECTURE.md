# SolidPrivacy Client Data Architecture

Status: architecture decision — implementation scheduled by `ROADMAP.md`

## Purpose

SolidPrivacy's shared repository is the governed capability/source-of-truth layer. It is not a customer dossier store. Real client evidence, direct identifiers, credentials, Scrub Keys, model-call content and durable client state require a separate private data plane with explicit tenant, residency, access, retention and AI-egress controls.

This document defines the target data boundary for Privacy Officer as a Service (POaaS).

## Core rule

> GitHub stores product logic, schemas, legal-source governance, synthetic fixtures, work records and assurance evidence. The Client Data Plane stores real customer dossiers and operational privacy state. The AI runtime receives only the minimum tenant-scoped context required for one governed task.

No real client dossier may be committed to this repository, GitHub Issues, pull-request comments, Actions artifacts, regression fixtures or implementation handovers.

## Five-plane runtime model

```text
GLOBAL GOVERNED CAPABILITY PLANE
  source registry / law / methodologies / schemas / workflows / evals
                    |
                    v
EXECUTION + ASSURANCE PLANE
  run orchestration / policy gates / validators / human review / audit
                    |
                    v
PRIVATE CLIENT DATA PLANE
  evidence vault / structured state DB / retrieval index / artifact vault / keys
                    |
                    v
CLIENT OPERATING STATE
  organisation / engagement / processing / processors / assessments / actions
                    |
                    v
DELIVERY + CONTINUOUS SERVICE
  questions / work queues / reports / reassessment / management delivery
```

The physical Client Data Plane and the logical Client Operating State are deliberately separate concepts. A database implementation may change without changing the canonical privacy model.

## Initial production isolation posture

For the first production cohort, especially healthcare customers, prefer **one dedicated EU/EEA data project/account per client** rather than a pooled multi-tenant customer database.

A client data project should contain its own:

- relational database/security boundary;
- object-storage namespace/buckets;
- retrieval/vector index where enabled;
- application/service credentials;
- encryption-key scope;
- backups and retention policy;
- audit/access-log scope.

Shared orchestration and governed capability code may operate across clients, but must acquire a short-lived tenant-scoped authorization before accessing one client's data plane.

A later pooled architecture is an optimisation, not the default. It requires explicit assurance that row-level/attribute-based access control, object-store isolation, key scoping, backup/restore, telemetry, batch jobs and retrieval indexes cannot cross tenant boundaries.

## Data stores

### 1. Evidence Vault — original and submitted evidence

Purpose: retain source documents and other evidence with provenance.

Target properties:

- EU/EEA storage by default;
- encryption in transit and at rest;
- versioned/immutable object identity where practical;
- content hash and evidence ID;
- tenant-scoped access policy;
- classification, source, received date, retention state and legal-hold metadata;
- malware/content-safety scanning before downstream processing;
- no public URLs;
- controlled download/export logging.

Original evidence can contain direct identifiers and special-category data. It must never be assumed safe for external model egress.

### 2. Canonical Client State Store — structured organisational privacy state

Purpose: durable structured state used across workflows.

Typical objects:

- organisation/legal entities/units;
- engagements and service commitments;
- processing activities;
- systems/applications;
- processors/recipients;
- purposes, data categories, data subjects and legal bases;
- retention rules;
- measures/controls;
- assessments, findings, actions and approvals;
- accepted facts, contradictions and superseded facts;
- deliverable lineage.

Every material state object must support:

- stable ID;
- tenant/organisation ID;
- provenance/evidence references;
- lifecycle state;
- created/updated/effective timestamps;
- version or immutable revision identity;
- review/approval metadata where applicable;
- dependency links used for impact propagation.

The state store is the operational source of truth. Word/PDF/Excel outputs are projections from a defined state version.

### 3. Retrieval Index — derived AI-search material

Purpose: permit tenant-scoped retrieval without repeatedly placing an entire dossier in a model context.

Rules:

- embeddings/chunks are customer data and inherit source classification;
- no cross-client/global customer vector index;
- every chunk is bound to tenant ID, evidence ID, source version and classification;
- retrieval is filtered by tenant before ranking, never filtered only after retrieval;
- indexes must be rebuildable from governed source evidence;
- deletion/retention of a source must propagate to derived chunks/embeddings;
- raw identifiers should be scrubbed/minimised before indexing whenever the use case allows;
- the index is not authoritative evidence without a link back to the exact source object/version.

### 4. Workflow + Audit Store

Purpose: reconstruct what the system and humans did.

Store at least:

- run/workflow/stage IDs;
- input snapshot/version references and hashes;
- policy/model/prompt/source versions;
- retrieval evidence references;
- model-call decision/egress classification;
- validator outcomes;
- human review decisions;
- state mutations/proposals;
- deliverable hashes;
- errors/abstentions/blocks;
- access/security-relevant events.

Prefer event/append-oriented semantics for material decisions. Audit records should contain the minimum customer content needed to prove lineage; avoid duplicating full documents into audit logs.

### 5. Delivery Artifact Vault

Purpose: retain generated/reviewed customer-facing artefacts.

Examples:

- reviewed DPIA;
- RoPA export;
- privacy baseline;
- management report;
- action plan;
- evidence/source appendices;
- signed/approved delivery package.

Each artifact records which client-state, evidence, legal-source, workflow and review versions produced it.

### 6. Key and Secret Boundary

Encryption keys, credentials and provider secrets do not live in GitHub content or the client database.

Use a dedicated secrets/KMS capability with:

- per-environment separation;
- preferably per-client data-encryption-key scope;
- key rotation;
- auditable use;
- least privilege;
- separation between application credentials and encryption-key administration.

## Scrub boundary

SolidPrivacy Scrub remains a special trust boundary.

Preferred flow:

```text
ORIGINAL EVIDENCE
  -> tenant Evidence Vault / controlled local source
  -> Scrub local/trusted processing
       -> scrubbed/minimised artifact
       -> local/private Scrub Key + replacement mapping
  -> AI workflow receives scrubbed/minimised artifact only
  -> reviewed scrubbed result
  -> local/trusted reinsert service
```

The external AI path never receives the Scrub Key or replacement mapping. Where originals must be centrally retained, access to originals and access to reinsertion/key material should be separable roles/capabilities rather than one broad AI service credential.

`scrubbed=true` is still not an anonymity claim; scrubbed material can remain personal data and retains a data classification/egress policy.

## AI access model

The model is not the dossier store.

A governed model call should work as follows:

```text
workflow + tenant identity + purpose
  -> authorization
  -> scoped state/evidence retrieval
  -> minimisation/scrub policy
  -> approved provider/model policy
  -> bounded model context
  -> structured result
  -> validation
  -> durable result/audit in client data plane
```

Requirements:

1. A model/provider never receives database credentials or unrestricted direct access to a client store.
2. Context is assembled by the SolidPrivacy runtime under tenant authorization.
3. Only the minimum required chunks/facts are supplied.
4. External provider use requires explicit policy for content classification, location/transfer, training, retention and logging.
5. Provider-side training on client content is prohibited unless an explicit future product/legal decision overrides the default; production policy should require no-training terms.
6. Provider retention/content logging must be disabled or contractually/policy-bounded according to the approved provider posture.
7. Application telemetry must not copy prompt/document content into general logs by default.
8. Cross-client conversational/model memory is prohibited.
9. Any persistent cache or conversation history is a client-data object with tenant, retention and deletion semantics.
10. Model outputs are proposals until validated/reviewed; reading a fact does not make it accepted client state.

## Residency and transfers

Default production posture:

- Client Data Plane in EU/EEA;
- backups in EU/EEA;
- no external AI/data processor outside the approved transfer posture;
- processor/subprocessor and transfer metadata maintained as part of the platform's own vendor governance;
- any exception is an explicit documented architecture/legal decision, not an accidental provider default.

EU residency alone is not treated as sufficient security or transfer compliance; provider entity, subprocessors, access/support paths and contractual posture still require review.

## Identity and access control

Access must be derived from authenticated identity plus tenant, role and purpose.

Minimum role separation should support:

- client contributor/uploader;
- client reviewer/approver where applicable;
- SolidPrivacy operator;
- qualified Privacy Officer reviewer;
- independent FG/DPO role where contractually applicable;
- platform operations;
- security/key administration.

Use least privilege, short-lived service credentials, MFA for human privileged access, and explicit break-glass access with heightened audit.

No role gets cross-client access merely because it is an AI/runtime service. Cross-client operational functions must acquire separate per-tenant authorization.

## Retention, deletion and legal hold

Retention applies separately to:

- original evidence;
- structured state;
- derived embeddings/chunks;
- model-call payload/result records;
- audit records;
- generated deliverables;
- backups.

A source deletion/expiry must have a documented cascade policy for derived material. Backups require a bounded expiry/restore procedure so deleted customer material does not silently become active again.

Legal hold must be explicit and tenant-scoped.

Engagement termination must produce a deterministic offboarding plan: export/handback, deletion or retained legal/audit evidence, credential revocation and tenant closure.

## Security and assurance requirements before real client data

The Client Data Plane may not be declared production-ready until at least:

- tenant-isolation threat model is documented;
- access-control tests include cross-tenant negative cases;
- object-store and retrieval-index isolation are tested;
- encryption/key management and rotation are evidenced;
- backup/restore respects tenant boundaries;
- deletion cascade is tested;
- audit events cover reads, writes, exports, model egress and privileged access;
- secrets cannot appear in logs or GitHub;
- external model-provider policy is approved for the relevant data classes;
- incident response/runbook exists;
- representative synthetic healthcare corpus passes the same isolation and lifecycle paths;
- independent `governance_release_assurance` issues PASS on the exact production candidate.

## Technology posture

Keep the architecture implementation-neutral. A Postgres-compatible relational store, S3-compatible object storage, tenant-scoped retrieval/vector capability and managed KMS/secrets service are reasonable implementation candidates. A managed EU platform such as Supabase, Azure, AWS or GCP can satisfy parts of this architecture, but no provider is approved merely by being named here.

The first implementation should optimise for auditable isolation and operational simplicity rather than the lowest storage cost. Provider choice is a separate architecture/security/vendor-assessment decision.

## Source-of-truth boundaries

```text
GitHub repository
  = product/governance/legal/workflow source of truth

Client Data Plane
  = real client evidence + operational privacy state source of truth

Control-plane repository
  = shared cross-project governance doctrine/source of truth

Generated documents
  = controlled projections, never independent authoritative state

Model context
  = ephemeral/scoped execution material, never authoritative storage
```
