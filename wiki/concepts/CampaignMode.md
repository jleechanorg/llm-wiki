---
title: "Campaign Mode"
type: concept
tags: [campaign-mode, game-state, dnd, faction]
sources: ["dual-mode-campaign-system-dnd-faction-integration"]
last_updated: 2026-04-08
---

## Definition
The current focus state of a campaign, determining how time passes and what player actions are available.

## Modes

### ADVENTURE Mode
- Focus on personal character actions
- Time flows in minutes/hours
- Combat, exploration, dialogue interactions
- Linked to [[DungeonsAndDragons]] rules

### FACTION Mode
- Focus on organizational/kingdom management
- Time flows in days/weeks (1 turn = 7 days)
- Resource management, strategic decisions
- Neglect warnings when ignoring too long


## Switching
Commands: /adventure enters personal mode, /faction enters strategic mode. Switching generates attention triggers if player has neglected one mode while focusing on the other.

## Related Concepts
- [[DualModeCampaignSystem]] — parent system
- [[AttentionTriggers]] — alerts when switching modes
- [[StrategicTurn]] — time unit in faction mode
