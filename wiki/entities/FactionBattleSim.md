---
title: "Faction Battle Simulator"
type: entity
tags: [faction, battle, simulation, python]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Module in mvp_site.faction.battle_sim that simulates tactical battles between attacker and defender forces. Returns casualties, victor, rounds fought, and battle log.

## Usage
Called via faction_simulate_battle tool with attacker/defender soldier and elite counts, fortification levels, and optional battle seed.

## Connections
- [[FactionToolDefinitions]] — exposed via tool definition
- [FactionCombat](FactionCombat.md) — related combat calculations
- [SRDUnits](SRDUnits.md) — unit definitions used in battle
