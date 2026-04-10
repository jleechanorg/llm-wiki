---
title: "Dot-Notation Transaction Update"
type: concept
tags: [firestore, transaction, dot-notation, settings-preservation]
sources: [api-key-rotation-firestore-regression-tests]
last_updated: 2026-04-08
---

Firestore transaction method using dot-notation keys like `settings.personal_api_key_hash` to update specific nested fields without overwriting sibling fields. Unlike `transaction.set()` with a nested dict (which replaces the entire parent dict), dot-notation update merges only the specified field while preserving other fields at the same level.

## Use Case
When updating user settings, use dot-notation to preserve existing settings:
```python
# Correct: preserves gemini_api_key, openclaw_gateway_url, etc.
txn.update(user_ref, {"settings.personal_api_key_hash": new_hash})

# Wrong: would overwrite all settings
txn.set(user_ref, {"settings": {"personal_api_key_hash": new_hash}})
```

## Related
- [[FirestoreService]] — uses this pattern for API key rotation
- [[APIKeyRotation]] — operation that requires settings preservation
