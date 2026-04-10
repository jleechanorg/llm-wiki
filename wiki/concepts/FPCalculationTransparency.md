---
title: "FP Calculation Transparency"
type: concept
tags: [prompt-engineering, game-state, transparency]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
Displaying the components and delta breakdown of Faction Points (FP) changes so players understand why their FP jumped or changed.

## Problem
FP jumped from 5,750 to 12,000 with no apparent in-game action, leaving players confused about the source of gains.

## Solution
In prompts, show FP components:
- Base income per turn
- Bonus from victories/events
- Penalties from losses
- Current delta from previous state

## Related Concepts
- [[GoldCalculation]] — similar transparency for gold
- [[GameStateManagement]] — state display
