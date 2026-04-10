---
title: "Legacy State Migration"
type: concept
tags: [data-migration, game-state, backwards-compatibility]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Definition
Process of cleaning up deprecated fields from game state data structures while maintaining backwards compatibility with older campaign saves.

## Implementation
`_cleanup_legacy_state(state_dict)` removes deprecated fields and returns cleanup statistics.

## Related Concepts
- [[GameState]]
- [[DataMigration]]
