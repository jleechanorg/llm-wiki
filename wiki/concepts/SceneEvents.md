---
title: "Scene Events"
type: concept
tags: [event, scene, system]
sources: [debug-events-export-tests]
last_updated: 2026-04-08
---

## Description
Events that trigger specific scenes in the campaign, such as companion requests, story beats, or encounters.

## Types
- **companion_request** — Companion asks for help with personal quest
- Additional types available in the system

## Fields
- **type** — The kind of scene event
- **actor** — Who triggers the event
- **description** — What happens in the scene

## Example
```python
{
    "type": "companion_request",
    "actor": "Shadowheart",
    "description": "Asks for help with a personal quest",
}
```

## Connections
- [[LivingWorld]] — generates scene events
- [[CompanionSystem]] — companion request mechanics
- [[DebugEventsExport]] — exports scene events
- [[Shadowheart]] — example companion
