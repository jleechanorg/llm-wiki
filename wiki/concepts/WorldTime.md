---
title: "World Time"
type: concept
tags: [temporal, world-building, game-mechanics]
sources: [world-time-module]
last_updated: 2026-04-08
---

## Definition
The temporal system used in World of Assiah campaign tracking. Represented as a dict with year, month, day, hour, minute, second, and microsecond fields. The LLM advances world time during narrative pauses in [[Think Mode]].

## Key Properties
- **Multi-calendar support**: Handles Forgotten Realms, Grayhawk, and Gregorian month names
- **UTC normalization**: Timestamps with timezone offsets converted to UTC for consistent comparison
- **Partial data handling**: Allows incomplete world_time (e.g., hour/minute only) without triggering temporal violations

## Usage
Used by [[World Time Module]] for parsing LLM responses and maintaining temporal consistency across game sessions.
