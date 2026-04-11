---
title: "Delete Token Processing Tests"
type: source
tags: [python, testing, firestore, state-management, delete-markers]
source_file: "raw/test_delete_token_processing.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive unit tests for `__DELETE__` token processing in the `update_state_with_changes` function within `mvp_site.firestore_service`. Tests validate removing specific keys from nested dictionaries while preserving unrelated state.

## Key Claims
- **Nested NPC Deletion**: `__DELETE__` tokens remove specified keys from nested dictionaries (e.g., `npc_data`) while preserving unrelated entries
- **Top-Level Deletion**: `__DELETE__` works at the top level of state objects, removing entire keys
- **Non-Dict Value Handling**: `__DELETE__` properly handles non-dict values (strings, numbers, lists)
- **Deeply Nested Structures**: Deletion works in deeply nested paths (e.g., `world.regions.forest.npcs`)
- **Mixed Operations**: Regular updates can be combined with deletions in a single operation

## Key Test Cases
- `test_nested_npc_deletion`: Verifies Drake 1 and Drake 2 removed from `npc_data` while Lyra (ally) remains
- `test_top_level_deletion`: Verifies `temporary_effect` removed while `player_data` and `world_data` preserved
- `test_delete_non_dict_value`: Validates deletion works on numeric, string, and list values
- `test_deeply_nested_deletion`: Tests deletion at 4+ levels deep in nested structures
- `test_mixed_updates_and_deletions`: Validates combining regular updates with `__DELETE__` markers

## Connections
- [[FirestoreService]] — contains the `update_state_with_changes` function being tested
- [[DeleteToken]] — the `__DELETE__` marker pattern for state removal
- [[NestedStateManagement]] — the broader concept of handling nested dictionary updates
