---
title: "PR #6233: refactor: centralize level/XP architecture (steps 1-2 of 7)"
type: test-pr
date: 2026-04-13
pr_number: 6233
files_changed: [game_state.py, world_logic.py, test_game_state.py, test_world_logic.py]
---

## Summary
Major refactoring to centralize level and XP handling across the codebase. This is steps 1-2 of 7 in the refactoring effort. Moves XP extraction logic into `game_state.py` as canonical `extract_character_xp` function and restructures how level-up signals are resolved.

## Key Changes
- **game_state.py**: Added `extract_character_xp` as the canonical function for extracting character XP from various payload shapes
- **world_logic.py**: Updated to use `extract_character_xp` from game_state, removed duplicate extraction helpers
- **test_game_state.py**: Comprehensive tests for new XP extraction logic
- **test_world_logic.py**: Updated tests to work with new centralized architecture

## Motivation
The previous architecture had duplicated XP extraction logic across multiple files, making it difficult to maintain consistency and causing regressions when changes weren't propagated everywhere.