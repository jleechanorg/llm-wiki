# Harness Fix PRs — Status 2026-04-16 Late

## PR #6276 — MERGED (2026-04-15 16:26 UTC)
- **Branch**: `feat/world-logic-clean-layer3`
- **Status**: MERGED
- **What shipped**: rewards_engine.py (new), llm_parser.py (streaming orchestrator renamed), world_logic.py (deprecated wrappers), design-doc-gate.yml (8 CI grep gates), CI line-count gate ≤9200
- **Layer 3 CLEAN incomplete**:
  - world_logic.py line count: 8896 lines (target ~1,500 — NOT achieved)
  - 3 `_is_state_flag_true` copies remain (target 1)
  - constants.py XP math deduplication still present
  - 4 design-doc Layer 2 integration tests missing

## rev-v4ci01 — TOMBSTONED
world_logic.py strip from ~8896 lines to ~1500 lines is unachievable as designed. The deprecated wrapper functions MUST stay (they redirect to rewards_engine, maintaining backward compat).

## rev-v4ci05 — Behavioral Equivalence Audit
Design doc claimed "5 world_logic functions map to rewards_engine equivalents." **FALSE — 0/3 tested pairs are equivalent.**

| world_logic function | rewards_engine equivalent | Gap |
|---|---|---|
| `_should_emit_level_up_rewards_box` | `should_show_rewards_box` | world_logic checks `game_state` cross-referencing; rewards_engine only checks `rewards_box` |
| `_enforce_rewards_box_planning_atomicity` | `_enforce_atomicity` | world_logic does injection + scrubbing; rewards_engine only does null check |
| `_project_level_up_ui_from_game_state` | `project_level_up_ui` | Return type mismatch — different return contract |

**3 behavioral gaps must be resolved before redirecting world_logic call sites.**

## PR #6287 — DISMISSED CR → Substantive Fix Pushed
- **Branch**: `fix/resolve-signal-rename`
- **CR State**: DISMISSED x5 → substantive commits pushed
- **Commits pushed**:
  - `5c1875808d`: `_infer_level_up_target_from_xp` now uses rewards_box param as fallback (was `del rewards_box`)
  - `2495b7d265`: docstring update for `_infer_level_up_target_from_xp`
- **Bug fixed**: `del rewards_box` discarded parameter — now uses `rewards_box.get("resolved_target_level")` as fallback
- **Bug fixed**: `_should_emit_level_up_rewards_box` returned `True` for invalid rewards_box → now returns `False`
- **Status**: OPEN, mergeStateStatus UNSTABLE

## PR #6289 — CHANGES_REQUESTED
- **Branch**: `fix/br-4bk-design-doc-skill`
- **CR State**: CHANGES_REQUESTED x2
- **coder-1 fixes pushed** (`f2a9e008da`):
  1. `_resolve_level_up_signal` guard fix: `and not level_up_in_progress` → `_is_state_flag_false(level_up_in_progress_raw)`
  2. KeyError fix: `planning_block["choices"]` → `planning_block.get("choices")`
  3. `_enforce_rewards_box_planning_atomicity`: check `progression.level_up_available` directly before suppressing
  4. isinstance guards at lines ~7074 and ~7804
- **Status**: OPEN, mergeStateStatus BLOCKED

## PR #6308 — CHANGES_REQUESTED
- **Branch**: `feat/world-logic-clean-layer3`
- **CR State**: CHANGES_REQUESTED x5 (27 open items)
- **Critical fix pushed** (`e53d38816f`):
  - `skeptic-evaluate.sh`: `gh pr merge` removed → posts "merge-ready" comment instead
  - Per repo policy: no agent may call `gh pr merge` without explicit human MERGE_APPROVED
- **CRITICAL items remaining**: agents.py `_is_stale_level_up_pending` semantic inversion
- **Major items**: rewards_engine stale badge suppression, world_logic stuck completion issues, 20+ test file items
- **Status**: OPEN, mergeStateStatus BLOCKED

## PR #6328 — No CR Yet
- **Branch**: `feat/design-doc-as-contract-skill`
- **CR State**: None
- **Status**: OPEN, mergeStateStatus UNSTABLE
- **Blocker**: 0 runners, CI stuck

## Infrastructure Blocker — 0 Runners
- **Issue**: 0 self-hosted runners online
- **Impact**: All CI (green-gate, skeptic-gate) queued indefinitely
- **Bead**: br-pz6tp (P1)

## Team Status
- coder-1: tasks 6 and 8 complete
- task 7 (PR #6308 remaining CR items): in progress
