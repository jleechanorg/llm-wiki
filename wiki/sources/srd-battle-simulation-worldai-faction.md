---
title: "SRD-based Battle Simulation for WorldAI Faction Management"
type: source
tags: [worldarchitect, battle-simulation, dnd, sr, combat, faction, python]
source_file: "raw/srd-battle-simulation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Implements D&D 5.1 SRD combat mechanics for tactical battle resolution between faction forces in WorldArchitect.AI. Supports three simulation modes: Fast (deterministic expected damage), Detailed (full roll-by-roll with combat log), and Deterministic (seeded RNG for reproducible results). All mechanics follow official D&D 5.1 SRD rules.

## Key Claims
- **Three Simulation Modes**: Fast mode uses expected damage calculation (no dice, deterministic), Detailed mode runs full roll-by-roll with combat log, Deterministic mode uses seeded RNG for test reproducibility
- **D&D 5.1 SRD Compliance**: Implements official SRD rules for attack rolls, damage rolls, initiative order, and combat resolution
- **Morale Rout System**: Units retreat when HP falls below MORALE_ROUT_THRESHOLD, simulating realistic battlefield behavior
- **Type Safety**: Uses TypedDict for BattleResult with casualties, rounds, victor, and detailed_log fields

## Key Functions
- `parse_damage_dice()`: Parses damage strings like "2d8+3" into (num_dice, die_size, modifier)
- `calculate_expected_damage_value()`: Computes expected damage without rolling for fast mode
- `roll_attack()`: Resolves attack roll against target AC with critical hit/miss handling
- `calculate_hit_chance()`: Computes probability of hitting target for fast mode calculations
- `simulate_battle()`: Main entry point for all three simulation modes

## Connections
- [[WorldArchitect.AI]] — the parent platform this battle system supports
- [[AI Faction Generator]] — generates the faction units that battle in this simulation

## Contradictions
- None identified
