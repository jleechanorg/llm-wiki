---
title: "SceneManifest"
type: concept
tags: [data-structure, pydantic, game-state]
sources: [pydantic-validation-entity-tracking-tests]
last_updated: 2026-04-08
---

## Description
Pydantic model representing a scene's extracted entities from game state. Contains player characters, NPCs, and current location.

## Fields
- `player_characters` — list of validated player character objects
- `npcs` — list of validated NPC objects
- `current_location` — string representing current scene location

## Creation
Created via `entity_tracking.create_from_game_state()` which validates input game_state dict and returns typed SceneManifest.

## Related Concepts
- [[Pydantic]] — validation framework
- [[entity_tracking]] — module that creates manifests
- DefensiveNumericConverter — handles type coercion during creation
