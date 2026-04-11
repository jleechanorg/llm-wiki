---
title: "Iteration 007 Campaign Analysis"
type: source
tags: [testing, E2E, iteration-007, worldarchitect, economic-modeling, ranking-system]
sources: []
source_file: ~/Downloads/campaigns/Iteration 007 Campaign.txt
date: 2026-01-13
last_updated: 2026-04-07
---

## Summary

Iteration 007 shows major improvements over previous versions with consistent resource change logs, FP calculation transparency, and properly modeled economic systems. However, critical design flaws make the game unplayable: catastrophic economic failure due to upkeep being 10x too high (instant bankruptcy), and a broken ranking system where the player remains stuck at Rank #201 despite accumulating 11,923 FP. All 25 turns passed, but the economic and ranking systems require fundamental rebalancing.

## Key Claims

- **Resource Change Logs ✅**: Consistent and transparent `[RESOURCE CHANGE LOG]` blocks across all turns
- **FP Calculation Transparency ✅**: Formula breakdown shown in Scene 25 (territory, soldiers, fortifications)
- **Failed Actions Blocked ✅**: Correctly blocks failed actions (spy checks, persuasion rolls)
- **Economic Modeling ✅**: Upkeep system properly implemented, just needs rebalancing
- **Catastrophic Economic Failure 🔴**: Upkeep 10x too high (7gp/soldier/week vs expected 0.5-1gp), tax income 50x too low (0.02gp vs 1-2gp per citizen)
- **Ranking System Broken 🔴**: Player stuck at Rank #201/201 despite 11,923 FP (4,673 soldiers + 525 territory + 2 fortifications)

## Critical Issues

### 1. Catastrophic Economic Failure
- **Upkeep**: 32,760gp for 4,673 soldiers (~7gp per soldier/week)
- **Income**: Only 590gp per turn (from 20,000 citizens)
- **Result**: Treasury goes from +1,680gp to -30,490gp in one turn
- **Root Cause**: Upkeep formula 10x too high compared to D&D 5e RAW; tax income 50x too low

### 2. Ranking System Broken
- **Player FP**: 11,923 total (4,673 soldiers + 5,250 territory + 2,000 fortifications)
- **Rank**: Stuck at #201/201 (dead last)
- **Root Cause**: Ranking threshold absurdly high, calculation doesn't update properly, or system non-functional

## Improvements Over Previous Versions

- Resource change logs consistent and transparent
- FP formula breakdown visible
- Failed actions correctly blocked
- Economic modeling implemented (upkeep system works)
- No entity hallucination
- Soldier counts consistent (4,935 - 262 = 4,673)

## Test Results
- **Total turns**: 25
- **Successful**: 25/25 ✅
- **Failed**: 0
- **Faction headers**: 22/25
- **Tutorial detected**: 21 turns
- **Tools used**: `faction_calculate_power`, `faction_calculate_ranking`

## Recommended Fixes

**Phase 1 (Critical):** Rebalance upkeep to 0.5-1gp/soldier/week, increase tax to 1-2gp/citizen/week, add bankruptcy warnings

**Phase 2 (Ranking):** Fix ranking calculation, rebalance FP formula, add construction cost menu

**Phase 3 (Polish):** Enforce turn action budget, fix spy recruitment, clarify troop accounting