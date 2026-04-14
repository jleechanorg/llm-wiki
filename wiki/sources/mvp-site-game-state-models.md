---
title: "mvp_site game_state_models"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/game_state_models.py
---

## Summary
Dynamically generates Pydantic models from the canonical JSON Schema (game_state.schema.json) at import time. Eliminates the divergence bugs that occurred with static Pydantic model auto-generation by making the schema the single source of truth. Uses extra='allow' to pass through all fields without rejection.

## Key Claims
- Uses the JSON Schema as the single source of truth — the Pydantic model is generated dynamically
- Real validation is performed by validate_game_state() in validation.py via jsonschema, not by this Pydantic model
- Exists solely for to_model()/from_model() round-trip support, ensuring data fidelity during serialization

## Connections
- [[GameState]] — generated model class that wraps the full game state
- [[Serialization]] — provides model serialization support for the game state