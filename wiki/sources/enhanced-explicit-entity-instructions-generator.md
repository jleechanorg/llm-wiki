---
title: "Enhanced Explicit Entity Instructions Generator"
type: source
tags: [python, ai-prompting, entity-tracking, game-state, instruction-generation]
source_file: "raw/enhanced-explicit-entity-instructions.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module generating explicit AI instructions ensuring entity presence in game scenes. Implements a priority-based system with templates for different entity types (player characters, NPCs, location-associated entities, story-critical entities). Uses dataclasses for structured instruction representation with priority levels 1-3.

## Key Claims
- **Template-Based Generation**: Pre-built instruction templates for 5 entity categories with specific contexts
- **Priority System**: 3-tier priority (1=highest) with player characters and referenced NPCs at top
- **Multi-Input Processing**: Handles entities list, player references, location context, and story context
- **Categorized Instructions**: Distinguishes mandatory, conditional, and background entity presence requirements
- **Dataclass Structure**: EntityInstruction dataclass for type-safe instruction representation

## Key Quotes
> "The player character {entity} MUST be present and actively involved in this scene. Include their actions, thoughts, or dialogue." — mandatory template for player characters

> "{entity} has been directly referenced by the player and MUST appear or respond in this scene." — mandatory template for NPC references

## Connections
- [[EntityTracking]] — SceneManifest import for game state integration
- [[PromptEngineering]] — AI prompt generation methodology
- [[EntityPrioritySystem]] — 3-tier priority classification for entity inclusion

## Contradictions
- None identified
