# Control Models

This layer represents privacy and governance controls, their implementation state, evidence, findings and remediation.

The design is **OSCAL-inspired**, not a claim of OSCAL conformance.

Minimum conceptual model:

```text
Control
  -> Implementation
      -> Evidence
      -> Assessment
          -> Finding
              -> Remediation
                  -> Approval / closure
```

## Design goals

- make recommendations actionable and traceable;
- separate control intent from implementation evidence;
- support inherent/residual risk links;
- preserve who/what generated evidence and when;
- allow human acceptance or rejection of residual risk;
- support future mapping to ISO 27701, NIST, organisational controls and vendor controls.

Normative standard text must not be copied here unless licensing explicitly permits it.
