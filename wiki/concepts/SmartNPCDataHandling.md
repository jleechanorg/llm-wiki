---
title: "Smart NPC Data Handling"
type: concept
tags: [npc-data, firestore, state-management, ai-input-handling]
sources: [test-npc-data-handling]
last_updated: 2026-04-08
---

## Definition
A pattern in [[update_state_with_changes]] where AI-provided string values for NPC entries are automatically converted to status field updates, preserving the original NPC dictionary structure.

## How It Works
When the AI proposes changes to npc_data with string values (a common AI mistake), the system:
1. Detects string value vs dict value
2. Preserves all original NPC fields (name, hp_current, hp_max, role, inventory, etc.)
3. Applies the string value to the status field
4. Returns the merged NPC object

## Example
```python
# AI proposes: "Goblin_Leader": "defeated"
# Becomes: "Goblin_Leader": {"name": "Grishnak", "hp_current": 15, "status": "defeated", ...}
```

## Related Patterns
- [[DeleteTokenPattern]] — __DELETE__ token for NPC removal
- [[ListPayloadCoercion]] — converting list-based payloads to dict updates
