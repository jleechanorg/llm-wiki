---
title: "PR 6276 Post-Merge Assessment 2026-04-16 — Layer 3 CLEAN Incomplete"
type: source
tags: [worldarchitect.ai, PR6276, level-up, v4-architecture, design-doc-drift]
date: 2026-04-16
---

## Summary

PR #6276 (`feat/world-logic-clean-layer3`) was merged at commit `6d29d8eeda4c04f73819403596e67063bd5ac6c0` on 2026-04-15 at 16:26 UTC. The core v4 architecture is correct (~85% complete): `llm_parser.py` as single orchestration root, `rewards_engine.py` with full API, `_canonicalize_core()` single-call-site invariant met. However, the design doc's Layer 3 CLEAN goals were NOT fully achieved.

## What Was Delivered

- **`rewards_engine.py`**: New file with full public API (`canonicalize_rewards`, `project_level_up_ui`, `_canonicalize_core`, `resolve_level_up_signal`, `ensure_rewards_box`, `ensure_planning_block`, `normalize_rewards_box`, `should_show_rewards_box`, `is_level_up_active`)
- **`llm_parser.py`**: Renamed from `streaming_orchestrator.py`, single orchestration root for streaming + non-streaming + polling paths
- **world_logic.py**: 0 rewards_engine PUBLIC API imports (deprecation redirects added instead)
- **CI line-count gate**: `world_logic.py line count ≤ 9200` (rev-v4ci04 ✅)
- **design-doc-gate.yml**: 8 CI grep gates added
- **rev-v4ci01 TOMBSTONED**: world_logic.py strip to ~1500 lines declared unachievable

## What Layer 3 CLEAN Required (NOT Done)

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| world_logic.py line count | ~1,500 | ~8,896 | ❌ NOT achieved |
| Delete `_is_state_flag_true` | 3→1 | 3 copies remain | ❌ NOT achieved |
| constants.py XP math deduplication | Remove dupes | Still present | ❌ NOT achieved |
| app.js boolean coercion cleanup | Remove | Still present | ❌ NOT achieved |
| 4 design-doc Layer 2 integration tests | Must exist | rev-v4ci02 says exist but uncertain | ⚠️ Unclear |
| Net negative lines (exit gate) | Negative | Not enforced | ❌ NOT enforced |

## Key Discovery: Design Doc Equivalence Claim Was Wrong

The design doc (`level-up-engine-single-responsibility-design-2026-04-14.md`) claimed **"5 world_logic functions map to rewards_engine equivalents."**

**rev-v4ci05 behavioral equivalence audit proved this FALSE:**
- **0/3 pairs are equivalent** when tested against actual game state
- **Two different philosophies** produce different outputs from the same input:
  - `rewards_engine` approach: XP-threshold/causal — compute from XP values
  - `world_logic` approach: flag-driven/stateful — check persisted flags

**Functions that MUST stay in world_logic:**
1. **Stuck completion synthesis** — world_logic's `_enforce_rewards_box_planning_atomicity` does injection + scrubbing; rewards_engine's `_enforce_atomicity` only does null check
2. **Loot/gold extraction** — 7 extraction functions in world_logic, 0 in rewards_engine; LLM output coupling makes moving impractical
3. **`_should_emit_level_up_rewards_box`** — needs game_state cross-check; rewards_engine's `should_show_rewards_box` only checks rewards_box

## Root Cause: Design Doc Drift

PR #6276 merged with design-doc-gate FAIL because:
1. **Structural grep gates ≠ behavioral verification** — design-doc-gate.yml checks imports and function presence, not whether implementations are equivalent
2. **CI line-count gate added** (rev-v4ci04) but not enforced as exit gate for Layer 3 CLEAN
3. **skeptic-gate skips** PRs with CR=DISMISSED or Bugbot=none without posting VERDICT
4. **Layer 3 CLEAN exit gate** (net negative lines) was never wired to CI

## Current PR States

| PR | Branch | State | mergeStateStatus | Key Issue |
|----|--------|--------|-------------------|-----------|
| #6276 | feat/world-logic-clean-layer3 | **MERGED** | — | ~85% done |
| #6287 | fix/resolve-signal-rename | OPEN | **CLEAN** | skeptic-gate NOT run on current SHA |
| #6285 | fix/claude-md-design-doc-gate-rule | OPEN | UNSTABLE | skeptic-cron not triggered on current SHA |
| #6292 | fix/br-4bk-green-gate-design-doc | OPEN | BLOCKED | CR CHANGES_REQUESTED |
| #6289 | fix/br-4bk-design-doc-skill | OPEN | DIRTY | **OBSOLETE** — target file deleted by #6276 |
| #6308 | feat/world-logic-clean-layer3 | OPEN | DIRTY | 3 extra commits beyond merge base |

## Connections
- [[LevelUpV4Architecture]] — single root pipeline
- [[BehavioralEquivalenceAudit]] — 0/3 pairs equivalent
- [[DesignDocGate]] — 8 CI grep gates
- [[rev-v4ci01]] — TOMBSTONED
- [[rev-v4ci05]] — audit complete
- [[SkepticGate]] — exits 0 with SKIP on CR DISMISSED

## Update 2026-04-16 (mid-day) — CORRECTION

**Previous assessment was WRONG**: I claimed 908b5db7c9 merged into main. **Reality**: 908b5db7c9 is on `origin/feat/world-logic-clean-layer3`, NOT on `origin/main`. The feature branch merged main INTO itself.

- `origin/main` = `6d29d8eeda` (PR #6276 squash-merge) — unchanged
- `origin/feat/world-logic-clean-layer3` = `f89300be49` — 4 commits ahead of main
- PR #6308 is alive, MERGEABLE, head = `f89300be49`

New commits on feature branch (not yet on main):
- `f89300be49` — Fix stuck completion fallback in project_level_up_ui
- `08c57724c4` — Fix level-up badge suppression to check all four signals
- `908b5db7c9` — merge: resolve origin/main conflicts (branch merged main)
- `47b5bae3fb` — chore(beads): add rev-v4ci09
- `0fef3eb2d6` — refactor(world_logic): delete 2 deprecated functions
- `1deb850219` — fix(world_logic): delete dead _xp_increased
- `8b6bd0572f` — fix(ci): correct design-doc-gate for project_level_up_ui count (new commit on feature branch)

## Update 2026-04-16 (current)
- **PR #6285**: CONFLICTING (mergeable=false) — branch out of date with main
- **PR #6287**: UNSTABLE — green-gate queued (24473716915), CI running
- **PR #6289**: CONFLICTING (mergeable=false) — branch out of date with main
- **PR #6308**: BLOCKED + CHANGES_REQUESTED — 5 commits ahead of main, CI fix on branch
