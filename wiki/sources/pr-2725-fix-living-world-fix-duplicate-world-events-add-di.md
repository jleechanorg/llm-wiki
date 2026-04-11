---
title: "PR #2725: fix(living-world): Fix duplicate world_events + add diagnostic tool"
type: source
tags: []
date: 2025-12-28
source_file: raw/prs-worldarchitect-ai/pr-2725.md
sources: []
last_updated: 2025-12-28
---

## Summary
- **Bug Fix**: Stop duplicating cumulative world_events to story entries
- **New Tool**: Add `scripts/check_living_world.py` diagnostic script

### Bug Fix Details
**Problem**: `world_events` from `game_state` (cumulative) were being copied to every story entry's `structured_fields`, causing all turns to display the same events (e.g., "Turn 27" events appearing in turns 280+).

**Solution**: Now extracts `world_events` from the LLM response's `structured_fields` (this turn's new events only) ins

## Metadata
- **PR**: #2725
- **Merged**: 2025-12-28
- **Author**: jleechan2015
- **Stats**: +566/-9 in 3 files
- **Labels**: none

## Connections
