---
title: LLM Decides, Server Executes
type: concept
tags: [architecture-pattern, validation, dnd, state-management]
date: 2026-05-16
---

## Summary
Core architecture pattern: LLM proposes state changes, server validates and persists them. Prevents LLM from directly writing to Firestore — all proposals go through `world_logic.py` validation. This ensures mechanical integrity (dice, stats, rules) while preserving narrative immersion.

## Connections
- [[WorldArchitectAI]] — core pattern
- [[DiceIntegrity]] — enforces this for dice
- [[TokenBudget]] — enforces this for prompt assembly
