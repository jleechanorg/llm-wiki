---
title: "WorldAI Faction Management"
type: entity
tags: [project, game-mechanics, worldai]
sources: []
last_updated: 2026-04-08
---

## Overview
WorldAI Faction Management is the module/system within WorldArchitect.AI that handles NPC faction resources, including military unit tracking, resource expenditure, and strategic decision-making.

## Key Components
- Unit upkeep calculation (soldiers, spies, elites)
- Resource budgeting for faction activities
- Integration with [GameState](GameState.md) for persistent faction data

## Connections
- Related to [GameState](GameState.md) for faction state storage
- Related to [[FactionToolDefinitions]] for LLM function calling interface
- Used in [ThinkMode](../concepts/ThinkMode.md) for strategic planning
