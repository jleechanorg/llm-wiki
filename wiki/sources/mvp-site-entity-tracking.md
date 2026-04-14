---
title: "mvp_site — Entity Tracking System"
type: source
tags: [worldarchitect-ai, entities, Pydantic, scene-manifest, validation]
date: 2026-04-14
source_file: raw/mvp_site_all/entity_tracking.py
---

## Summary

Provides entity tracking for narrative generation, ensuring characters, NPCs, and other entities are properly tracked and validated during story generation. Uses Pydantic schemas (`entities_pydantic.py`) for robust schema enforcement. Bridge between core application and Pydantic entity schemas.

## Key Claims

### Entity Validation Type
`VALIDATION_TYPE = "Pydantic"` — all entity validation delegated to Pydantic models

### Core Data Structures
- `SceneManifest` — scene-level entity collection with turn/session context
- `EntityStatus` — enum: active, inactive, mentioned
- `Visibility` — enum: visible, hidden, off-screen

### Scene Manifest Creation
```python
create_from_game_state(game_state, session_number, turn_number)
```
Creates a `SceneManifest` from current game state, tagging entities with status and visibility.

### Architecture
- Wrapper around Pydantic schemas (`entities_pydantic.py`)
- Game state integration for entity discovery
- Scene-based tracking with turn/session context
- Validated by Pydantic at boundary

## Connections

- [[EntitySchema]] — Pydantic schema layer
- [[mvp-site-game-state]] — game state that entity tracking reads from
- [[mvp-site-entity-instructions]] — entity instruction generation
