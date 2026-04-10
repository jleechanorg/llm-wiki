---
title: "NPC"
type: concept
tags: [game-entity, character, schema, pydantic]
sources: []
last_updated: 2026-04-08
---

## Description
Non-Player Character. A game entity schema that represents characters controlled by the game system rather than players. In the WorldArchitect system, NPC objects include fields for display_name, gender, faction, role, health status, and current location.

## Key Fields
- **gender**: String field that now enforces consistency to prevent narrative generation bugs
- **display_name**: The visible name of the NPC
- **faction**: Which group/faction the NPC belongs to (e.g., "Jedi Order")
- **role**: The NPC's role (e.g., "Jedi Master")

## Related
- [[HealthStatus]] — tracks NPC hit points
- [[Pydantic]] — validation library used for schema enforcement
- [[NarrativeGeneration]] — system that must read gender field to produce consistent pronouns
