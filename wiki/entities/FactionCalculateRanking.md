---
title: "FactionCalculateRanking"
type: entity
tags: [tool, faction-combat, ranking]
sources: [faction-ranking-recompute-tests, faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

Faction combat tool that calculates the player's faction ranking based on their faction power relative to other factions. Requires accurate faction power values — if called without power tool or with stale FP, ranking should be recomputed.

## Usage Pattern
- Input: player_faction_power (int), turn_number (int)
- Output: ranking (int), total_factions (int)
- Dependencies: Must be called after [[FactionCalculatePower]] with accurate power values

## Known Issues
- Previously could be called with placeholder FP=0 when LLM forgot to emit power tool
- HIGH priority fix ensures ranking is dropped and recomputed when power is missing or stale
