---
title: "Battle Simulation Bug Tests (PR #2778)"
type: source
tags: [python, testing, unittest, tdd, battle-simulation, bug-fix]
source_file: "raw/battle-simulation-bug-tests-pr-2778.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite reproducing battle simulation bugs before fixing them using TDD methodology. Tests cover two critical bugs: damage calculation incorrectly multiplying by defender group count, and morale threshold logic inverted to check casualties instead of HP remaining.

## Key Claims
- **Bug #1 - Damage Multiplication**: Damage calculation incorrectly multiplies total damage by number of defender groups, causing same attackers to deal different damage based on defender grouping
- **Bug #2 - Morale Threshold Inverted**: Morale rout check uses inverted logic - triggers at 25% casualties instead of 25% HP remaining (75% casualties)
- **TDD Validation**: Tests are written to FAIL before fixes are applied, validating the bug reproduction

## Key Code Patterns
```python
from mvp_site.faction.battle_sim import (
    _calculate_round_casualties_fast,
    _check_morale_rout,
    _simulate_round_detailed,
)
from mvp_site.faction.srd_units import create_unit_group

# Damage test: single vs split defender groups
damage_single = _calculate_round_casualties_fast(attackers, defenders_single)
damage_split = _calculate_round_casualties_fast(attackers, defenders_split)

# Morale test: 25% HP remaining should trigger rout
units[0]["remaining"] = 25  # 25% remaining = 75% casualties
should_rout = _check_morale_rout(units)
```

## Connections
- [[PR2778]] — PR containing these bug fixes
- [[BattleSimulation]] — module under test
- [[SRDUnits]] — unit creation utilities
- [[TDD]] — test methodology used

## Contradictions
- None identified yet — this is the test source for bugs yet to be fixed
