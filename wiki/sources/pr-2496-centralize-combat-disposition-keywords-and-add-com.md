---
title: "PR #2496: Centralize combat disposition keywords and add CombatDisposition enum"
type: source
tags: []
date: 2025-12-19
source_file: raw/prs-worldarchitect-ai/pr-2496.md
sources: []
last_updated: 2025-12-19
---

## Summary
Addresses code review feedback on PR #2454's keyword-based approach by centralizing the combat disposition logic and adding formal type-safe structures.

### Changes:
- **constants.py**: Added `FRIENDLY_COMBATANT_TYPES` and `GENERIC_ENEMY_ROLES` frozensets with helper functions `is_friendly_combatant()` and `is_generic_enemy_role()`
- **game_state.py**: Refactored `_is_named_npc()` and `cleanup_defeated_enemies()` to use centralized constants instead of inline keyword sets
- **entities_pydantic.

## Metadata
- **PR**: #2496
- **Merged**: 2025-12-19
- **Author**: jleechan2015
- **Stats**: +167/-13 in 4 files
- **Labels**: none

## Connections
