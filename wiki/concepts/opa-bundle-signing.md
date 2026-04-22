---
title: "OPA Bundle Signing"
type: concept
tags: [opa, security, policy-as-code, integrity, bundle]
sources: [https://www.openpolicyagent.org/docs/latest/]
last_updated: 2026-04-19
---

## Overview
OPA bundle signing uses asymmetric cryptography to verify that policy bundles loaded by OPA originate from a trusted source and have not been tampered with. The bundle author creates a JWT token containing the file hashes; OPA verifies the token's signature against the author's public key before loading any policies. This prevents supply-chain attacks on policy code.

## Key Properties
- **JWT token**: Token contains file hashes (SHA256) and signing metadata
- **Asymmetric keys**: Private key signs; OPA verifies with author's public key
- **Integrity verification**: Any file change invalidates the signature
- **Source authentication**: Signature proves bundle author identity
- **Bundle path**: Default path check; signed bundles only loaded from allowed paths

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| OPA | Policy engine | Verifies signed bundles |
| Digital-Signatures | Concept | Generic concept of cryptographic signing |
| OPA Bundle Files | Deployment | Bundle signing is applied to bundle files |
| Regal | Rego linter | Validates before signing |

## Connection to ZFC Level-Up Architecture
Bundle signing maps to the ZFC model contract: prompt files + schema + formatter code must be deployed as a consistent unit. If the prompt says "emit `previous_turn_exp`" but the formatter doesn't recognize that field, there's a supply-chain mismatch. Bundle signing patterns could enforce version pinning of prompts + formatter together.

## See Also
- [[Digital-Signatures]]
- [[Bundle-Files]]
- [[OPA]]
- [[Rego]]
