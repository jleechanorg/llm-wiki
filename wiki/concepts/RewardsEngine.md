---
title: "RewardsEngine"
type: concept
tags: [level-up, rewards-box, rewards-engine, worldarchitect, normalization, canonicalization]
sources: [level-up-v4-current-status-2026-04-14, level-up-v4-semantic-regression-bug, level-up-engine-v4-design]
last_updated: 2026-04-14
---

# RewardsEngine

Single-responsibility rewards computation module in worldarchitect.ai. Replaces scattered rewards logic across `world_logic.py` and `streaming_orchestrator.py`.

## Architecture

**Two entry points converge on `_canonicalize_core`:**

| Function | Path | When |
|---------|------|------|
| `canonicalize_rewards()` | Streaming + Non-streaming | LLM response present |
| `project_level_up_ui()` | Polling only | No LLM output — re-derives from game_state |

## Key Functions

### `_canonicalize_core(raw_rb, raw_pb, game_state_dict, original_state_dict)`

All paths converge here. Steps:
1. `resolve_level_up_signal()` — detect level-up
2. `ensure_rewards_box()` + `ensure_planning_block()` — atomic pair build
3. `normalize_rewards_box()` — clean types
4. `should_show_rewards_box()` — visibility gate
5. `_enforce_atomicity()` — if either is None, both are None

### `should_show_rewards_box(rewards_box) -> bool`

Returns True ONLY when `level_up_available=True`. **Critical semantic**: in v3 (`normalize_rewards_box_for_ui`), XP-progress boxes were emitted even when `level_up_available=False`. v4 changed this — a regression that suppressed all non-level-up XP rewards in production.

### `normalize_rewards_box(rewards_box) -> dict | None`

ONE normalizer. Guarantees clean booleans and coerced ints. Returns None if `rewards_box` is empty/None.

### `resolve_level_up_signal(game_state_dict, raw_rewards_box, original_state_dict) -> (detected, target_level, max_level)`

Detects active level-up from game state flags and XP thresholds.

## CRITICAL BUG: should_show_rewards_box Semantic Regression

**PR #6273** changed `should_show_rewards_box()` to block ALL non-level-up XP progress boxes. The old `normalize_rewards_box_for_ui()` allowed `xp_gained=50, level_up_available=False` boxes through. v4 only emits when `level_up_available=True`.

This caused 4 of 6 production bugs on 2026-04-14. Fix: restore XP-progress visibility or rename the function to reflect its new semantics.

See [[LevelUpCodeArchitecture]] for full regression analysis.

## Key Files

- `mvp_site/rewards_engine.py` — all rewards computation
- `mvp_site/llm_parser.py` — calls `canonicalize_rewards()` (streaming) and `project_level_up_ui()` (polling)

## Related Concepts

- [[LevelUpCodeArchitecture]] — full pipeline architecture
- [[LevelUpPolling]] — polling vs streaming paths
- [[FrontendRewardsBoxGate]] — frontend visibility gate
