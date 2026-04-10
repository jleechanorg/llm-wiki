---
title: "D&D 5E Mechanics"
type: concept
tags: [dnd-5e, game-mechanics, rpg, rules]
sources: []
last_updated: 2026-04-08
---

## Description
The D&D 5E rules system integrated into WorldArchitect.AI for deterministic game logic. Includes XP thresholds (0-355000 for levels 1-20), proficiency bonuses by level (2 at levels 1-4, increasing to 6 at levels 17-20), challenge rating XP values (XP_BY_CR table), and mechanical calculations that code executes while the LLM handles narrative.

## Key Components
- **XP Thresholds**: Cumulative XP requirements per level
- **Proficiency Bonus**: +2 to +6 based on character level
- **Challenge Rating XP**: XP rewards by creature CR (0-30)
- **Time Monotonicity**: Prevention of time regression in campaigns

## Connections
- [[GameStateClassDefinition]] — implements D&D 5E mechanics
- [[DiceMechanicsToolRequestsProtocol]] — mandatory dice execution
- [[DNDSRD5eSystemAuthority]] — mechanical rules reference
