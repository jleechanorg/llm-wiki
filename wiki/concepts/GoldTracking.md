---
title: "Gold Tracking"
type: concept
tags: [gold, currency, tracking, game-state]
sources: []
last_updated: 2026-04-07
---

## Description
Dual-currency system tracking character personal wealth separately from faction treasury.

## Key Requirements
- **Character Gold**: Personal wealth (10gp baseline)
- **Faction Gold**: Treasury pool (tracked separately in faction header)
- No confusion between pools

## Fix History
- **Before**: Confusion between character gold and faction gold (Scene 18: 110gp)
- **After (Iteration 005)**: Dual gold tracking working (24gp faction / 10gp character)

## Connections
- [[20TurnTestImprovementSummary]] — validated via 20-turn test
- [[GameStateManagement]] — requires separate state pools
