---
title: "D&D 5E Ability Scores"
type: concept
tags: [dnd-5e, stats, mechanics, ability-scores]
sources: ["game-state-schema-json"]
last_updated: 2026-04-08
---

## Definition
The six core ability scores used in D&D 5E character creation and mechanics.

## The Six Scores
| Score | Abbreviation | Used For |
|-------|--------------|----------|
| Strength | STR | Melee attacks, damage, carrying capacity |
| Dexterity | DEX | Ranged attacks, AC, initiative |
| Constitution | CON | HP, concentration saves |
| Intelligence | INT | Wizard spellcasting, knowledge checks |
| Wisdom | WIS | Perception, cleric/druid spells |
| Charisma | CHA | Bard/warlock/sorcerer spells, social checks |

## Schema Details
- **Minimum**: 1 (default 10)
- **Unbounded**: Epic levels allow scores beyond 30
- **Validation**: Defensive integer handling for robustness

## Related Concepts
- [[ProficiencyBonus]] — Derived from level
- [[HealthStatus]] — HP based on CON modifier
