---
title: "Warning Generation"
type: concept
tags: [game-mechanic, player-notification, urgency]
sources: ["time-pressure-game-state"]
last_updated: 2026-04-08
---

## Definition
Warning generation is the system that alerts players to approaching deadlines based on urgency level and time remaining until the deadline.

## Warning Properties
- **warnings_given**: Counter tracking how many warnings have been issued
- **urgency_level**: Determines frequency and intensity of warnings
- **time_pressure_warnings**: Dict in GameState storing active warnings

## Urgency-Based Timing
- **critical**: Immediate warnings, deadline may already be passed
- **high**: Warnings when deadline is approaching (e.g., within 4 days)

## Related Concepts
- [[TimeSensitiveEvents]] — events that generate warnings
- [[DeadlineConsequences]] — what happens if warnings are ignored
