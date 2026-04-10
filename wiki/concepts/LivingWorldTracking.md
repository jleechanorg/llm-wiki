---
title: "Living World Tracking"
type: concept
tags: [game-mechanics, world-state, time-tracking]
sources: []
last_updated: 2026-04-08
---

## Description
Feature that tracks the world's state across turns, including the turn number and time information (day, hour, minute, season, etc.). Essential for maintaining temporal consistency in an open-world game.

## Key Fields
- `last_living_world_turn` — integer counter of world turns
- `last_living_world_time` — dict with day, hour, minute, second, microsecond, time_of_day, season

## Related Bug
- [[REVa73]] — data loss bug where these fields were lost in serialization
