---
title: "Living World Updates"
type: concept
tags: [frontend, game-state, debug-information, world-events]
sources: ["frontend-structured-fields-tests-simple"]
last_updated: 2026-04-08
---

## Definition
Diagnostic display of background game system state, visible only in debug mode. Includes world events, faction updates, time events, rumors, scene events, and complications.

## Components
- **world_events**: Background narrative events with actor, action, event_type, status
- **faction_updates**: Current objectives for each faction
- **time_events**: Time-based triggers and events
- **rumors**: Rumor array for player discovery
- **scene_event**: Active scene event with type, description, actor
- **complications**: Challenge triggers with boolean/string triggered flag

## Rendering Rules
- Only displays when debugMode=true
- Each component type has its own conditional check
- Complications.triggered accepts both boolean true and string "true"

## Related Concepts
- [[Debug Mode]]
- [[Structured Fields Rendering]]
