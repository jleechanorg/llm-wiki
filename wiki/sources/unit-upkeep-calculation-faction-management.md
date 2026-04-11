---
title: "Unit Upkeep Calculation for WorldAI Faction Management"
type: source
tags: [python, faction-management, dnd-5e, economics, game-mechanics]
source_file: "raw/unit-upkeep-calculation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module implementing upkeep costs for military units in WorldAI Faction Management, based on D&D 5e hireling wages. Calculates weekly gold piece costs for soldiers, spies, and elite units using scaled formulas.

## Key Claims
- **Soldier Upkeep**: 0.5gp per soldier per week (conscript/regular pay)
- **Spy Upkeep**: 1gp per spy per week (specialist pay)
- **Elite Upkeep**: 5gp per elite unit per week (elite unit pay)
- **Total Cost**: Sum of all unit upkeep using integer arithmetic

## Key Quotes
> "Formula (based on D&D 5e hireling wages)"

## Connections
- [[FactionToolDefinitions]] — faction management system this supports
- [[GameState]] — stores unit counts and tracks resource expenditures
- [[ThinkMode]] — strategic planning may factor unit costs into decisions

## Contradictions
- None identified
