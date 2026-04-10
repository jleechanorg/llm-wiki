---
title: "Faction Ranking"
type: concept
tags: [game-mechanics, faction, ranking]
sources: [faction-ranking-calculation-tests, faction-ranking-recompute-tests]
last_updated: 2026-04-08
---

The system that orders factions by their Faction Power (FP) from highest to lowest. Determines a player's position relative to AI factions on the ranking board.

## Key Functions
- `calculate_ranking(player_fp, turn_number)` - Returns rank position and sorted faction list
- `get_all_ai_factions()` - Retrieves AI faction base FP values

## Ranking Logic
1. Player FP is compared against all AI faction FP values
2. Factions are sorted by FP descending
3. Player rank is position in sorted list (1 = highest)
4. Only factions above MIN_RANK_FP are displayed

## Related Tests
- [[Faction Ranking Calculation Tests]]
- [[Faction Ranking Recompute Tests]]
