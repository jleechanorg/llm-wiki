---
title: "Structured Fields Fixtures"
type: source
tags: [testing, fixtures, game-state, structured-response]
sources: [mvp-site-structured-fields-fixtures]
last_updated: 2025-01-15
---

## Summary

Structured field fixtures for UI testing providing proper JSON responses with all 10 required fields from game_state_instruction.md. Used for validating LLM response structure.

## Key Claims

- **10-field structure**: All responses include session_header, resources, narrative, planning_block, dice_rolls, god_mode_response, entities_mentioned, location_confirmed, state_updates, debug_info
- **Game state sync**: state_updates contains NPCs, combat, world_data, custom_campaign_state
- **UI validation**: Responses match expected screenshots for campaign creation flow
- **Combat tracking**: Full combat state with HP, position, status per NPC

## Fixture Types

| Fixture | Purpose |
|---------|---------|
| INITIAL_CAMPAIGN_RESPONSE | Character creation phase response |
| FULL_STRUCTURED_RESPONSE | Complete combat encounter with all 10 fields |
| GOD_MODE_RESPONSE | DM information query response |
| MINIMAL_STRUCTURED_RESPONSE | Minimal response with empty state updates |

## Required Response Fields

1. session_header - Timestamp, location, character status
2. resources - HD, Second Wind, Action Surge, Potions
3. narrative - In-character DM narration
4. planning_block - thinking, context, choices
5. dice_rolls - Attack and save rolls with results
6. god_mode_response - DM-only information
7. entities_mentioned - List of all entities referenced
8. location_confirmed - Current location string
9. state_updates - NPC states, combat state, world data
10. debug_info - dm_notes and state_rationale

## Connections

- [[mvp-site-data-fixtures]] - Sample data for testing
- [[mvp-site-game-state-instruction]] - Game state instruction source
