---
title: "Turn Advancement Mechanics"
type: concept
tags: [game-design, strategic-tick, prompt-engineering]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
Defining Turn as a strategic time tick that gates player actions (1-3 actions per turn), with scenes representing individual action resolutions within that turn.

## Problem
All Scenes 1-25 occur in Turn 1 despite major campaign events — turn concept not being utilized.

## Solution
Define in prompts:
- **Turn**: Strategic time unit (1 week in-game)
- **Actions per turn**: 1-3 player actions (attacks, diplomacy, building, etc.)
- **Scene**: Resolution of one action
- Advance turn counter when all actions exhausted

## Related Concepts
- [[TimestampProgression]] — time tracking in game
- [[GameStateManagement]] — strategic state
