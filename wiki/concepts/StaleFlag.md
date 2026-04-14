---
title: "Stale Flag"
type: concept
tags: [state-management, bug, flag, detection, level-up]
sources: []
last_updated: 2026-04-14
---

## Description
State management anti-pattern where boolean flags retain stale values after their purpose is complete. In modal management, a stale flag can cause incorrect routing decisions.

## Example
After level-up modal completes:
- `level_up_in_progress` should be set to `False`
- If not cleared, system thinks level-up is still in progress
- Related to [[REV-0g1y]] stale flag handling fix

## Level-Up Specific Flags

| Flag | When Stale | Effect |
|------|------------|--------|
| `level_up_in_progress` | After level-up completes | Blocks next level-up |
| `level_up_complete` | Never cleared | Stuck completion state |
| `level_up_pending` | After modal exit | Misleading signal |
| `character_creation_in_progress` | After creation completes | Prevents normal gameplay |

**PR #6262 fix:** Stale flag recovery in `_project_level_up_ui_from_game_state` — checks `level_up_complete=true` OR XP-level mismatch when `resolve_level_up_signal` returns inactive.

## Prevention
- Clear flags explicitly on modal completion
- Use sentinel values (None) vs booleans for tri-state
- Test for both true AND false conditions

## Connections
- [[REV-0g1y]] — fixed stale flag detection
- [[REV-439p]] — also addresses flag handling
- [[GameState]] — manages flag lifecycle
- [[LevelUpBug]] — level-up bug chain including stale flag bugs
