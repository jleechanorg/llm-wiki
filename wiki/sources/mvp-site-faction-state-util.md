---
title: "mvp_site faction_state_util"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/faction_state_util.py
---

## Summary
Centralized utilities for faction minigame state access. Provides single source of truth for extracting faction_minigame dict from various game_state structures, checking if faction is enabled, and handling all known game_state navigation paths.

## Key Claims
- get_faction_minigame_dict() extracts faction_minigame dict from any game_state structure (handles 6+ paths)
- is_faction_enabled() checks boolean validation for faction minigame activation
- get_faction_state() provides provider-agnostic extraction from prompt_contents (LLM request format)
- Detects faction minigame enable actions in user_action strings

## Connections
- [[FactionMinigame]] — faction state extraction utilities
- [[GameState]] — extracts faction data from game_state structures
- [[DiceMechanics]] — DICE_ROLL_TOOLS import