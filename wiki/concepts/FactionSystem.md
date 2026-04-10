---
title: "Faction System"
type: concept
tags: [game-mechanics, faction, simulation, rpg]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Game system for managing factions in WorldAI: battle simulation, intel operations, rankings, and power calculation. Provides tools for LLM to trigger backend faction mechanics.


## Core Components
- Battle simulation with soldier/elite units and fortifications
- Intel/spy operations with success tiers
- Ranking calculations with faction points progression
- Power calculation for faction strength

## Connections
- [[LLMFunctionCalling]] — execution mechanism
- [[FactionToolDefinitions]] — tool definitions
- [[ThinkMode]] — strategic planning integration
