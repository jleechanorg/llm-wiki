---
title: "Faction Rankings Module"
type: entity
tags: [faction, rankings, progress, points]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Module in mvp_site.faction.rankings that calculates faction rankings and progress toward next rank. Exposed via faction_calculate_ranking and faction_fp_to_next_rank tools.

## Connections
- [[FactionToolDefinitions]] — exposed via tool definition
- [[FactionCombat]] — related power calculations
