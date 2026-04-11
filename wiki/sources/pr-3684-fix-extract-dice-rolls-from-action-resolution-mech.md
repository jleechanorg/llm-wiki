---
title: "PR #3684: Fix: Extract dice_rolls from action_resolution.mechanics.rolls for Firestore"
type: source
tags: []
date: 2026-01-17
source_file: raw/prs-worldarchitect-ai/pr-3684.md
sources: []
last_updated: 2026-01-17
---

## Summary
- **Bug**: When LLM correctly places dice in `action_resolution.mechanics.rolls` (as instructed in `game_state_instruction.md:236`), the `dice_rolls` field remained empty `[]` in Firestore because `extract_structured_fields()` only read `dice_rolls` directly from the LLM response.
- **Fix**: After extracting `action_resolution`, now call `extract_dice_rolls_from_action_resolution()` to populate `dice_rolls` from `action_resolution.mechanics.rolls` (single source of truth).
- **Tests**: Added 3 r

## Metadata
- **PR**: #3684
- **Merged**: 2026-01-17
- **Author**: jleechan2015
- **Stats**: +345/-36 in 5 files
- **Labels**: none

## Connections
