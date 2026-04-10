---
title: "Faction Campaigns"
type: concept
tags: ["campaign-type", "game-mode", "faction"]
sources: ["llm-first-state-management-plan-pr-2778"]
last_updated: 2026-04-07
---

# Faction Campaigns

## Definition
A campaign type in WorldArchitect.AI where players manage a faction alongside their character.


## Complexity Factors
- **Dual Gold Tracking**: character.gold (personal) + faction.resources.gold (treasury)
- **Turn Number Tracking**: Strategic turns vs narrative scenes
- **Tutorial Progress**: Multi-phase tutorial with completion detection
- **Longer sequences**: 20-turn test generates 25+ scenes

## Why Issues Are More Visible
1. Longer sequences (20-turn test generates 25+ scenes)
2. More complex state (dual gold tracking)
3. Additional state variables (turn numbers, rankings, tutorial progress)
4. Structured testing designed to catch long-term drift

## Shared Path with Normal Campaigns
- Same LLM service
- Same narrative generation
- Same state management
- Same timestamp tracking
- **Fixes benefit both campaign types**
