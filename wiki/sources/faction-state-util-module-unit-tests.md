---
title: "Faction State Util Module Unit Tests"
type: source
tags: [python, testing, faction-minigame, state-access, utility-module]
source_file: "raw/test_faction_state_util.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the `faction_state_util` module's `get_faction_minigame_dict()` function, which extracts faction_minigame data from various game_state structures. Tests cover nested attribute access, dict wrappers, data dictionary patterns, and edge cases.

## Key Claims
- **Function**: `get_faction_minigame_dict()` extracts faction_minigame from multiple possible locations
- **Access Patterns**: Supports direct attribute, nested custom_campaign_state, and data wrapper paths
- **Edge Cases**: Handles None, missing keys, non-dict values, and precedence rules
- **Precedence**: custom_campaign_state path takes precedence over direct faction_minigame when both exist

## Key Quotes
> "Extract from game_state.faction_minigame attribute"

> "Extract from game_state.data dict (not object) with nested structure"

## Connections
- [[FactionMinigame]] — the game feature this utility accesses
- [[FactionSettingsPersistence]] — settings that depend on correct state access

## Contradictions
- None identified
