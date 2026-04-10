---
title: "NarrativeResponse"
type: entity
tags: [class, python, schema]
sources: [state-update-integration-tests]
last_updated: 2026-04-08
---

## Description
Pydantic schema for structured LLM responses containing narrative, entities, location, and state_updates.

## Key Fields
- `narrative`: The story text
- `entities_mentioned`: List of entities in the response
- `location_confirmed`: Confirmed location
- `state_updates`: Dict containing player_character_data and npc_data

## Connections
- [[LLMResponse]] — wraps this schema
- [[StateUpdateIntegrationTests]] — tests this schema's usage
