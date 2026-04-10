---
title: "Agent Priority Ordering"
type: concept
tags: [agent, architecture, priority, routing]
sources: [dialog-agent-end2end-tests]
last_updated: 2026-04-08
---

## Description
System for selecting the appropriate agent based on game state context. The priority ordering determines which agent handles a given request: RewardsAgent → DialogAgent → StoryModeAgent.

## Priority Flow
1. **RewardsAgent** — handles reward-related state updates
2. **DialogAgent** — handles dialog state continuity or explicit dialog mode
3. **StoryModeAgent** — handles general story continuation

## Selection Criteria
- Dialog state continuity detection
- Explicit dialog mode requests
- Game state context analysis
