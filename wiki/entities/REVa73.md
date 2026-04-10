---
title: "REV-a73"
type: entity
tags: [bug, regression, serialization]
sources: []
last_updated: 2026-04-08
---

## Description
Bug report describing data loss where last_living_world_turn and last_living_world_time fields were not preserved through GameState.to_model() → from_model() round-trip serialization.

## Status
Fixed — TDD tests added to prevent regression.

## Related Tests
- [[Living World Model Round Trip Tests]] — validates the fix
