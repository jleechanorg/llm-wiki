---
title: "mvp_site upkeep"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/upkeep.py
---

## Summary
Unit upkeep calculation for WorldAI Faction Management. Implements D&D 5e hireling wages for military unit costs.

## Key Claims
- calculate_unit_upkeep() formula: soldiers*0.5gp + spies*1gp + elites*5gp per week
- Soldiers: 0.5gp/week (conscript/regular pay)
- Spies: 1gp/week (specialist pay)
- Elites: 5gp/week (elite unit pay)

## Connections
- [[FactionMinigame]] — unit upkeep costs
