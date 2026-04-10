---
title: "Gold Ledger Tracking"
type: concept
tags: [prompt-engineering, game-state, economics]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
A weekly/turn-by-turn ledger block showing income sources and expenses for gold, providing transparency into economic changes.

## Problem
Gold jumped from 331 to 26,756 (+26,425) in one week with no explanation — extreme unexplained wealth that breaks game balance.

## Solution
Add ledger block in game state showing:
- Starting gold
- Income by source (trade, loot, taxes, etc.)
- Expenses by category (upkeep, construction, units, etc.)
- Net change per period

## Related Concepts
- [[FPCalculationTransparency]] — similar transparency for FP
- [[GameStateManagement]] — economic state
