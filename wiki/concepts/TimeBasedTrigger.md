---
title: "Time-Based Trigger"
type: concept
tags: [trigger-system, game-mechanics, time-tracking]
sources: ["living-world-trigger-evaluation.md"]
last_updated: 2026-04-08
---

Trigger mechanism that fires when elapsed in-game time exceeds a threshold. Uses `world_time.calculate_hours_elapsed` to compute hours between last_time and current_time dictionaries, triggering when hours >= `LIVING_WORLD_TIME_INTERVAL`.

Complements turn-based triggers to ensure world advances even if players spend many real-time hours in a single scene.
