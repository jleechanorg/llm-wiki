---
title: "Nested State Management"
type: concept
tags: [state-management, firestore, nested-structures, python]
sources: ["delete-token-processing-tests"]
last_updated: 2026-04-08
---

## Definition

Nested state management refers to the handling of hierarchical data structures in application state, where updates must operate at specific depths without affecting sibling or parent objects.

## Key Patterns

### Selective Preservation
Updates to nested structures must preserve unrelated keys at the same level. If removing `goblin1` from `npc_data`, `merchant` must remain untouched.

### Path-Based Operations
The `__DELETE__` marker works at any depth:
- Top-level: `{"temporary_effect": "__DELETE__"}`
- Nested: `{"npc_data": {"Drake 1": "__DELETE__"}}`
- Deeply nested: `{"world": {"regions": {"forest": {"npcs": {"goblin1": "__DELETE__"}}}}`

### Cross-Section Isolation
Changes in one section (e.g., `npc_data`) must not affect other sections (e.g., `combat_active`, `player_data`).

## Implementation

The `update_state_with_changes` function handles this by recursively traversing the changes dict and applying deletions or updates at the corresponding depth in the state.

## Related

- [[DeleteToken]] — the marker that triggers removal
- [[FirestoreService]] — the service implementing nested state management
- [[delete-token-processing-tests]] — test validation
