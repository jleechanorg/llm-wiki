---
title: "Faction Minigame"
type: concept
tags: [game-feature, faction-system, nested-state]
sources: []
last_updated: 2026-04-08
---

A faction-based minigame system within the campaign framework. The faction_minigame state can exist at multiple locations in the game_state structure:
- Direct attribute: `game_state.faction_minigame`
- Custom campaign state: `game_state.custom_campaign_state.faction_minigame`
- Data wrapper: `game_state.data.game_state.custom_campaign_state.faction_minigame`

## Related Concepts
- [[FactionStateUtil]] — utility module for accessing faction minigame state
- [[FactionSettingsPersistence]] — settings system that persists faction minigame preferences
- [[FactionRankingCalculation]] — ranking system that calculates faction combat power
