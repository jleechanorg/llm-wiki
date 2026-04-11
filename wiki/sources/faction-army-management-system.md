---
title: "Faction & Army Management System"
type: source
tags: [python, faction-system, army-management, game-state, minigame, mass-combat]
source_file: "raw/faction-army-management-system.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive faction and army management system for D&D campaigns with mandatory suggestion protocol, mass combat mechanics, and faction power calculation tools. Handles army recruitment, upkeep, strategic combat, and faction ranking with player-driven enablement.

## Key Claims
- **Faction Minigame Suggestion Protocol**: Mandatory checklist for recommending faction system based on army strength thresholds (100+, 500+)
- **Army Strength Categorization**: Forces categorized into soldiers/spies/elites before tool calls for accurate power calculation
- **Mass Combat System**: Initiative→Ranged→Charge→Melee→Morale Check per round with unit blocks (10 soldiers)
- **Upkeep Costs**: Infantry=10gp/day, Cavalry=25-40gp/day, War Mages=100gp/day per block
- **Planning Block Integration**: Enable choice via planning_block with exact key "enable_faction_minigame"
- **Entity Tracking Requirement**: Player name must appear in faction status narrative

## Key Components
- `faction_calculate_power` - Calculates faction power from categorized forces
- `faction_calculate_ranking` - Ranks faction based on power value
- Suggestion protocol with strong_suggestion_given and suggestion_given flags
- State updates for faction_minigame configuration

## Commands
- army status, recruit, disband, pay troops, fortify, forced march, battle plan

## Contradictions
- None identified in current wiki
