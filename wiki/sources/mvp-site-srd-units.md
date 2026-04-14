---
title: "mvp_site srd_units"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/srd_units.py
---

## Summary
D&D 5.1 SRD stat block mapping for faction units. Maps faction unit archetypes (soldier, veteran, spy, scout, assassin, elite) to SRD creature stat blocks. Provides scaling functions for elite units based on character levels.

## Key Claims
- UNIT_TO_SRD_MAP: soldier→guard, veteran→veteran, spy→spy, scout→scout, assassin→assassin, elite_6→knight, elite_10→gladiator
- UNIT_ARCHETYPE_ALIASES maps genre-neutral names to SRD archetypes
- SRDStatBlock TypedDict: name, ac, hp, attack_bonus, damage_dice, cr, traits
- Generic aliases allow any genre to resolve to same SRD archetypes

## Connections
- [[FactionMinigame]] — SRD stat block mapping for faction units
- [[CombatSystem]] — SRD creatures for combat simulation
