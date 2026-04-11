---
title: "NPC Death State Persistence TDD Tests"
type: source
tags: [python, testing, tdd, npc, death-state, firestore]
source_file: "raw/test_npc_death_state_persistence_tdd.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests for NPC death state persistence bug. Tests verify that when a user kills a named NPC (e.g., Marcus), the death state is properly synced between combat_state and npc_data — the NPC should be marked as dead, not deleted.

## Key Claims
- **Named NPCs preserved**: NPCs with meaningful roles or backstories should be marked dead (status: ["dead"]) rather than deleted
- **Death state synchronization**: Dead NPCs preserved in npc_data so LLM knows they're dead in future turns
- **Entity tracking**: Dead NPCs can be referenced in narrative as deceased characters
- **Root cause fix**: Named NPCs identified by role that isn't generic (enemy/minion)

## Key Test
- `test_named_npc_with_role_marked_dead_not_deleted`: Named NPC with role "merchant" preserved with status: ["dead"]
- `test_named_npc_with_backstory_marked_dead_not_deleted`: Named NPC with backstory preserved with status: ["dead"]

## Connections
- [[GameState]] — manages combat and npc_data state
- [[NPC Death State Persistence E2E Tests]] — E2E validation of death state sync
- [[NarrativeResponse]] — references dead NPCs in story generation

## Contradictions
- None
