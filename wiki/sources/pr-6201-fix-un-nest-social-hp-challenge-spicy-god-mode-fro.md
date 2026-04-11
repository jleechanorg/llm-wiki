---
title: "PR #6201: fix: un-nest social_hp_challenge/spicy/god_mode from rewards_box gate"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6201.md
sources: []
last_updated: 2026-04-11
---

## Summary
- **Bug**: `social_hp_challenge`, `recommend_spicy_mode`, `recommend_exit_spicy_mode`, and `god_mode_response` were gated inside `if hasattr(structured_response, "rewards_box")`, silently dropped on turns with no rewards_box (pure narrative/combat without XP)
- **Fix**: Moved all four fields to independent if-blocks at the same level as the rewards_box check, matching the pattern for `debug_info` after PR #6197
- **Test**: Added 4 new tests covering each formerly-gated field

## Metadata
- **PR**: #6201
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +245/-31 in 2 files
- **Labels**: none

## Connections
