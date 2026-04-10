---
title: "Turn-Based Trigger"
type: concept
tags: [trigger-system, game-mechanics, living-world]
sources: ["living-world-trigger-evaluation.md"]
last_updated: 2026-04-08
---

Trigger mechanism that fires at regular turn intervals using modulo arithmetic (`current_turn % turn_interval == 0`). Ensures consistent scheduling at fixed turn boundaries (e.g., turns 3, 6, 9) independent of time-based triggers.

Used by [[LivingWorldAdvancementProtocol]] to generate background events on a predictable cadence.
