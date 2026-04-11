---
title: "API Key Rotation Firestore Regression Tests"
type: source
tags: [python, testing, firestore, api-key, transaction, regression-tests, dot-notation]
source_file: "raw/test_api_key_rotation_regression.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Regression tests validating that `rotate_personal_api_key` and `revoke_personal_api_key` use dot-notation `transaction.update()` (not `transaction.set()` with nested dict) when updating existing user documents. This preserves existing settings fields like `gemini_api_key`, `openclaw_gateway_url`, etc. on API key generate/revoke operations.

## Key Claims
- **Dot-notation update preserves settings**: Using `transaction.update()` with dot-notation keys like `settings.personal_api_key_hash` preserves other settings fields
- **set() would overwrite settings**: Calling `transaction.set()` on user_ref for existing users would overwrite all settings
- **New user uses set(merge=True)**: When user doc doesn't exist, uses `set(merge=True)` to create with defaults
- **Fix commit eea7c67cba**: The fix "use dot-notation update to preserve settings on API key rotate/revoke" introduced this behavior

## Key Quotes
> "The critical wiring: user_ref.get.return_value = user_snap so that the production code's `user_ref.get(transaction=transaction)` returns our controlled snapshot with the correct .exists value."

## Connections
- [[FirestoreService]] — module containing the functions under test
- [[FirestoreTransaction]] — covers dot-notation update vs set behavior
- [[APIKeyRotation]] — concept for rotate/revoke operations

## Contradictions
- None identified
