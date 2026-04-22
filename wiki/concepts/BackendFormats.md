---
title: "Backend Formats"
type: concept
tags: [zfc, architecture, backend, formatter]
sources: [zfc-level-up-model-computes-north-star-2026-04-19]
last_updated: 2026-04-20
---

**Backend Formats** — ZFC architectural pattern where the backend is pure formatter: validates and formats model output for UI, without semantic inference.

## Definition

Under the ZFC North Star, backend code (`rewards_engine.py`, `game_state.py`, `world_logic.py`) must not:
- Compute XP totals (model computes)
- Detect level-up thresholds (model computes)
- Decide reward eligibility (model computes)
- Scan for `_has_rewards_narrative` keywords (ZFC violation)

The backend's sole responsibility is:
1. Parse structured model output
2. Validate required fields exist
3. Format into UI structures (`rewards_box`, `planning_block`)
4. Compute deterministic display values from explicit totals

## Display Value Computations

From explicit `previous_turn_exp` and `current_turn_exp`:
- `xp_gained = current_turn_exp - previous_turn_exp`
- `progress_percent = current_turn_exp / total_exp_for_next_level`

These are deterministic, not semantic — allowed in backend code.


## Connections

- [[ZFCNorthStar]] — architectural principle
- [[ModelComputes]] — complementary pattern
- [[RewardsBox]] — formatted UI structure
- [[PlanningBlock]] — formatted UI structure
- [[RewardsEngineArchitecture]] — rewards_engine.py role
