---
title: "Hit Dice Tracking"
type: concept
tags: [character-progression, game-state, validation]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
Tracking Hit Dice (HD) as spent/total with proper HP scaling on level-up, ensuring character progression is correctly reflected in stats.

## Problem
Level 5 Fighter still has 20/20 HP and HD 1/1 (should be 5 total HD) — character progression not reflected in stats.

## Solution
Track HD as two values:
- **Spent HD**: Actual dice available for healing
- **Total HD**: Derived from character level
On level up:
- Add new HD (max die type for class)
- Increase max HP by full die roll + CON modifier

## Related Concepts
- [[LevelProgression]] — overall level advancement
- [[CharacterProgression]] — RPG character growth
