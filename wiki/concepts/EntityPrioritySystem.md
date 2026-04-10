---
title: "Entity Priority System"
type: concept
tags: [priority-classification, entity-tracking, game-ai]
sources: ["enhanced-explicit-entity-instructions-generator"]
last_updated: 2026-04-08
---

## Definition
A 3-tier classification system determining the urgency and forcefulness of AI instructions for entity inclusion in generated content.

## Priority Levels
| Priority | Level | Entity Types | Instruction Force |
|----------|-------|--------------|-------------------|
| 1 | Highest | player_character, npc_referenced, location_owner | "MUST be present" |
| 2 | Medium | story_critical, location_associated | "should be included" |
| 3 | Lowest | background | "may be acknowledged" |

## Application
The priority system sorts entity instructions before generating AI prompts, ensuring higher-priority entities receive more forceful language. This prevents lower-priority entities from crowding out critical characters in constrained token budgets.

## Relationship to Other Concepts
- Enables [[TokenBudgetAllocation]] by prioritizing entity instructions
- Works with [[EntityInstructionGeneration]] to apply appropriate force
- Supports [[CombatSystemProtocol]] by prioritizing combatants
