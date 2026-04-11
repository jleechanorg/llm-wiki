---
title: "PR #5946: fix: centralize turn tracking, fix living-world UI rendering and payload normalization"
type: source
tags: []
date: 2026-03-13
source_file: raw/prs-worldarchitect-ai/pr-5946.md
sources: []
last_updated: 2026-03-13
---

## Summary
- Centralize turn tracking via `_increment_turn_counter()` as single source of truth in `world_logic.py`
- Fix living-world payload normalization: handle `world_events.append` format (LLM sometimes returns `{append:[...]}` instead of `{background_events:[...]}`) so events surface in UI on every structured turn
- Fix living-world UI rendering: remove `debugMode` gate from `hasLivingWorldData` in `app.js` so all users (not just debug sessions) see world events
- Fix `game_state.turn_number` serial

## Metadata
- **PR**: #5946
- **Merged**: 2026-03-13
- **Author**: jleechan2015
- **Stats**: +1247/-175 in 25 files
- **Labels**: none

## Connections
