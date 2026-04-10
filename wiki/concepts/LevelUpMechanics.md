---
title: "Level-Up Mechanics"
type: concept
tags: [character-progression, dnd-5e, game-mechanics]
sources: [level-up-mode-dnd-5e]
last_updated: 2026-04-08
---

## Description
System for advancing a D&D 5e character from one level to the next with mandatory modal interaction. The user must complete all required selections before returning to active gameplay.

## Process Steps
1. Confirm level transition (from_level → to_level)
2. Calculate HP gain (rolled or fixed method)
3. Recalculate proficiency bonus
4. Enumerate new class features
5. Update spellcasting (for casters)
6. Handle ASI or Feat decision
7. Recompute derived stats
8. Validate legal choices

## Modal Constraints
- User cannot exit until explicit finish choice selected
- Finish option must be last in planning_block.choices
- World events do not advance while level-up is active

## Related Concepts
- [[HitPoints]] — character health
- [[ProficiencyBonus]] — level-based bonus
- [[ClassFeatures]] — abilities gained from class levels
- [[Spellcasting]] — magic progression
- [[AbilityScoreImprovement]] — stat increases
- [[Feat]] — optional power gains
