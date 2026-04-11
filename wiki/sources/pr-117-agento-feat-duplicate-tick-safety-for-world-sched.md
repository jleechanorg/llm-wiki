---
title: "PR #117: [agento] feat: duplicate-tick safety for world_scheduler (worldai_claw-e0c)"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-117.md
sources: []
last_updated: 2026-03-29
---

## Summary
The WorldScheduler uses in-process flags (`schedulerLock`/`isRunning`) to prevent concurrent ticks. However, in multi-process or crash-restart scenarios, the same tick could be double-processed, causing duplicated faction simulations and companion actions.

## Metadata
- **PR**: #117
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +141/-1 in 3 files
- **Labels**: none

## Connections
