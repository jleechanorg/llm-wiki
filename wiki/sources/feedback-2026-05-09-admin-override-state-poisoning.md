---
title: "Admin Override State Poisoning Pattern"
type: source
tags: [admin-override, state-machine, modal-flags, worldarchitect]
date: 2026-05-09
source_file: raw/feedback_2026-05-09_admin_override_state_poisoning.md
---

## Summary

God mode and admin override actions bypass state machine entry/exit protocols in `world_logic.py`. After the override, stale modal flags (level_up_pending, character_creation_in_progress, combat_active) persist, trapping players in modal loops or skipping required transitions. Three separate PRs (#6844, #6842, #6825) independently discovered this pattern.

## Key Claims

- Admin short-circuits leave stale modal flags because no post-override invariant check exists
- The pattern recurs across character creation, level-up, and combat state machines
- A declarative `ADMIN_OVERRIDE_CONTRACTS` dict mapping each override to required post-override invariants would prevent regressions
- `_validate_post_override_state()` enforcement after each override execution is the correct fix direction

## Key Quotes

> "God mode and admin actions short-circuit state machines (character creation, level-up, combat), leaving stale flags that trap players in modal loops." — session analysis

## Connections

- [[AdminOverrideContract]] — proposed declarative contract solution
- [[StaleFlag]] — the symptom class
- [[ModalAgentConstraint]] — modal exit constraints
- [[ZeroFrameworkCognition]] — LLM decides, server executes; admin overrides violate server-ownership boundary
- [[WorldLogicStrip]] — the primary file where overrides live
