---
title: "TestNPCDataHandling"
type: source
tags: [python, testing, npc-data, firestore, state-updates, tdd]
source_file: "raw/test_npc_data_handling.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating smart handling for npc_data in Firestore state updates. Tests verify that AI's string-valued NPC updates get converted to status field updates, preserving original NPC data while applying the string value to the status field.

## Key Claims
- **String to status conversion**: AI string updates like `"Goblin_Leader": "defeated"` convert to status field updates
- **Original data preservation**: NPC dictionary fields (name, hp_current, role) are preserved during updates
- **Delete token support**: AI can delete NPCs using `__DELETE__` special token
- **List payload coercion**: Malformed list-based NPC payloads coerce to dict updates

## Key Tests
- `test_ai_string_update_converts_to_status_field`: Validates string → status field conversion
- `test_ai_updates_specific_npc_fields`: Validates normal dict-based field updates
- `test_ai_delete_npc_with_delete_token`: Validates __DELETE__ token removes NPCs
- `test_ai_updates_npc_entry_from_list_payload`: Validates list coercion to dict

## Connections
- [[update_state_with_changes]] — Firestore service function that applies AI proposed changes
- [[FirestoreStateManagement]] — broader state handling concepts
