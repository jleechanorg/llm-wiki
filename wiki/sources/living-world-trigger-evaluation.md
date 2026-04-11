---
title: "Living World Trigger Evaluation"
type: source
tags: [living-world, game-mechanics, trigger-evaluation, state-recovery]
source_file: "raw/living-world-trigger-evaluation.md"
sources: ["living-world-advancement-protocol.md"]
last_updated: 2026-04-08
---

## Summary
Python function implementing living world trigger logic that evaluates both turn-based and time-based conditions for advancing the living world. Includes state recovery logic to handle corrupt/stale tracking that puts last_turn ahead of current_turn.

## Key Claims
- **Turn-Based Triggers**: Uses modulo arithmetic (`current_turn % turn_interval == 0`) for consistent scheduling at turns 3, 6, 9, etc.
- **Time-Based Triggers**: Evaluates hours elapsed between last_time and current_time via `world_time.calculate_hours_elapsed`
- **State Recovery**: Realigns stale tracking by finding most recent interval boundary when last_turn > current_turn
- **Turn Deduplication**: Prevents multiple triggers per turn by checking `current_turn > normalized_last_turn`

## Key Functions
- `evaluate_living_world_trigger()`: Main function returning `(should_trigger, reason_string, hours_elapsed)`
- `calculate_hours_elapsed()`: Referenced from `world_time` module for time-based evaluation

## Connections
- [[LivingWorldAdvancementProtocol]] — implements trigger evaluation for the protocol
- [[MvpSite]] — the project containing this function
- [[Constants]] — provides `LIVING_WORLD_TURN_INTERVAL` and `LIVING_WORLD_TIME_INTERVAL`
- [[WorldTime]] — provides time calculation utilities

## Contradictions
[]
