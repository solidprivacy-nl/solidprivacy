# Model call policies

Model call policies are executable privacy-boundary configurations. They are not provider endorsements and do not establish that a named provider is legally or contractually acceptable.

Before any model invocation the runtime evaluates the request against `contracts/model_call_policy.schema.json` and the deterministic gate in `src/solidprivacy/runtime/ai_boundary.py`.

`privacy_context.scrubbed=true` is **not** a declaration that content is anonymous or outside data-protection law. `scrubbed_personal_data` therefore has its own explicit egress permission.

For the WP4 external boundary: a Scrub Key is always rejected; direct identifiers are rejected; unknown direct-identifier status is rejected for sensitive content; scrubbed-personal-data egress requires explicit permission; raw personal/special-category data requires separate permissions; and unresolved provider training, retention or sensitive-content logging posture blocks the call.

A policy marked `approved=true` requires an approver and approval timestamp. Real provider policies should also carry a review date because provider terms/settings can change.

The fixture policy under `evals/ai_fact_extraction/` exists only for CI. It approves no real provider.
