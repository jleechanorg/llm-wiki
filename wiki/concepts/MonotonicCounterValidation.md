---
title: "Monotonic Counter Validation"
type: concept
tags: [validation, game-state, server-side]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
Server-side validation enforcing that certain counters (XP, gold, territory) can only increase, never decrease — reflecting that player progress should not regress.

## Problem
XP decreased from 800/900 to 550/900 between scenes, indicating state corruption or prompt hallucination.

## Solution
Add server-side validation that:
1. Tracks current value for XP, gold, territory counters
2. Rejects any LLM response that would decrease these values
3. Returns error for monotonic violations instead of applying delta

## Related Concepts
- [[GameStateManagement]] — overall state handling
- [[CampaignCoherence]] — maintaining consistent player progress
