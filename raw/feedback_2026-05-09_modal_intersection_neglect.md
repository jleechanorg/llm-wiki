---
name: Modal Intersection Neglect Pattern
description: Concurrent modal systems corrupt each other's state when they overlap
type: feedback
bead: rev-modal-intersect
---

When two modal systems are active simultaneously (CC + level-up, combat + living world), neither handler clears the other's stale state. This causes players to be trapped in one modal while the other system expects normal flow.

**Pattern seen in**: PR #6842 (CC modal guard doesn't account for concurrent level-up), PR #6839 (cooldown field clearing misses intersection with combat state).

**Fix direction**: Hypothesis-style parametrized property tests that verify all modal intersection combos produce consistent state.

**Why**: Each modal handler was written in isolation. Intersection testing was never part of the design, so stale cross-modal state accumulates silently.

**How to apply**: When adding or modifying a modal handler (character creation, level-up, combat), enumerate its intersections with every other active modal and add property tests for each combo.
