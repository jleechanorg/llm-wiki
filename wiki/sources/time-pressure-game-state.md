---
title: "Time Pressure in GameState"
type: source
tags: [testing, game-state, time-management, deadline-tracking]
source_file: "raw/time-pressure-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for time pressure functionality in GameState. Tests verify tracking of time-sensitive events with deadlines, NPC agenda progression over time, deadline consequence triggers when deadlines pass, and warning generation at different urgency levels (high, critical, etc.).

## Key Claims
- **Event Tracking**: Time-sensitive events with deadlines are properly tracked in game_state.time_sensitive_events
- **NPC Agendas**: NPCs have agendas that progress over time with current_goal, progress_percentage, and next_milestone
- **Deadline Consequences**: Missing a deadline triggers consequences (e.g., "Merchant will be sold to slavers", "Half the village dies from plague")
- **Warning Generation**: Warnings are generated based on urgency_level (high, critical) and time remaining until deadline

## Key Quotes
> "rescue_merchant" event with deadline on day 25, hour 18 — urgency_level: high, consequences: "Merchant will be sold to slavers"

> Garrick (Bandit Leader) agenda with current_goal: "Sell captured merchant to slavers", progress_percentage: 30

## Connections
- [[GameState]] — the class being tested with time pressure structures
- [[TimeConsolidation]] — related time management in GameState

## Contradictions
- None identified
