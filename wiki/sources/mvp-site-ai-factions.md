---
title: "AI Factions Generator"
type: source
tags: [ai-factions, deterministic, ranking-system, faction-generation]
sources: []
last_updated: 2026-04-14
---

## Summary

Generates 200 deterministic AI factions for the WorldAI faction ranking system using seeded random generation. Ensures consistency across sessions through fixed seeds and controlled distribution of difficulty tiers (30% easy, 40% medium, 30% hard). Each faction has name, difficulty, base FP value, behavior type, and aggression level.

## Key Claims

- **Deterministic Generation**: Uses `AI_FACTION_SEED` constant to ensure same factions across sessions
- **Distribution Formula**: Easy (30%): 5K-50K base FP, low aggression (0.1-0.4); Medium (40%): 75K-300K base FP, moderate aggression (0.3-0.6); Hard (30%): 400K-1.5M base FP, high aggression (0.5-0.8)
- **Unique Name Generation**: Uses adjective + noun pattern with 100+ adjectives and 180+ nouns, handles collisions via numeric suffix fallback
- **Behavior Types**: 20 behavior types including defensive, isolationist, trader, raider, expansionist, aggressive, arcane, diplomatic, shadowy, nature, imperial, mysterious, dominating, crusading
- **Sorted Output**: Factions sorted by base_fp ascending (weakest to strongest)

## Key Quotes

> "Creates a fixed roster of AI factions with consistent names, difficulties, base FP values, behaviors, and aggression levels"

> "Uses seeded random generation to ensure the same factions are generated across sessions"

> "Fallback: add numeric suffix if we somehow exhaust combinations"

## Connections

- [[FactionRankings]] — generated factions are used in ranking system
- [[ArmyFactionPower]] — related concept for faction power calculation
- [[AIFactionBehavior]] — behavior types defined here

## Contradictions

- None identified