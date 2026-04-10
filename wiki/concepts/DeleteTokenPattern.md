---
title: "Delete Token Pattern"
type: concept
tags: [npc-data, deletion, firestore, state-management]
sources: [test-npc-data-handling]
last_updated: 2026-04-08
---

## Definition
A special token `__DELETE__` that AI can use to explicitly remove NPCs from npc_data during state updates.

## How It Works
When the AI sets an NPC entry to the special string `__DELETE__`, the system removes that NPC key entirely from npc_data rather than updating it.

## Example
```python
ai_proposed_changes = {"npc_data": {"Bandit_1": "__DELETE__"}}
# Result: Bandit_1 key is removed from npc_data
```

## Related Patterns
- [[SmartNPCDataHandling]] — string value handling
- [[FirestoreStateManagement]] — broader state update patterns
