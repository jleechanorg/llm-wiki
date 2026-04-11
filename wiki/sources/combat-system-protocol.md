---
title: "Combat System Protocol"
type: source
tags: [combat, dnd-5e, game-mechanics, initiative, reaction-protocol]
source_file: "raw/combat-system-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Protocol defining the combat encounter workflow for D&D 5e gameplay, covering initiative order enforcement, turn processing, reaction windows, and post-combat resolution including XP awarding. Mandatory rules require dice rolls for all attacks/saves, no dice in narrative, and strict turn ordering.

## Key Claims
- **Initiative Order**: All combatants take turns in strict initiative order; player cannot take consecutive turns
- **Reaction Window Protocol**: Mandatory pauses before attack resolution for Shield/Parry, before spell resolution for Counterspell, after damage for Hellish Rebuke
- **Combat End Protocol**: Sets combat_phase to "ended", computes xp_awarded, updates player XP before any post-combat narration
- **XP Display**: Narrative text MUST include XP breakdown visible to users
- **Turn Processing**: After player ends turn, ALL ally/enemy turns processed before player input

## Key Quotes
> "CRITICAL: ALL combatants MUST take turns in initiative order - NO consecutive player turns"

> "CRITICAL: Player controls when their turn ends - do NOT auto-end after one action"

## Connections
- [[Initiative Order]] — strict turn sequencing enforcement
- [[Reaction Window Protocol]] — pre-hit, pre-spell, post-damage reaction triggers
- [[Combat Victory Protocol]] — end-of-combat XP handling and display
- [[Dice System]] — mandatory rolling for all attacks/saves

## Contradictions
- None detected
