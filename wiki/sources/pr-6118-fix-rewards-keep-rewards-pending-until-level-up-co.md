---
title: "PR #6118: fix(rewards): keep rewards_pending until level-up completes"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6118.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Stale `rewards_pending.processed: true` while `level_up_available` and the character is still below `new_level` no longer hides pending rewards from routing or `has_pending_rewards()`.
- `_check_and_set_level_up_pending` clears that stale flag on the early-return path when XP already implies the pending target but the stored level has not caught up.
- `GameState.has_pending_rewards()` defensively treats the same inconsistent persisted state as still pending.

## Metadata
- **PR**: #6118
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +494/-125 in 7 files
- **Labels**: none

## Connections
