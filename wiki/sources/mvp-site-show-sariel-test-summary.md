---
title: "Show Sariel Test Summary"
type: source
tags: [testing, sariel, validation, summary]
sources: [mvp-site-show-sariel-test-summary]
last_updated: 2025-01-15
---

## Summary

Display utility that shows what the Sariel campaign integration test validates. Reports field counts and test scenarios for entity tracking validation.

## Key Claims

- **Field validation**: Shows 7 top-level game state fields validated
- **Player character**: Up to 20+ fields per character
- **NPC tracking**: Up to 8+ fields per NPC per interaction
- **Entity tracking**: 7 fields per interaction for desync measurement
- **10 interactions**: ~280+ total fields validated across replay

## Game State Top-Level Fields (7)

- game_state_version
- player_character_data
- world_data
- npc_data
- custom_campaign_state
- combat_state
- last_state_update_timestamp

## Test Scenarios

1. **Initial campaign setup** - validates proper initialization
2. **The 'Cassian Problem'** - tests entity reference handling
3. **Location changes** - validates entity presence based on context
4. **NPC interactions** - ensures all mentioned NPCs are tracked

## Connections

- [[mvp-site-run-sariel-replays]] - Replay runner
- [[mvp-site-sariel-campaign]] - Sariel campaign source
- [[mvp-site-structured-fields-fixtures]] - Structured field fixtures
