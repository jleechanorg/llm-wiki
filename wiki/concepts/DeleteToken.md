---
title: "Delete Token"
type: concept
tags: [state-management, firestore, markers, deletion-patterns]
sources: ["delete-token-processing-tests"]
last_updated: 2026-04-08
---

## Definition

The `__DELETE__` marker is a sentinel value used in state updates to indicate that a specific key should be removed from the state rather than updated. It's processed by the `update_state_with_changes` function in `FirestoreService`.

## How It Works

1. When applying state changes, the function checks each value
2. If a value equals the string `"__DELETE__"`, the corresponding key is removed from the state
3. The deletion works at any nesting level — top-level keys, nested in `npc_data`, or deeply nested paths
4. All other values in the same parent object are preserved

## Use Cases

- **Combat Cleanup**: Removing defeated enemies from `npc_data` after combat
- **Temporary Effects**: Removing expired buffs or effects from state
- **Deep Cleanup**: Removing NPCs nested within world/region structures
- **Mixed Operations**: Combining regular updates with deletions in one operation

## Related

- [[FirestoreService]] — the service containing `update_state_with_changes`
- [[StateManagement]] — broader state handling patterns
- [[delete-token-processing-tests]] — test validation
