# POaaS Reference Workflow

## Purpose

This document defines the reference customer-lifecycle workflow for SolidPrivacy **Privacy Officer as a Service (POaaS)**. It translates the repository's governed privacy-workflow architecture into a repeatable service flow from signed engagement to initial deliverables and continuous operation.

It is a product/architecture reference, not a promise that all stages are implemented today. `ROADMAP.md` defines the implementation sequence.

## Reference customer

Synthetic example:

- medium-sized Dutch healthcare organisation;
- primarily home care / district nursing;
- approximately 1,200 employees and 4,000 clients;
- EU/EEA + Netherlands jurisdiction;
- ECD, planning, HR/payroll, Microsoft 365, website/client portal and care-technology suppliers;
- service: Privacy Officer as a Service.

No real customer evidence or identifiers belong in the shared SolidPrivacy repository.

## Architectural interpretation

The governed repository is the **capability factory**. It contains canonical semantics, legal-source governance, methodologies, contracts, workflows, controls, policies and evaluations.

Each customer requires an isolated **client operating state** containing the organisation-specific facts and evidence over which those capabilities operate.

```text
SHARED / GOVERNED                         ISOLATED / CLIENT-SPECIFIC

legal sources                             organisation + legal entities
jurisdiction packs                        engagement + service commitments
methodologies                             evidence inventory
canonical schemas          --->           accepted privacy facts
workflow definitions                      processing inventory
model-call policies                       systems + processors
control definitions                       assessments + findings
regression/evals                          actions + deliverables
                                           review/audit history
```

The shared layer may know *how* to perform a Dutch DPIA. The client layer knows *which processing activity, evidence, systems and decisions* belong to one customer.

## Central design rule: documents are evidence and projections

Incoming policies, contracts, spreadsheets and diagrams are evidence. They are not automatically authoritative organisation state.

Outgoing RoPA, DPIA and management reports are projections of reviewed structured state. They are not independent databases that must later be manually reconciled.

```text
incoming documents / answers / collector evidence
                   |
                   v
             evidence objects
                   |
                   v
       extracted / proposed facts
                   |
        provenance + contradiction
                   |
             human acceptance
                   |
                   v
     persistent organisational state
       /        |         |         \
     RoPA      DPIA     vendor     report
```

A changed fact therefore updates or supersedes structured state and creates downstream impact/review signals. It does not silently rewrite approved documents.

## Reference service flow

### 1. Signed engagement

Input:
- customer identity and legal entities;
- service package;
- jurisdictions;
- service period;
- agreed scope/exclusions;
- promised deliverables;
- designated customer contacts and SolidPrivacy reviewers.

System output:
- organisation record;
- engagement record;
- deliverable manifest;
- initial evidence requirements;
- initial due/decision dependencies.

Example deliverables might include:
- privacy baseline;
- governance/role summary;
- processing register;
- DPIA screening register;
- selected DPIAs;
- processor/vendor overview;
- improvement/action register;
- management report.

### 2. Evidence request and intake

The service package and known organisation profile determine an initial evidence request. Typical categories:
- existing RoPA;
- DPIAs/pre-scans;
- privacy policy/notice;
- processor/vendor register and agreements;
- breach and DSAR procedures;
- retention policy;
- system/application inventory;
- information-security evidence relevant to privacy controls;
- organisational charts/roles;
- architecture diagrams;
- care-technology documentation.

Each item receives evidence metadata including source, date/version, scope, client ownership and privacy classification.

Sensitive input is routed according to the Scrub/minimisation and model-egress policy. The presence of a workflow never implies permission for cloud processing.

### 3. Classification and evidence registration

Documents/evidence are classified by type and potential workflow relevance.

The system should answer:
- what evidence was expected;
- what has been received;
- what is usable;
- what requires Scrub/local handling;
- what appears duplicated/outdated;
- what cannot yet be interpreted reliably.

No substantive legal conclusion is needed at this stage.

### 4. Fact extraction and normalisation

AI or deterministic parsers propose privacy facts and map them to canonical concepts such as:
- processing activity;
- purpose;
- data subject;
- personal-data category;
- system;
- controller/processor/recipient;
- legal basis;
- retention;
- technical/organisational measure.

Observed/inferred facts remain tied to evidence and exact support. Assumptions remain explicit.

### 5. Provenance, contradiction and missing-information analysis

The validator separates:
- supported facts;
- unreviewed facts;
- contradictions;
- missing material information;
- stale or weak evidence.

Example:

```text
CONTRADICTION
processing: client health record
source A: RoPA -> retention 15 years
source B: retention policy -> retention 20 years
next action: customer/privacy-officer resolution
```

The system does not select the convenient answer merely because one document looks more recent.

### 6. Targeted client questions

After evidence analysis, generic intake should narrow into targeted questions generated from validated gaps.

Examples:
- Which retention period is actually applied to the client record?
- Is supplier X currently used for this processing activity?
- Does location tracking operate continuously or only during an active care visit?

Answers become evidence/user-confirmed facts with provenance. Model-generated wording is not itself a legal requirement.

### 7. Persistent organisational privacy state

Accepted facts are promoted into versioned client state.

Important objects include:
- organisation/legal entity;
- organisational unit;
- system/application;
- processing activity;
- data subject/data category;
- purpose/legal basis;
- processor/recipient;
- retention rule;
- security/privacy measure;
- assessment;
- control/finding/action.

State must preserve lifecycle such as proposed, provenance-valid, human-accepted, superseded or disputed.

### 8. RoPA / processing inventory

The processing inventory becomes the organisational backbone rather than a one-off spreadsheet.

A client-grade Article 30 register is generated as a projection of approved state.

The same underlying processing objects become inputs to:
- DPIA screening;
- vendor assessment;
- retention governance;
- international-transfer assessment;
- breach scoping;
- DSAR discovery/scoping.

### 9. DPIA screening and DPIA execution

Relevant processing activities pass through governed pre-scan/necessity support.

The existing DPIA vertical slice demonstrates the intended internal pattern:

```text
evidence
 -> facts/provenance
 -> readiness
 -> deterministic pre-scan/legal gate
 -> governed legal context
 -> structured DPIA analysis
 -> validator
 -> Privacy Officer review
 -> scrubbed report/reinsert/audit
```

Methodology results remain separate from binding-law conclusions. Material residual-risk and consultation decisions remain human-accountable.

### 10. Baseline, controls and findings

The organisational state and available evidence are assessed against governed control/requirement sets.

A finding must connect to evidence and, where legal, to an approved legal rule/source classification.

Operational representation:

```text
control
 -> implementation
 -> assessment
 -> evidence
 -> finding
 -> remediation
 -> owner / due date
 -> verification
 -> approval/closure
```

Recommendations therefore become work, not prose that disappears into a report.

### 11. Privacy Officer review

AI should concentrate human effort on judgement-heavy items:
- disputed or incomplete facts;
- legal interpretation requiring human acceptance;
- proportionality/necessity judgements;
- high-impact findings;
- residual risk;
- prior consultation;
- rights-affecting decisions;
- material changes to accepted organisation state.

Review actions should support accept, reject, change and request-evidence with rationale where material.

### 12. Deliverable production

Promised deliverables are generated from the reviewed state and assessment outputs.

Potential initial package:
- processing register;
- DPIA register and selected reviewed DPIAs;
- privacy baseline;
- processor/vendor coverage overview;
- improvement/action register;
- governance summary;
- management report.

Each deliverable records the state/evidence/source/review version from which it was produced.

### 13. Delivery state

The engagement should expose a machine-readable delivery status, for example:

```text
RoPA                    complete
DPIA register           complete
ECD DPIA                needs PO review
privacy baseline        complete
processor assessment    waiting on client
improvement plan        blocked by 2 unresolved facts
```

This status is derived from workflow/dependency state, not manually maintained presentation text.

### 14. Continuous service

Onboarding creates a living privacy state rather than closing the file.

Future inputs include:
- new supplier;
- new system;
- changed processing purpose;
- new data category;
- incident;
- DSAR;
- evidence expiry;
- remediation completion;
- legal-source update.

Changes generate impact events. Example:

```text
processor changed
   -> processing object impacted
   -> Article 28 review impacted
   -> transfer assessment possibly impacted
   -> DPIA facts possibly stale
   -> RoPA projection stale
   -> Privacy Officer work items created
```

Previously approved conclusions are not silently rewritten.

## Division of labour

### AI / deterministic automation
- classify evidence;
- extract and normalise facts;
- find duplicates/conflicts/gaps;
- build targeted questions;
- apply deterministic assessment gates;
- retrieve governed legal context;
- produce first analyses/drafts;
- maintain cross-object consistency;
- generate structured deliverable projections.

### Operational privacy support
- chase missing evidence;
- resolve administrative/low-risk gaps;
- maintain supplier/system information;
- prepare review packages;
- track remediation/evidence.

### Qualified Privacy Officer / DPO/FG where applicable
- accept/reject material facts and conclusions;
- interpret context where deterministic rules are insufficient;
- decide proportionality/necessity and residual risk;
- make high-impact rights/breach/transfer/consultation decisions;
- approve client-facing material conclusions.

This separation enables scaling without representing AI confidence as legal truth.

## Required architecture objects revealed by this workflow

The customer journey exposes several objects that a single DPIA workflow does not require but POaaS does:

1. `organisation` — durable client identity/scope without mixing tenants;
2. `engagement` — what service is currently contracted;
3. `deliverable_commitment` — what has been promised and its state;
4. `evidence_requirement` — what information/evidence the service needs;
5. `client_question` — targeted unresolved dependency and answer provenance;
6. `organisational_privacy_state` — accepted reusable facts independent of one workflow run;
7. `state_change_event` / dependency impact — what became stale after a change;
8. `work_item` — who must do what next and why;
9. `deliverable_projection` — client document/report generated from known reviewed state.

These should be implemented as explicit contracts or canonical objects rather than hidden fields inside prompts or UI databases.

## Reference acceptance philosophy

A feature is not POaaS-ready merely because it can generate a plausible document.

A reference customer flow is acceptable only when the system can demonstrate:
- why information was requested;
- where each material fact came from;
- which contradictions remain;
- which legal sources supported a material claim;
- who approved high-impact conclusions;
- what deliverables remain due/blocked;
- what client state was current at delivery;
- what changed later and which prior outputs require reassessment.

See `ROADMAP.md` for M1 (integrated DPIA) and M2 (integrated synthetic POaaS onboarding) acceptance milestones.
