---
title: "EntitiesPydantic"
type: entity
tags: [pydantic, schema, entities, mvp-site]
sources: ["pydantic-entity-integration-tests"]
last_updated: 2026-04-08
---

Pydantic schema module in `mvp_site.schemas.entities_pydantic` defining entity models for the game system. Contains NPC, PlayerCharacter, HealthStatus, and Stats classes with integrated validation from entities_simple.py and game_state_instruction.md.

## Key Models
- **NPC**: Non-player character with mandatory gender, optional age, required health and location
- **PlayerCharacter**: Player-controlled entity with optional gender
- **HealthStatus**: Embedded model for HP tracking (hp, hp_max)
- **Stats**: Character statistics model

## Validation Features
- Gender required for NPCs (narrative consistency)
- Gender optional for PlayerCharacters
- Fantasy age ranges (0-50,000 years)
- 16 MBTI personality type validations
