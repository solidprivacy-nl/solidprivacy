# OSCAL-inspired control adapter

Status: architecture placeholder; no NIST OSCAL content vendored.

Reference: `https://pages.nist.gov/OSCAL/`

SolidPrivacy will use OSCAL primarily as an architectural reference for machine-readable controls, implementation, assessment, evidence, findings and remediation.

## Initial mapping target

```text
external control concept
  -> SolidPrivacy control
  -> implementation state
  -> evidence references
  -> assessment result
  -> finding
  -> remediation
  -> approval / closure
```

This adapter does not imply OSCAL conformance. Any future claim of conformance requires explicit schema/version validation and tests.
