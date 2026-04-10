---
title: "API Key Rotation"
type: concept
tags: [api-key, security, firestore, settings]
sources: [api-key-rotation-firestore-regression-tests]
last_updated: 2026-04-08
---

Security operation that generates a new API key hash for a user while invalidating the old key. Critical requirement: preserve existing user settings (gemini_api_key, openclaw_gateway_url, etc.) during rotation or revocation.

## Operations
- **Rotate**: Generate new key hash, update stored hash
- **Revoke**: Clear stored hash, invalidate key

## Implementation Requirement
Both operations must use [[DotNotationTransactionUpdate]] with `transaction.update()` and dot-notation keys to ensure settings preservation. Fix commit eea7c67cba ensured this behavior.

## Related
- [[FirestoreService]] — implements rotation functions
- [[APIRotationRegressionTests]] — validates the fix
