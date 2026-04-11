---
title: "Game State JSON Schema"
type: source
tags: [json-schema, game-state, schema-definition, pydantic]
source_file: "raw/game-state-schema-json.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Canonical JSON Schema defining the complete game state structure for WorldArchitect.AI. Serves as the single source of truth for all game state validation and serialization, with Pydantic models generated dynamically at runtime to guarantee schema alignment. Defines core types for stats, health, entities, and character data.

## Key Claims
- **Schema Authority**: game_state.schema.json is the authoritative source for all game state structure
- **Type Safety**: Stats (STR/DEX/CON/INT/WIS/CHA) use defensive integer validation with minimum 1, unbounded for epic levels
- **Health Tracking**: Complete health system including current HP, max HP, temp HP, conditions, and death saves
- **Entity System**: Six entity types (pc, npc, creature, loc, item, faction, obj) with flexible status representation
- **Backward Compatibility**: Stats and EntityStatus allow additional properties for legacy/test data

## Key Quotes
> "$schema": "https://json-schema.org/draft/2020-12/schema" — Uses JSON Schema Draft 2020-12

> "EntityType": ["pc", "npc", "creature", "loc", "item", "faction", "obj"] — Core entity taxonomy

## Connections
- [[RuntimeGeneratedPydanticModels]] — Pydantic models dynamically generated from this schema
- [[GameStateClassDefinition]] — GameState class using this schema for validation
- [[GameStateExamples]] — Example instances conforming to this schema
- [[EntityTrackingSystem]] — Entity tracking built on this schema's types

## Contradictions
[]
