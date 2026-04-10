---
title: "Timestamp Progression"
type: concept
tags: [timestamp, time, progression, validation]
sources: []
last_updated: 2026-04-07
---

## Description
Temporal consistency rule ensuring scene timestamps move forward logically without reversals or unrealistic gaps.

## Key Requirements
- Forward progression: timestamps must always increase
- Logical increments: 5-15 minutes for small actions, 30-60 minutes for combat
- No reversals: Scene N+1 timestamp must be greater than Scene N

## Fix History
- **Before**: Scene 20→21 showed reversal (11:15→10:45)
- **After (Iteration 005)**: Completely fixed, logical progression throughout

## Connections
- [[20TurnTestImprovementSummary]] — validated via 20-turn test
- [[PromptEngineering]] — fixes applied via prompt clarifications
