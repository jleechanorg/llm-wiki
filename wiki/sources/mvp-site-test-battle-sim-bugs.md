---
title: "test_battle_sim_bugs.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
TDD tests for battle simulation bugs identified in PR #2778. Tests reproduce bugs before fixing them including damage multiplier, morale threshold, casualty calculation, and elite type handling issues.

## Key Claims
- **Bug #1**: Damage should NOT be multiplied by defender group count (5% tolerance test)
- **Bug #2**: Morale rout threshold checks HP remaining, not casualties (25% remaining = rout)
- **Bug #7**: Casualty calculation must weight by unit count, not group count
- **Bug #8**: Invalid elite type returns error dict, not KeyError crash
- **Bug #9**: Damage dice scaling preserves negative modifier sign
- Tests both `_calculate_round_casualties_fast` and `_simulate_round_detailed` modes

## Key Quotes
> "These tests reproduce the bugs before fixing them (TDD approach)."

## Connections
- [[battle_sim]] — the module being tested
- [[srd_units]] — provides unit creation helpers