# Jurisdictions

Jurisdiction-specific overlays live here. The first production scope is EU/EEA + Netherlands.

```text
jurisdictions/
├── eu/
└── nl/
```

A jurisdiction pack may define:

- applicable legal-source sets;
- regulator/source precedence;
- terminology aliases;
- procedural/regulator-specific requirements;
- report/notification adapters;
- jurisdiction-specific evaluation cases.

## Isolation rule

Rules from another jurisdiction must never silently enter an EU/NL workflow. For example, UK ICO guidance may be used as methodology inspiration, but it cannot support an EU/NL legal conclusion unless the proposition is independently grounded in an approved EU/NL source.
