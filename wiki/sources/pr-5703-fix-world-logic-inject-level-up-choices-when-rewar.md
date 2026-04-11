---
title: "PR #5703: fix(world_logic): inject level-up choices when rewards_box.level_up_available=true but rewards_pending=null"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5703.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Fixes REV-wqwx: level-up indicator shows "LEVEL UP AVAILABLE!" but no clickable buttons appear
- Root cause: LLM returns `rewards_box.level_up_available=true` (deferred rewards) while also setting `state_updates.rewards_pending=null`, bypassing server-side choice injection
- Added `rewards_box` parameter to `_inject_levelup_choices_if_needed` with fallback synthesis

## Metadata
- **PR**: #5703
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +554/-12 in 2 files
- **Labels**: none

## Connections
