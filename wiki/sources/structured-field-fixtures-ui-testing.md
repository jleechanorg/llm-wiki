---
title: "Structured Field Fixtures for UI Testing"
type: source
tags: [javascript, testing, fixtures, ui-testing, game-state, json]
source_file: "raw/structured-field-fixtures-ui-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript module providing structured field fixtures for UI testing, matching the complete 10-field JSON response schema defined in game_state_instruction.md. Includes INITIAL_CAMPAIGN_RESPONSE for character creation and FULL_STRUCTURED_RESPONSE for in-game state.

## Key Claims
- **10-Field Schema Compliance**: Fixtures include all required game_state fields: session_header, resources, narrative, planning_block, dice_rolls, god_mode_response, entities_mentioned, location_confirmed, state_updates, debug_info
- **Character Creation Fixture**: INITIAL_CAMPAIGN_RESPONSE provides campaign setup response for testing the character creation wizard UI
- **In-Game State Fixture**: FULL_STRUCTURED_RESPONSE provides complete battle/encounter response for testing narrative display, resource tracking, and state management

## Key Fields
| Field | Type | Description |
|-------|------|-------------|
| session_header | string | Timestamp, location, status line |
| resources | string | HD, Second Wind, Action Surge, etc. |
| narrative | string | Main story/content text |
| planning_block | object | Thinking context, choices |
| dice_rolls | array | Any dice rolls made |
| god_mode_response | string | GM-only content |
| entities_mentioned | array | NPCs/items referenced |
| location_confirmed | string | Current location |
| state_updates | object | world_data + custom_campaign_state |
| debug_info | object | dm_notes, state_rationale |

## Connections
- [[game-state-instruction]] — defines the 10-field schema these fixtures implement
- [[streaming-client-worldarchitect]] — uses these fixtures for SSE response parsing
- [[session-header-utilities]] — formats the session_header field

## Contradictions
- None identified
