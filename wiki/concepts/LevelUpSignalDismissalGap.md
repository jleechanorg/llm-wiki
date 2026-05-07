---
title: "LevelUpSignalDismissalGap"
type: concept
tags: [worldarchitect-ai, rewards-engine, bug, level-up]
date: 2026-04-30
---

## Overview

A dismissal gap pattern where one signal in a pair has a clearance mechanism but the paired signal does not. Specifically: `level_up_available` has a dismissal guard in `_canonicalize_core` (SIM102 block at lines 1499-1506), but `xp_gained` in the non-level-up path does not.

## Key Properties

- **What**: `xp_gained` in the non-level-up XP-progress path has no dismissal guard, while `level_up_available` in the level-up path does
- **Why it matters**: This asymmetry causes stale XP awards to persist across turns. The `level_up_available` dismissal guard was added by PR #6719; the `xp_gained` dismissal was never implemented for the non-level-up case

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| rewards_engine._canonicalize_core | Code | Has SIM102 block for `level_up_available` but no equivalent for `xp_gained` |
| rewards_engine.format_model_level_up_signal | Code | Builds rewards_box from level_up_signal; changed in commit 9814d0d0a |
| _enforce_atomicity | Code | Enforces paired None return but doesn't clear stale values |

## Dismissal Pattern

The pattern is: when a signal's active condition becomes false, the signal should be cleared. For `level_up_available`, this is handled by the SIM102 block at `_canonicalize_core:1499-1506`. For `xp_gained` in the non-level-up path, there is no equivalent guard — the value persists until a new XP award overwrites it.

## See Also
- [[RewardsBoxDismissalGap]]
- [[RewardsEngine]]
- [[RewardsBoxAtomicity]]
