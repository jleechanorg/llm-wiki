---
title: "Modal Intersection Neglect Pattern"
type: source
tags: [modal, intersection, state-machine, worldarchitect]
date: 2026-05-09
source_file: raw/feedback_2026-05-09_modal_intersection_neglect.md
---

## Summary

When two modal systems are active simultaneously (character creation + level-up, combat + living world), neither handler clears the other's stale state. This causes players to be trapped in one modal while the other system expects normal flow. Each modal handler was written in isolation; intersection testing was never part of the design.

## Key Claims

- Concurrent modal systems corrupt each other's state when they overlap
- Character creation and level-up modals can be active simultaneously without either clearing the other
- Combat state and living world turns have the same intersection problem
- Hypothesis-style parametrized property tests are the correct fix

## Key Quotes

> "When two modal systems interact (CC + level-up, combat + LW), neither handler clears the other's stale state." — session analysis

## Connections

- [[ModalIntersection]] — the concept page
- [[ModalAgentConstraint]] — individual modal constraints
- [[AdminOverrideContract]] — admin overrides are a common cause of intersection violations
- [[StaleFlag]] — the symptom class
