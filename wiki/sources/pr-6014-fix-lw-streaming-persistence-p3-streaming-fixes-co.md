---
title: "PR #6014: fix(lw+streaming): persistence + P3 streaming fixes combined"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldarchitect-ai/pr-6014.md
sources: []
last_updated: 2026-03-19
---

## Summary
- **rev-lw5lk / rev-lwuz5 (P1)**: Persist `full_state_updates` and `game_state_snapshot` in every story entry so Living World deltas are never lost; lazy-init `game_states` subcollection for old campaigns that predate it
- **rev-lw-warn-freeze-guard (P2)**: `_warn_if_living_world_missing` now accepts `should_freeze_time` and skips the warning when time is frozen, preventing false-positive LW warnings
- **rev-stream-sign-env (P3)**: Inject `STREAM_RESPONSE_SIGNING_SECRET` in test env so signature

## Metadata
- **PR**: #6014
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +1065/-893 in 6 files
- **Labels**: none

## Connections
