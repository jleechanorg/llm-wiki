---
title: "Living World End-to-End Integration Tests"
type: source
tags: [python, testing, e2e, living-world, game-state]
source_file: "raw/test_living_world_e2e.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test suite validating Living World system functionality through the full application stack. Tests player_turn counter behavior, world_events extraction with turn_generated annotation, and backward compatibility when player_turn is absent.

## Key Claims
- **player_turn increments on non-GOD actions**: The player_turn counter stored in game_state increments on every non-GOD mode action
- **player_turn does NOT increment on GOD mode**: GOD mode actions intentionally skip player_turn increment to preserve world state consistency
- **world_events extraction with turn_generated**: World events are properly extracted and annotated with turn_generated metadata
- **Backward compatibility**: When player_turn is not present in state, it is computed from context rather than causing errors

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_player_turn_increments_on_non_god_action | Non-GOD mode action executed | player_turn increments by 1 |
| test_player_turn_not_incremented_on_god_action | GOD mode action executed | player_turn remains unchanged |
| test_world_events_extracted_with_turn_metadata | World event generated | Event includes turn_generated field |
| test_backward_compatibility_no_player_turn | Legacy state without player_turn | Computed from context |

## Connections
- [[GameState]] — validated through to_model/from_model round-trip
- [[Living World]] — core feature under test
- [[End2EndBaseTestCase]] — test infrastructure base class
