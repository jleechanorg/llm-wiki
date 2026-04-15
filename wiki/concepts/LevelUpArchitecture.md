---
title: "Level Up Architecture"
type: concept
tags: [level-up, architecture, rewards, state-machine, worldai]
last_updated: 2026-04-14
---

## Summary

Level Up is a state-machine-based progression system where characters transition between states (e.g., Active, LevelUpPending, LevelUpAcknowledged) based on XP thresholds and UI interaction events.

## State Diagram

```
[Active] --(xp_threshold)--> [LevelUpPending]
[LevelUpPending] --(user_acknowledges)--> [LevelUpAcknowledged]
[LevelUpAcknowledged] --(server_confirms)--> [Active]
[LevelUpPending] --(stale_timer)--> [StaleLevelUp]
[StaleLevelUp] --(user_returns)--> [LevelUpPending]
```

## Core Components

### RewardsEngine
Computes XP deltas and determines when level-up thresholds are crossed.

### LevelUpDetection
Watches for `has_level_up_signal` in LLM responses or database state changes.

### LevelUpUI
Modal that presents choices to the player on level-up. Blocks until player selects.

### LevelUpOrchestrator
Coordinates between RewardsEngine, LevelUpDetection, and LevelUpUI.

## Key Design Decisions

**Single Responsibility**: Each component has one job:
- `RewardsEngine` — pure XP math
- `LevelUpDetection` — signal detection
- `LevelUpUI` — modal presentation/interaction

**Passthrough Normalization**: The streaming path must normalize rewards boxes before persisting — see [[StreamingPassthroughNormalization]].

## Connections
- [[LevelUpBug]] — Known bugs and fixes
- [[LevelUpStateManagement]] — State management patterns
- [[LevelUpPolling]] — Polling vs. push-based detection
- [[StreamingPassthroughNormalization]] — Normalization in streaming path
