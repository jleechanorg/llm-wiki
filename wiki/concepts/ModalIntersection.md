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

- [[AdminOverrideContract]] — admin overrides commonly cause intersection violations
- [[ModalAgentConstraint]] — individual modal constraints
- [[StaleFlag]] — the symptom
- [[Cross-Modal-Interaction]] — existing concept on cross-modal patterns
