---
title: "Shadow"
type: entity
tags: [player-character, npc, game-state]
sources: [think-mode-e2e-tests]
last_updated: 2026-04-08
---

## Description

Shadow is a player character in the WorldArchitect AI RPG system. Mentioned in THINK MODE end-to-end tests as a Lvl 3 Rogue with HP 22/28, XP 2500/6000, and 75gp. The character is tracked through entity validation in think mode responses to preserve character identity across game sessions.

## Attributes

- **Class**: Rogue (Level 3)
- **HP**: 22/28
- **XP**: 2500/6000
- **Gold**: 75gp
- **Intelligence**: 14

## Related Entities

- [[DungeonEntrance]] — location mentioned in test scenario
- [[Mirtul]] — month in the game's calendar system

## Related Concepts

- [[ThinkMode]] — game mode where this character was referenced
- [[SessionHeader]] — session state containing character stats
