---
title: "Level-Up Mode (D&D 5e)"
type: source
tags: [dnd-5e, level-up, game-mechanics, modal-system, character-progression]
source_file: "raw/level-up-mode-dnd-5e.md"
sources: []
last_updated: 2026-04-08
---

## Summary
System for handling D&D 5e character level-up in a strict modal flow. The user remains locked in level-up mode until explicitly completing all required selections (HP, class features, ASI/feats, spellcasting updates), with the finish option always appearing as the last choice.

## Key Claims
- **Modal Lock Enforcement**: User cannot exit level-up mode without choosing explicit finish option; story does not advance until completion
- **Incremental State Updates**: Level-up processes checklist items in order, updating state after each decision
- **Mandatory Finish Option**: The "Finish Level-Up and Return to Game" choice must be last in `planning_block.choices`
- **HP Calculation**: Rolled HP (hit die + Con mod) OR fixed average HP + Con mod; exact math must be called out
- **Class Feature Enumeration**: All features gained at new level with usage limits, recharge cadence, and action economy impact

## Key Quotes
> "When `custom_campaign_state.level_up_in_progress == true`: The user remains in level-up mode until they explicitly choose to exit."

> "The finish option must be the final (last) choice in `planning_block.choices`."

## Connections
- [[LevelUpAgent]] — routes to this system via `custom_campaign_state.level_up_in_progress` flag
- [[GameStateClassDefinition]] — maintains campaign state including level and stats
- [[PlanningBlockPattern]] — structured choice presentation for pending decisions

## Contradictions
- None identified
