---
title: "OPA Bundle Files"
type: concept
tags: [opa, policy-deployment, packaging, cncf]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
OPA bundle files are `.tar.gz` archives containing `.rego` policy files and `.json`/`.yaml` data files with an optional `.manifest` for metadata. Bundles enable distributed policy deployment: policies are versioned, signed, and pulled by OPA from an OCI registry or HTTP server at startup or at runtime with hot reload.

## Key Properties
- **Packaged format**: `.tar.gz` containing Rego policies + data files
- **Manifest metadata**: Optional `.manifest` with revision hash, description, metadata
- **OCI registry support**: Distributed via Docker/OCI artifact standard
- **Hot reload**: Updated policies activated on startup or on signal without restart
- **Bundle persistence**: Downloaded policies persist to disk for recovery

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA | Policy engine | Bundle consumer |
| Regal | Rego linter | Validates bundle Rego files before deployment |
| Conftest | Static analyzer | Tests bundle policies before deployment |

## Connection to ZFC Level-Up Architecture
Bundle files are the deployment mechanism for policy-as-code — analogous to how the ZFC design doc specifies that prompt files are the model contract that must be deployed together with the formatter code. Separating policy (prompts) from enforcement (formatter) and versioning them as a unit is the bundle pattern.

## See Also
- [[OPA]]
- [[Digital-Signatures]]
- [[Policy-as-Code]]
- [[OPA-Bundle-Signing]]