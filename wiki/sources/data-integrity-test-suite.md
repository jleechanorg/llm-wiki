---
title: "Data Integrity Test Suite"
type: source
tags: [python, testing, data-corruption, firestore, game-state, regression]
source_file: "raw/test_data_integrity.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test suite that validates data structure integrity, catching bugs where NPCs are converted to strings, state inconsistencies occur, or other data structure violations occur. Tests the `update_state_with_changes` function and NPC data validation to prevent silent data corruption.

## Key Claims
- **NPC Structure Validation**: Every NPC in `npc_data` must be a dictionary, not a string or other type
- **State Update Integrity**: State updates via `update_state_with_changes` preserve data structure, preventing dict fields from being overwritten with strings
- **Corruption Detection**: Tests detect when AI updates or other processes corrupt data structures
- **Recursive Merge Safety**: Validates that nested dictionary updates don't destroy existing structure

## Key Quotes
> "Test version of NPC validation that returns issues instead of logging."

## Connections
- [[FirestoreService]] — the module being tested for state update integrity
- [[GameState]] — GameState class used in tests
- [[DataIntegrityValidation]] — concept of validating data structures at runtime

## Contradictions
- None identified
