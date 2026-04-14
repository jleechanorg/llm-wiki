---
title: "WorldArchitect Level-Up Beads"
type: source
tags: [beads, level-up, worldarchitect, implementation, testing, epic]
sources: []
last_updated: 2026-04-14
---

## Summary

Current implementation of the level-up v4 design is tracked across 5 open beads in worldarchitect.ai. The epic bead `rev-v4eng` coordinates all sub-tasks. Property-based tests and architectural tests are mandatory per v4 design.

## Open Beads

### rev-v4eng — Level-Up v4 Implementation Epic
**Status:** In progress
**Bead:** `rev-v4eng`
**Type:** Epic

Top-level epic coordinating the v4 single-root rewards engine implementation. Supersedes all 4 PRs (#6262, #6263, #6264, #6268) with a clean rewrite.

Key sub-beads:
- `rev-v4t0` — Layer 0: RED contract tests
- `rev-v4t1` — Layer 1: GREEN pure functions
- `rev-v4t2` — Layer 2: WIRE integration
- `rev-v4t3` — Layer 3: CLEAN deletion
- `bd-9ndvc` — v4 design finalization

### jleechan-7tas — Property-Based Tests (XP overflow, DNC coercion, ASI)
**Status:** Open
**Bead:** `jleechan-7tas`
**Created:** 2026-04-14

Mandatory property-based tests for the rewards engine:
- `test_xp_never_overflows_level_20` — XP in range 0-500000 must always produce level 1-20
- `test_normalize_coerces_all_formats` — DNC: `"true"/"1"/true → True`, `"false"/"0"/false → False`, `"500" → 500`
- `test_asi_levels_fighter_includes_6` — Fighter gets ASI at level 6 (not just 4/8/12/16/19)
- `test_asi_levels_rogue_includes_10` — Rogue gets ASI at level 10
- Sentinel test: `normalize_rewards_box({}) is None`

### jleechan-20z1 — Architectural Tests (world_logic layer constraint)
**Status:** Open
**Bead:** `jleechan-20z1`
**Created:** 2026-04-14

Mandatory architectural tests to enforce layer constraints:
```python
def test_world_logic_does_not_import_game_state():
    import world_logic
    assert 'game_state' not in dir(world_logic)

def test_world_logic_does_not_import_rewards_engine():
    import world_logic
    assert 'rewards_engine' not in dir(world_logic)
```

These tests prevent world_logic.py from accumulating orchestration logic (the v4 anti-pattern).

### jleechan-xvrx — v4 Implementation
**Status:** Open
**Bead:** `jleechan-xvrx`
**Created:** 2026-04-14

The main implementation bead. References:
- Design doc: `~/roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`
- Analysis: `~/roadmap/level_up_second_opinion.md`

Key design decisions:
1. `llm_parser.py` is ONE entry point for streaming + non-streaming + polling
2. `rewards_engine.py` owns all rewards decisions (canonicalize_rewards + project_level_up_ui)
3. `world_logic.py` is thin modal wrapper only (no orchestration)
4. Double-touch bug eliminated — canonicalize once before persist + response
5. `rewards_engine` must be IDEMPOTENT for polling clients

### jleechan-bwmj — Close 4 Overlapping PRs
**Status:** Open
**Bead:** `jleechan-bwmj`
**Created:** 2026-04-14

Strategy: close PRs #6262, #6263, #6264, #6268. Cherry-pick test files only. One clean rewrite on `feat/rewards-engine-single-responsibility`.

Rationale: All 4 PRs share the same root bugs (off-by-one in stuck-completion, wrong dict keys, dead ensure_level_up_planning_block, missing freeze_time). PR #6268 patches code that #6264 deletes. Merge sequence is fragile.

### jleechan-9ej1 — Option B Implementation
**Status:** Open
**Bead:** `jleechan-9ej1`
**Created:** 2026-04-14

One clean rewrite following Option B from the design review. Implements `level_up_engine.py` with the 8-function public API design.

## Closed/PR Beads

### rev-v4s1 through rev-v4s8 (Deprecated)
**Beads:** `rev-v4s1`-`rev-v4s8`
**Status:** Superseded

Original 8-step sequential implementation order. Replaced by 4-layer TDD approach (rev-v4t0-t3).

## Design Documents

| Document | Path |
|----------|------|
| v4 Design | `~/roadmap/level-up-engine-single-responsibility-design-2026-04-14.md` |
| v4 Analysis | `~/roadmap/level_up_second_opinion.md` |
| Secondo Analysis | `/tmp/secondo_levelup_analysis.md` |
| Research Analysis | `/tmp/research_levelup_full.md` |

## Connections

- [[LevelUpCodeArchitecture]] — v4 architecture overview
- [[LevelUpPolling]] — Polling pattern and the 3 paths
- [[DeferredRewardsProtocol]] — LLM-driven deferred rewards
- [[RewardsBoxAtomicity]] — rewards_box and planning_block consistency
