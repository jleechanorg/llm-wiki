---
title: "Level-Up Mechanics"
type: concept
tags: [character-progression, dnd-5e, game-mechanics]
sources: [level-up-mode-dnd-5e, level-up-dnd5e-research, level-up-second-opinion-analysis]
last_updated: 2026-04-14
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

## ASI Levels (D&D 5e class-specific)
- All classes: 4, 8, 12, 16, 19
- Fighter extra: **level 6** (not level 4)
- Rogue extra: **level 10** (not level 8)
- See [[LevelUpCodeArchitecture]] v3 for implementation
- **Multiclass rule**: when gaining a level in any class, check **total character level** (sum of all class levels) against each class's ASI schedule independently. If two classes have an ASI at the same total level, player receives ONE ASI, not two.

## Critical Guards
- **Zero/negative XP guard**: guard `xp_gained >= 0`; negative = no-op + warning log. Add to `game_state.py`.
- **Level cap 20**: clamp `resolved_target_level <= 20`; return `max_level` flag when hit.
- **Overflow XP retained**: e.g., 2,900 + 400 = 3,300 → still level 3, with 400 XP toward level 4. Never discard overflow XP.

## Related Concepts
- [[HitPoints]] — character health
- [[ProficiencyBonus]] — level-based bonus
- [[ClassFeatures]] — abilities gained from class levels
- [[Spellcasting]] — magic progression
- [[AbilityScoreImprovement]] — stat increases
- [[Feat]] — optional power gains
- [[LevelUpCodeArchitecture]] — v3: class-specific ASI levels enforced in rewards_engine._is_asi_level()
