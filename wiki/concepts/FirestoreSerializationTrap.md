---
title: "Firestore Serialization Trap"
type: concept
tags: [firestore, python, bugs, serialization]
---

## Definition

Firestore serializes Python `False` booleans as the string `"false"` when stored and retrieved. A plain Python `if val:` check treats this string as truthy — meaning `if level_up_pending:` passes even when the stored value was `False`.

## Why It's Dangerous

Unit tests typically use real Python dicts with real booleans, so they never reproduce this. The bug only manifests against real Firestore data — discovered only in live-campaign repros.

## Correct Pattern

Use typed helpers that handle all serialization variants:
```python
def _is_state_flag_true(val):
    if isinstance(val, bool): return val
    if isinstance(val, str): return val.lower() in ("true", "1")
    return bool(val)
```

## Connections

- [[LevelUpBugFixPostMortem20260418]] — primary case where this bit 7 flag sites
