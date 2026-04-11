---
title: "GameState Class Definition"
type: source
tags: [python, game-state, dnd-5e, xp-validation, session-management]
source_file: "raw/game-state-class-definition.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Defines the GameState class representing the complete state of a WorldArchitect.AI campaign. Integrates D&D 5E mechanics for deterministic game logic, XP/level validation using official XP thresholds, time monotonicity checks to prevent regression, and helper functions for XP→level calculations. The LLM focuses on narrative while code handles all mathematical operations.

## Key Claims
- **Complete Campaign State**: GameState class encapsulates all campaign data including world_data, player_character_data, combat_state, and narrative
- **D&D 5E Integration**: Uses official XP thresholds (0-355000 for levels 1-20) and proficiency bonuses by level for deterministic calculations
- **Time Monotonicity**: Prevents time regression in campaign chronology through validation checks
- **Schema Migration**: Supports legacy campaign migration with session ID seeding for Firestore compatibility
- **Separation of Concerns**: LLM handles narrative; code handles dice rolls, XP calculations, and validation

## Key Quotes
> "The LLM should focus on narrative while code handles all mathematical operations."

## Connections
- [[GameStateManagementProtocol]] — protocol for JSON response formatting and state updates
- [[GameStateExamples]] — session header format and response JSON schema
- [[RuntimeGeneratedPydanticModels]] — Pydantic model for serialization

## Contradictions
- None identified
