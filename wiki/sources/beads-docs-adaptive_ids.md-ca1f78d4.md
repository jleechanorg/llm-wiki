---
title: "Adaptive ID Length"
type: source
tags: [beads, feature, id-system, hash, collision-prevention, configuration]
sources: []
source_file: docs/adaptive_id_length.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Beads uses adaptive hash ID lengths that automatically scale based on database size, optimizing for readability in small databases while preventing collisions as databases grow. The system uses Birthday Paradox math to calculate collision probabilities and defaults to 25% max collision threshold.

## Key Claims

- **Adaptive Scaling**: ID length automatically adjusts based on database size — 4 chars (0-500), 5 chars (501-1500), 6 chars (1500+)
- **Birthday Paradox Math**: Collision probability calculated via `P ≈ 1 - e^(-n²/2N)` where N = 36^length
- **Collision Resolution**: Algorithm tries base length, then +1, then +2 with 10 nonces per length (30 total attempts)
- **Configurable**: Users can set max_collision_prob, min_hash_length, and max_hash_length
- **Performance**: ~10ns for collision calculation, ~300ns for ID generation, ~100μs for database query

## Key Quotes

> "Users who actively archive old issues can keep their IDs shorter over time"

> "The 25% threshold works well for most use cases"

## Connections

- [[Beads Changelog v0.49.5-v0.49.6]] — Beads issue tracker this feature belongs to
- [[Beads Performance Benchmarks]] — related performance metrics for the system

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| max_collision_prob | 0.25 | Maximum acceptable collision probability |
| min_hash_length | 4 | Minimum ID character length |
| max_hash_length | 8 | Maximum ID character length |

## Implementation Locations

- Algorithm: `internal/storage/sqlite/adaptive_length.go`
- ID generation: `internal/storage/sqlite/sqlite.go`
- Tests: `internal/storage/sqlite/adaptive_length_test.go`
- E2E tests: `internal/storage/sqlite/adaptive_e2e_test.go`