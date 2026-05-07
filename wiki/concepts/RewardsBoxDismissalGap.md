---
title: "RewardsBoxDismissalGap"
type: concept
tags: [worldarchitect-ai, rewards-engine, bug, xp-gained]
date: 2026-04-30
---

## Overview

A dismissal gap in the `rewards_engine` where non-level-up `xp_gained` has no clearance mechanism. When a user earns XP (e.g., `xp_gained=2300` from a combat), the value persists in `structured_fields.rewards_box` across subsequent turns even when no new XP award occurs.

## Key Properties

- **What**: Non-level-up XP-progress `rewards_box` (xp_gained > 0 without level_up_available=True) has no dismissal guard
- **Why it matters**: Stale xp_gained renders on every page load via `should_show_rewards_box()`. The LLM's prose acknowledgment ("State Cleanup: Deleted...") does NOT write to Firestore — only the canonicalization path can clear it.

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| rewards_engine._canonicalize_core | Code | Has `level_up_available` dismissal (SIM102) but no `xp_gained` dismissal |
| world_logic.normalize_rewards_box_for_ui | Code | Visibility gate for rewards_box display |
| world_logic._reconcile_level_up_ui_pair | Code | Reconciliation logic — only handles level-up staleness |
| should_show_rewards_box | Code | Returns True when xp_gained > 0 |
| structured_fields.rewards_box | Data | Firestore-persisted rewards_box that carries stale xp_gained |

## Connection to Stale Rewards Box Bug

`_canonicalize_core` non-level-up path (line 1481-1538) merges stale `xp_gained` from `updated_game_state_dict["rewards_box"]` on every turn because:
1. `raw_rewards_box=None` (LLM emits nothing)
2. Line 1486-1488 picks up stale from game state
3. `normalize_rewards_box()` preserves it unchanged
4. Written back to Firestore at world_logic.py:7348

The fix requires adding a dismissal guard: when no new XP award is present on a non-level-up turn, clear `xp_gained` from the merged rewards_box before normalizing.

## See Also
- [[RewardsEngine]]
- [[RewardsBoxAtomicity]]
- [[NormalizationAtomicity]]
- [[Level-Up-Signal-Dismissal-Gap]]
