---
title: "Digital Signatures"
type: concept
tags: [security, policy, opa, integrity]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
Digital signatures for policy bundles use JWT tokens containing file hashes to verify that policies originate from a trusted source and have not been tampered with in transit. OPA's bundle signing uses asymmetric keys: the bundle author signs with a private key; OPA verifies with the corresponding public key before loading policies.

## Key Properties
- **JWT bundle tokens**: Token contains file hashes and signing metadata
- **Asymmetric key verification**: Private key signs; public key verifies
- **Integrity guarantee**: Any modified file changes the hash and fails verification
- **Source authentication**: Signature proves bundle originated from the claimed source

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA | Policy engine | Bundle signing verification |
| Git commit signing | Version control | GPG signing commits as policy revision trust signal |
| OCI registries | Distribution | Signing container images as policy bundle carriers |

## Connection to ZFC Level-Up Architecture
Digital signatures model the principle that the model contract (prompt files + schema) should be integrity-verified before execution — analogous to how OPA refuses to load unsigned bundles. The ZFC design doc's prompt files should be treated as signed policy documents.

## See Also
- [[OPA-Bundle-Signing]]
- [[Policy-Decoupling]]
- [[ZFC-Level-Up-Architecture]]