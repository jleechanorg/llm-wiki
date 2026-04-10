---
title: "TimeOfDay"
type: concept
tags: [time, game-state]
sources: []
last_updated: 2026-04-08
---

Time of day description derived from hour value. Canonical mappings: 0-4=deep night, 5-6=dawn, 7-11=morning, 12-13=midday, 14-17=afternoon, 18-19=evening, 20-23=night. Stored in world_time.time_of_day field.

## Connections
- [[WorldTime]] — stored in unified time object
- [[GameState]] — calculates from hour
