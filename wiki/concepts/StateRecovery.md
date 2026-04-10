---
title: "State Recovery"
type: concept
tags: [error-handling, state-management, game-engine]
sources: ["living-world-trigger-evaluation.md"]
last_updated: 2026-04-08
---

Mechanism to recover from corrupt or stale tracking where `last_turn` exceeds `current_turn`. Realigns to the most recent interval boundary by computing `current_turn - (current_turn % turn_interval)`, ensuring trigger cadence continues correctly.

Critical for maintaining living world progression when game state becomes inconsistent.
