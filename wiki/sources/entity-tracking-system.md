---
title: "Entity Tracking System"
type: source
tags: [python, entity-tracking, narrative-generation, pydantic, game-state]
source_file: "raw/entity-tracking-system.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing entity tracking capabilities for narrative generation, ensuring characters, NPCs, and other entities are properly tracked and validated during story generation. Acts as a wrapper around Pydantic schemas, providing a stable API while delegating validation to the schemas module.

## Key Claims
- **Scene Manifest Creation**: Creates SceneManifest objects from game state with session and turn context
- **Entity Status Tracking**: Tracks entities as active, inactive, or mentioned using EntityStatus enum
- **Visibility Management**: Manages entity visibility states (visible, hidden, off-screen)
- **Pydantic Validation**: Uses schemas_pydantic for robust schema enforcement and data integrity
- **Wrapper Pattern**: Bridges core application to Pydantic-based entity schemas with stable API

## Key Exports
- SceneManifest: Container for expected entities with session/turn context
- EntityStatus: Enum for entity state tracking (active, inactive, mentioned)
- Visibility: Enum for visibility management (visible, hidden, off-screen)
- create_from_game_state(): Factory function to build manifests from game state
- VALIDATION_TYPE: Constant indicating Pydantic-based validation

## Connections
- [[Pydantic Schema Models for Entity Tracking]] — underlying schemas this module wraps
- [[Entity Preloader]] — provides entity instruction generation for AI prompts
- [[Character Creation & Level-Up Mode]] — entity tracking supports character lifecycle

## Contradictions
- None identified
