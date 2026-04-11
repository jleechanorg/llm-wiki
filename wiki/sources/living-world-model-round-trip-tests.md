---
title: "TDD Test for REV-a73: Living World Data Loss in to_model/from_model Round-trip"
type: source
tags: [python, testing, regression-fix, serialization, game-state]
source_file: "raw/test_living_world_model_round_trip.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite verifying that `last_living_world_turn` and `last_living_world_time` fields are preserved through GameState.to_model() → from_model() round-trip. Regression test for REV-a73.

## Key Claims
- **last_living_world_turn preserved**: Integer turn counter survives serialization round-trip
- **last_living_world_time preserved**: Complete time dict (day, hour, minute, etc.) survives round-trip
- **to_dict() includes fields**: Both fields are included in the dictionary representation

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_living_world_fields_preserved_in_model_round_trip | Set fields, serialize, deserialize | Values match original |
| test_living_world_fields_in_to_dict | Check to_dict() output | Fields present in output |

## Connections
- [[GameState]] — class being tested
- [[REVa73]] — the bug fix this test validates
- [[ModelRoundTrip]] — serialization pattern under test
