---
title: "AI Faction Generator for WorldAI Faction Management"
type: source
tags: [ai-factions, worldarchitect, deterministic-generation, game-mechanics, ranking-system]
source_file: "raw/ai-faction-generator-worldai-faction-management.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module generating 200 deterministic AI factions for the WorldAI ranking system using seeded random generation. Ensures consistent faction rosters across sessions with attributes including names, difficulty levels, base FP values, behaviors, and aggression levels.

## Key Claims
- **Deterministic Generation**: Uses seeded random (AI_FACTION_SEED) to ensure same factions across sessions
- **Difficulty Distribution**: 30% Easy (5K-50K FP), 40% Medium (75K-300K FP), 30% Hard (400K-1.5M FP)
- **Name Generation**: Combines 100+ adjectives and 70+ nouns for unique faction names
- **Behavior System**: 15 behavior types including defensive, isolationist, trader, raider, expansionist
- **Aggression Scaling**: Difficulty-linked aggression levels (Easy: 0.1-0.4, Hard: higher)

## Key Components

### Name Generation
- **Adjectives**: Ancient, Azure, Blazing, Celestial, Crimson, Divine, Emerald, etc. (100+)
- **Nouns**: Alliance, Armada, Bastion, Brotherhood, Citadel, Dominion, Empire, etc. (70+)
- **Behaviors**: defensive, isolationist, trader, raider, expansionist, aggressive, arcane, diplomatic

### Difficulty Tiers
| Tier | FP Range | Distribution | Aggression |
|------|----------|--------------|------------|
| Easy | 5K-50K | 30% | 0.1-0.4 |
| Medium | 75K-300K | 40% | moderate |
| Hard | 400K-1.5M | 30% | high |

## Connections
- [[WorldAI]] — product using this faction generator for ranking system
- [[WorldArchitectAI]] — parent platform
- [[FactionMinigame]] — related game mechanic

## Contradictions
- None identified
