---
title: "State Transitions"
type: concept
tags: [state-machine, modal-agent]
sources: ["modal-state-lifecycle-tests"]
last_updated: 2026-04-08
---

## Summary
Pattern for managing state transitions in modal agents, ensuring proper lifecycle from activate through in_progress to complete/cancel states.

## Key Claims
- **Three-phase lifecycle**: activate → in_progress → complete/cancel
- **Proper exit**: finish choice sets complete flag
- **Cancellation**: User-cancelled actions clear in_progress flags
- **Stale flag removal**: Old flags removed, not preserved as False

## Connections
- [[Modal State Management]] — higher-level concept
- [[LevelUpAgent]] — implements transitions
- [[CharacterCreationAgent]] — implements transitions
