---
title: "Game State Navigation"
type: concept
tags: [game-state, data-structures, extraction]
sources: [faction-minigame-state-access-utilities]
last_updated: 2026-04-08
---

The practice of extracting nested data from various game_state structures that may exist in different formats (object attributes, dict keys, data wrappers). Game state navigation handles precedence order when multiple access paths exist.

## Canonical Location
In WorldArchitect.AI, faction_minigame is stored in `custom_campaign_state["faction_minigame"]` — this is the canonical location that should be checked first before falling back to direct attribute access.
