---
title: "GameState None Semantics Preservation Tests"
type: source
tags: [python, testing, serialization, game-state, None-semantics, pydantic]
source_file: "raw/test_game_state_none_semantics.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating that None values are preserved through GameState.to_model() and GameState.from_model() round-trip serialization. Critical for fields like rewards_pending where None (no rewards structure) has different semantics than {} (empty rewards structure).

## Key Claims
- **None vs {} semantics**: None means "no rewards structure exists" vs {} means "rewards structure exists but is empty"
- **Preservation across serialization**: model_dump(mode='python') preserves None values that would otherwise convert to defaults
- **Multiple field coverage**: Tests cover rewards_pending, last_living_world_time, user_settings, encounter_state, planning_block, social_hp_challenge, action_resolution
- **Round-trip integrity**: Values serialized via to_model() and deserialized via from_model() maintain original None or {} state

## Key Quotes
> "GameState.from_model() uses model_dump(mode='python') to preserve None values"

## Connections
- Related to [[GameStateModel]] Pydantic schema
- Enables [[NarrativeResponse]] structured field handling

## Contradictions
- None documented
