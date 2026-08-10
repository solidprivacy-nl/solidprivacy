# Website evidence collector

Status: design placeholder.

Initial reference implementation to study: EDPS Website Evidence Collector.

## Intended evidence

- cookies and local/browser storage;
- third-party network requests;
- tracker/remote-host observations;
- timestamps, request metadata and reproducible session context.

## Boundary

The collector reports observations. A separate privacy workflow determines whether an observation creates a legal or compliance finding.

Prefer local execution. Evidence outputs must identify collection time, collector version, target, scope and limitations. No automatic external transmission of captured data is permitted by this placeholder.
