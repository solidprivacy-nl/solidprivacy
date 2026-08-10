# WP8 — Client Data Plane + Tenant/Security Boundary

Status: PLANNED — may start only after M1 PASS and WP7 execution/audit primitives are sufficiently defined.

## Outcome

Implement the first production-capable private data plane for real client dossiers and operational privacy state without placing customer data in the shared/public repository or giving an AI provider unrestricted datastore access.

## Why this workpackage exists

The POaaS model requires durable customer dossiers, evidence, state and audit history. That data is materially more sensitive than synthetic workflow fixtures and cannot be treated as an incidental database choice. Tenant isolation, key management, retrieval boundaries, retention and provider egress are prerequisites to safely implementing the client/engagement and persistent-state workpackages that follow.

## Architecture authority

- `docs/DATA_ARCHITECTURE.md`
- `docs/architecture.md`
- `control/PROJECT_GOVERNANCE_BOOTSTRAP.md`
- `control/SOLIDPRIVACY_RELEASE_ASSURANCE_CONTRACT_V1.md`
- model-call privacy policy contracts introduced in WP4

## Scope

### Tenant isolation

- dedicated EU/EEA client data project/account model for initial production cohort;
- tenant identity and authorization contract;
- per-client database/storage/retrieval/key scope;
- environment separation;
- no implicit cross-client operator/runtime access.

### Evidence storage

- encrypted private object storage;
- evidence object/version/hash metadata;
- controlled upload/download;
- source classification and retention state;
- synthetic malware/content-safety path for testing.

### Structured state storage substrate

- relational storage primitives capable of later hosting WP9/WP10 canonical client state;
- immutable/versioned revision support or equivalent change history;
- tenant-bound queries and mutations;
- migration/versioning mechanism.

### Retrieval/index boundary

- tenant-bound document chunk/index model;
- retrieval filtered by tenant before ranking;
- source/evidence/version lineage;
- delete/rebuild semantics;
- no global customer embedding index.

### Secrets/keys

- managed secrets/KMS boundary;
- per-environment and preferably per-client encryption scope;
- key/service-credential rotation evidence;
- no secrets in repository/Actions logs.

### Audit/security events

At minimum capture reads/writes/exports/model-egress/privileged-access and security-relevant failures with minimum necessary content.

### Lifecycle

- retention metadata;
- deletion cascade to derived material;
- backup/restore with tenant boundaries;
- offboarding/credential revocation path;
- legal-hold marker/exception path.

## Initial non-goals

- pooled multi-tenant storage optimisation;
- large client portal UI;
- full canonical client/engagement model (WP9);
- full privacy-state dependency graph (WP10);
- broad production model gateway (WP12);
- migration of real customer data before security assurance PASS.

## Acceptance criteria

1. A synthetic healthcare tenant can ingest evidence and create/read/update tenant-bound structured state.
2. A second synthetic tenant exists and cross-tenant database access is denied in negative tests.
3. Cross-tenant object-store access is denied.
4. Cross-tenant retrieval/index results are impossible in negative tests.
5. Runtime/model-call service receives only tenant-scoped retrieved content and never persistent database credentials.
6. Direct-identifier/Scrub-Key restrictions from prior work remain enforceable at the model boundary.
7. EU/EEA primary storage and backup target posture is evidenced for the selected provider/configuration.
8. Key/secrets configuration and rotation process are evidenced without exposing secrets in GitHub.
9. Deleting/expiring a synthetic evidence object propagates to its derived retrieval material according to policy.
10. Backup/restore does not restore one tenant into another tenant boundary.
11. Audit records exist for sensitive reads, writes, exports, model egress and privileged operations.
12. No real client data appears in repository, Actions logs/artifacts or test fixtures.
13. Target environment/provider/vendor posture is documented and approved for the enabled data classes.
14. Required exact-head CI and live target-environment verification pass.
15. Independent `governance_release_assurance` issues PASS on the exact candidate and target-state evidence.

## Required adversarial tests

- wrong tenant ID;
- manipulated object key/path;
- retrieval query attempting cross-tenant match;
- missing/expired authorization;
- privileged service identity used outside allowed purpose;
- log/exception path containing sensitive payload attempt;
- deletion followed by retrieval attempt;
- restore/import with mismatched tenant metadata;
- model request containing prohibited Scrub Key/direct identifier class;
- provider/policy posture unknown or disallowed.

## Definition of done

WP8 is complete only when implementation, exact-head CI, security/negative tests, live target-state evidence, project records, work-claim disposition and independent assurance are all complete. A configured database alone is not completion.
