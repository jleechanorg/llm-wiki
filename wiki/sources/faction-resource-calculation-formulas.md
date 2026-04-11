---
title: "Faction Resource Calculation Formulas"
type: source
tags: [game-mechanics, faction-management, resource-calculation, worldai, python]
source_file: "raw/faction-resource-calculation-formulas.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Implements exact formulas for WorldAI Faction Management resource calculations including citizen growth, gold income, arcana yield, building construction rates, and unit recruitment rates. All formulas are reverse-engineered from the WorldAI Faction Management ruleset with mathematical precision.

## Key Claims
- **Citizen Growth Formula** — 50 + 0.015 × current_citizens, with taper at 90-100% capacity and negative growth when over max
- **Gold Income** — Tax revenue (0.5gp per citizen) + Farm surplus (100gp per farm) + Trade routes (200gp per artisan guild) + optional prosperity ritual doubling
- **Arcana Yield** — Complex formula based on mana font percentage with optimal ratio at 55-56% fonts to avoid diminishing returns
- **Max Capacity** — Citizens capped at territory × 50

## Key Formulas
```
Citizens Growth: 50 + 0.015 × current_citizens (tapers at 90%+ capacity)
Gold Income: (citizens × 0.5) + (farms × 100) + (artisans × 200) × (prosperity ? 2 : 1)
Arcana Yield: floor(100 × fonts / territory) → complex yield calculation with diminishing returns
Max Citizens: territory × 50
```

## Connections
- [[Faction Power Rankings System]] — uses these resource calculations for faction strength
- [[NPC Relationship Trust System]] — separate system for NPC interactions
- [[Real Service Provider Implementation]] — could use these formulas for game state

## Contradictions
- None identified
