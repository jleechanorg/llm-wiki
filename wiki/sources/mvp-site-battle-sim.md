---
title: "Battle Simulation"
type: source
tags: [battle-sim, combat, dice-rolling, srdd5, tactical]
sources: []
last_updated: 2026-04-14
---

## Summary

SRD-based D&D 5.1 battle simulation for WorldAI faction management. Supports three simulation modes: Fast (expected damage, deterministic), Detailed (full roll-by-roll with combat log), and Deterministic (seeded RNG for reproducible tests). Implements attack rolls, damage rolls, initiative, morale routing, and casualty distribution mechanics.

## Key Claims

- **Three Simulation Modes**: Fast (no dice, expected damage), Detailed (full simulation with log), Deterministic (seeded RNG for tests)
- **D&D 5.1 SRD Compliance**: Attack rolls use d20 with natural 1=failure and natural 20=critical hit
- **Morale Rout System**: Forces retreat when remaining HP <= MORALE_ROUT_THRESHOLD percentage
- **Proportional Casualty Distribution**: Larger groups take proportionally more casualties
- **Weighted Average AC/HP**: Uses weighted averages by unit count for hit chance and damage calculations
- **Attack Scaling**: Caps attacks per group at 10 but scales damage proportionally (e.g., 100 units -> 10 attacks * 10.0 scale factor)

## Key Quotes

> "Implements D&D 5.1 SRD combat mechanics for tactical battle resolution between faction forces"

> "d20 == 1: return False (natural 1 miss); d20 == 20: return True (natural 20 hit)"

> "Larger groups take proportionally more casualties since they present bigger targets"

## Connections

- [[CombatState]] — battle simulation produces combat state
- [[AttackRoll]] — attack resolution mechanics
- [[BattleDamageCalculation]] — damage calculation logic
- [[MoraleRout]] — morale routing system

## Contradictions

- None identified