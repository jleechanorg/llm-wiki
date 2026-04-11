---
title: "PR #219: [antig] fix: companion and player state mutations idempotent on tick replay (wc-ca0)"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-219.md
sources: []
last_updated: 2026-04-04
---

## Summary
Re-running `simulateWorldTick` on an already processed deterministic tick was triggering `updateCompanion` and `UPDATE sessions SET state` unconditionally, even though the `saveCompanionAction` or `player_offline_actions` inserts were silently ignored due to unique ID constraints (idempotent DB layer). This violated idempotency rules and risked overwriting concurrent player UI changes with stale state from a replay tick.

## Metadata
- **PR**: #219
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +44/-35 in 3 files
- **Labels**: none

## Connections
