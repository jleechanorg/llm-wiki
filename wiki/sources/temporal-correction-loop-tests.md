---
title: "Temporal Correction Loop Tests"
type: source
tags: [testing, python, temporal, game-state, firestore]
source_file: "raw/temporal-correction-loop-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating temporal correction loop behavior to ensure player input preservation. Tests verify that backward time jumps are handled correctly and that incomplete world_time data doesn't trigger false temporal violation flags.

## Key Claims
- **Player Input Preservation**: Original player input must always be preserved and saved to Firestore during temporal corrections
- **Incomplete Time Not Violation**: Missing year/month/day fields should NOT trigger temporal violations (malformed data, not backward time)
- **Backward Time Detection**: Complete backward time data SHOULD still be flagged as violations
- **Temporal Corrections Disabled**: MAX_TEMPORAL_CORRECTION_ATTEMPTS=0 to reduce multiple LLM calls

## Key Quotes
> "Incomplete world_time should NOT trigger temporal violation. Missing year/month/day is malformed data, not backward time travel."

## Connections
- [[GameState]] — stores world_time across turns
- [[Firestore]] — persists player input and game state
- [[TemporalViolation]] — concept for detecting backward time travel

## Contradictions
- None detected
