# Curated legal rules

These rule files are a **machine-readable legal-context layer**, not a replacement for primary legal sources and not a copy of normative text.

Each rule is a short, independently verified paraphrase bound to an approved `source_id`, a concrete article/decision/guideline locator, a jurisdiction, a claim classification (`LAW_REQUIRED` or `REGULATOR_GUIDANCE`) and a verification date.

The runtime rejects `LAW_REQUIRED` rules unless the backing source is registered as authoritative binding law or an authoritative regulator decision. It rejects `REGULATOR_GUIDANCE` rules unless the source is authoritative regulator guidance.

Official methodologies, consultation drafts, standards and engineering references may be supplied as context, but they do **not** enter the authoritative rule set merely because they are useful or official.

Rules should remain concise. Do not reproduce substantial copyrighted guidance or licensed standard text. When the primary source changes, update source/rule verification and rerun legal-context plus workflow regressions.
