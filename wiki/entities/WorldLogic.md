---
title: "WorldLogic"
type: entity
tags: [module, game-logic, combat]
sources: [comprehensive-combat-cleanup-tests]
last_updated: 2026-04-08
---

World logic module containing apply_automatic_combat_cleanup() function that removes defeated enemies from combat when their HP reaches zero.

## Connections
- [[GameState]] — processes state for cleanup
- [[FirestoreService]] — chains after for cleanup pipeline
