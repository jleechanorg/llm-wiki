---
title: "Deterministic Generation"
type: concept
tags: [random-generation, seeding, reproducibility]
sources: []
last_updated: 2026-04-08
---

Deterministic generation uses a fixed random seed to ensure consistent output across multiple executions. In the AI Faction Generator, the seed (AI_FACTION_SEED) guarantees the same 200 factions are generated every session.

## How It Works
1. Initialize `random.Random(seed)` with fixed seed
2. All subsequent random calls produce identical sequences
3. Same faction names, FP values, behaviors generated each run

## Use Cases
- Game leaderboards requiring consistent AI opponents
- Testing and debugging with reproducible game state
- Save/load systems that depend on faction consistency
