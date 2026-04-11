---
title: "PR #5854: fix: surface equipped_items in character sheet display (equipment UI + stat bonuses + schema keys)"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5854.md
sources: []
last_updated: 2026-03-08
---

## Summary
- Fix character-sheet display for campaigns where the LLM stores equipped items in `player_character_data.equipped_items` (canonical slot map) — weapons/armor were invisible to the equipment UI button
- Fix stat bonus calculation to include items from `equipped_items` (e.g. `Ring of Strength +2` was yielding STR bonus = 0)
- Fix `_PLAYER_CHARACTER_SCHEMA_KEYS` missing `equipped_items`, `cantrips`, `spells` — these fields were being stripped from `player_character_data` on every `validate_and_cor

## Metadata
- **PR**: #5854
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +2050/-7428 in 95 files
- **Labels**: none

## Connections
