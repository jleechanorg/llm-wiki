---
title: "Entity Instruction Generation"
type: concept
tags: [ai-prompting, entity-tracking, game-mechanics]
sources: ["enhanced-explicit-entity-instructions-generator"]
last_updated: 2026-04-08
---

## Definition
A prompt engineering technique that generates explicit instructions for AI models requiring specific entities to be present in generated content. Used in game AI to ensure NPCs, locations, and story elements appear when referenced or required.

## Key Principles
- **Mandatory Requirements**: Entities marked as required MUST appear in AI output
- **Template-Based**: Pre-written instruction patterns for common entity types
- **Context-Aware**: Instructions adapt based on location and story context
- **Priority Sorting**: Higher-priority entities generate more forceful instructions

## Templates
| Entity Type | Mandatory Template | Use Case |
|-------------|-------------------|----------|
| player_character | "{entity} MUST be present and actively involved" | Ensure PC participation |
| npc_referenced | "{entity} has been referenced and MUST respond" | Honor player mentions |
| location_npc | "{entity} belongs in this location" | Maintain scene realism |
| story_critical | "{entity} is critical to story development" | Advance plot |
| background | "{entity} should be acknowledged as present" | Atmosphere |

## Relationship to Other Concepts
- Part of [[PromptEngineering]] methodology
- Integrates with [[EntityTracking]] for game state awareness
- Supports [[GameNarrativeGeneration]] by ensuring character presence
