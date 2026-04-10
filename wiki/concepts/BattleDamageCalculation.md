---
title: "Battle Damage Calculation"
type: concept
tags: [battle-simulation, damage-calculation, bug]
sources: [battle-simulation-bug-tests-pr-2778]
last_updated: 2026-04-08
---

## Description
Mechanics for calculating damage dealt in battle simulations. In the context of D&D 5e faction combat, damage is computed per round based on attacker strength versus defender groups.

## Bug Details
The bug (#1 in [[PR2778]]) caused damage to be incorrectly multiplied by the number of defender groups. This meant that splitting defenders into multiple groups would increase total incoming damage, which violates physics.

## Related Concepts
- [[MoraleThresholdLogic]] — related bug in rout decision
- [[SRDUnits]] — unit stat blocks used in calculations
- [[FactionBattleSimulation]] — broader system
