---
title: "Faction Minigame State Access Utilities"
type: source
tags: [python, faction-system, game-state, utilities, state-extraction]
source_file: "raw/faction-minigame-state-access-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Centralized utilities module providing a single source of truth for extracting faction_minigame dict from various game_state structures. Eliminates duplication across agents.py, gemini_provider.py, and LLM provider modules by handling all known game_state navigation paths with provider-agnostic extraction from prompt_contents.

## Key Claims
- **Canonical Location**: faction_minigame stored in custom_campaign_state dict (per world_logic.py lines 2940-2947)
- **Precedence Order**: custom_campaign_state checked BEFORE direct faction_minigame attribute
- **Multiple Structure Support**: Handles GameState objects, dicts, and data wrapper structures
- **Provider Agnostic**: Works with prompt_contents from any LLM provider

## Key Functions
- `get_faction_minigame_dict`: Extracts faction_minigame dict from any game_state structure, trying 6 known paths in precedence order

## Connections
- [[FactionArmyManagementSystem]] — uses these utilities for faction minigame state access
- [[DualModeCampaignSystem]] — integrates with faction minigame for D&D + Faction integration
