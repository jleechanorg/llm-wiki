---
title: "mvp_site — Faction Rankings System"
type: source
tags: [worldarchitect-ai, rankings, faction-power, AI-factions, leaderboard]
date: 2026-04-14
source_file: raw/mvp_site_all/rankings.py
---

## Summary

Implements the exact formulas for calculating Total Faction Power (FP) and ranking all 200 AI factions. The 200 AI factions are dynamically generated deterministically using `generate_ai_factions()` — ensuring consistent names, stats, and behaviors across sessions.

## Key Claims

### 200 AI Faction Generation
- `generate_ai_factions()` from `faction.ai_factions` module
- Deterministic: same seed → same 200 factions every session
- Each faction has: name, difficulty, base_fp, behavior, aggression

### FactionStats TypedDict
```
soldiers, spies, elites, elite_avg_level, territory, fortifications,
citizens, gold_pieces, arcana, prestige
```

### Faction Power Formula
- Combines military (soldiers, spies, elites), economic (gold, citizens, territory), and soft (prestige, arcana) power
- [[mvp-site-combat]] calculates damage using FP as the base unit metric
- Ranking position calculated from FP relative to all 200 factions

### Minimum Rank Threshold
`MIN_RANK_FP` — minimum FP required to appear on leaderboard (filters out factions with near-zero power)

## Connections

- [[mvp-site-combat]] — combat damage calculation uses FP
- [[mvp-site-ai-factions]] — the 200-faction generator
- [[FactionPower]] — the general concept
- [[ArmyFactionPower]] — campaign-side faction power tracking
