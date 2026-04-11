---
title: "PR #3081: feat: Add DeferredRewardsAgent for parallel rewards processing every 10 scenes"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-3081.md
sources: []
last_updated: 2026-02-01
---

## Summary
Add **DeferredRewardsAgent** for parallel rewards processing that automatically catches missed XP/loot every 10 scenes.

### Key Features
- **Parallel Injection**: Runs IN PARALLEL with StoryModeAgent (same LLM call, not separate inference)
- **Automatic Triggering**: Every 10 scenes (configurable via `DEFERRED_REWARDS_SCENE_INTERVAL`)
- **Semantic Routing**: User can also explicitly request via natural language ("check for missed rewards")
- **Explicit API Mode**: Programmatic access via `mode=

## Metadata
- **PR**: #3081
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +1369/-7 in 34 files
- **Labels**: none

## Connections
