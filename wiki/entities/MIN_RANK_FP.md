---
title: "MIN_RANK_FP"
type: entity
tags: [constant, faction, ranking]
sources: [faction-ranking-calculation-tests, faction-ranking-recompute-tests, faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

Minimum faction power threshold required for a player faction to appear on the ranking board. Defined in `mvp_site.constants`. Factions below this threshold are excluded from ranking calculations.

## Usage
Used by `calculate_ranking()` in `mvp_site.faction.rankings` to determine if a player faction qualifies for ranking display.

## Related
- [[Faction Ranking Calculation Tests]]
- [[Faction Combat Power Calculation Tests]]
