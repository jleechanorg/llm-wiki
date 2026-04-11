---
title: "PR #6071: fix(world_logic): suppress stale level-up banner after character creation completes"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldarchitect-ai/pr-6071.md
sources: []
last_updated: 2026-04-02
---

## Summary
- suppress stale level-up signal after level-up completion when `character_creation_completed=true` and `level_up_complete=true`
- prevent stale `rewards_pending.level_up_available` from reactivating level-up banner on next turn

## Metadata
- **PR**: #6071
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +92/-13 in 2 files
- **Labels**: none

## Connections
