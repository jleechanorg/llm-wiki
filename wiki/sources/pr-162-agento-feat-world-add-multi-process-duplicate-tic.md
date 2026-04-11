---
title: "PR #162: [agento] feat(world): add multi-process duplicate-tick safety (worldai_claw-e0c)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-162.md
sources: []
last_updated: 2026-03-31
---

## Summary
Add SQLite-backed atomic check-and-set guard to prevent concurrent `world_scheduler` instances from double-processing the same campaign tick during rolling deploys or multi-instance deployments.

## Metadata
- **PR**: #162
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +447/-48 in 7 files
- **Labels**: none

## Connections
