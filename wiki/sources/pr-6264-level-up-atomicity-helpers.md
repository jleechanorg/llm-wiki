---
title: "PR #6264: Level-Up Atomicity Helpers"
type: source
tags: [worldarchitect, level-up, atomicity, refactor]
date: 2026-04-14
source_file: raw/pr-6264-level-up-atomicity-helpers.md
---

## Summary
PR #6264 extracts inline stuck-completion reconciliation into `ensure_level_up_rewards_box` and `ensure_level_up_planning_block` module-level helpers, and adds postcondition assertions verifying rewards_box exists whenever level_up_complete=True.

## Key Claims
- **Helper extraction**: Inline stuck-completion code extracted to module-level `ensure_level_up_rewards_box` and `ensure_level_up_planning_block`
- **Postcondition assertions**: Verifies rewards_box exists when level_up_complete=True
- **TDD approach**: RED tests written first, then GREEN implementation
- **New test file**: `test_level_up_atomicity.py` with 9 tests

## Connections
- [[LevelUpBug]] — bug chain
- [[RewardsBoxAtomicity]] — atomicity helpers
- [[StaleFlag]] — stuck completion detection
