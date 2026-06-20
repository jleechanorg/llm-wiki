---
title: "Modal Intersection"
type: concept
tags: [architecture, modal, state-machine, testing, worldarchitect]
---

When two modal systems are active simultaneously, neither handler clears the other's stale state. This causes players to be trapped in one modal while the other system expects normal flow. Each modal handler was written in isolation; intersection testing was never part of the design.

## Known intersections

- Character creation + level-up
- Combat + living world
- Level-up + combat trigger

## Fix direction

Hypothesis-style parametrized property tests that verify all modal intersection combos produce consistent state.

## Related

- [AdministrativeStatePoisoning](AdministrativeStatePoisoning.md) — admin shortcuts are the most common cause
- [AdminOverrideContract](AdminOverrideContract.md) — admin overrides commonly cause intersection violations
- [ModalAgentConstraint](ModalAgentConstraint.md) — individual modal constraints
- [StaleFlag](StaleFlag.md) — the symptom
- [Cross-Modal-Interaction](Cross-Modal-Interaction.md) — existing concept on cross-modal patterns
