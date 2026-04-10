---
title: "Deep Copy Semantics"
type: concept
tags: [python, memory, data-structures, testing]
sources: []
last_updated: 2026-04-08
---

Programming pattern where copied data is completely independent from the original — modifications to the copy do not affect the source. Critical for simulating server-side storage behavior where data exists in a separate state from application memory.

## Why It Matters for Testing
Real databases (like Firestore) store data on the server. When code modifies a dict after persisting it to the database, the original dict change should NOT affect the stored document. Fakes must replicate this to catch bugs.

## Implementation
```python
import copy
self._data = copy.deepcopy(data)
```

## Related Pages
- [[Fake Firestore Implementation]] — uses deep copy to simulate server storage
