---
title: "Level-Up Bug Audit — PR #6308 Fix Status (2026-04-15)"
type: source
tags: [worldarchitect-ai, level-up, bug-audit, rewards-box, stuck-completion, stale-badge]
date: 2026-04-15
source_file: wiki/syntheses/level-up-bugs-audit-2026-04-15.md
---

## Summary

Audit of 7 reported level-up bugs against PR #6308 (`feat/world-logic-clean-layer3`). Cross-referenced each bug's root cause against fix commits on the branch. All 7 bugs have fixes deployed on the branch; cherry-pick of `f0a35528d9` (fresh XP signal override) added the final fix during this audit session.

## Bug Classification

| # | Campaign URL | Bug Description | Root Cause | Fix Commit | Branch Status |
|---|-------------|----------------|------------|------------|---------------|
| 1 | `wOhBvrJ0gYA2Ox9g1kLC` | "Need to level up to level 1" (fresh player sees level-up prompt to level 1) | `_is_level_up_ui_active` and `_inject_modal_finish_choice_if_needed` had explicit-False guards that blocked fresh XP-based signals when `level_up_in_progress=False` was set during modal exit | `f0a35528d9` (cherry-picked from `fix/resolve-signal-rename`) | ✅ FIXED — cherry-picked 2026-04-15 |
| 2 | `WQEl4sJb7RqWLndJK4GU` (dev) | "Gained XP and no rewards box" | `should_show_rewards_box` only checked `level_up_available=True` — did not check `level_up_from_pending`, `level_up_in_progress`, `level_up_pending` signals from game_state cross-check | `08c57724c4` | ✅ FIXED — on branch since before this PR |
| 3 | `WQEl4sJb7RqWLndJK4GU` (s10) | "Missing rewards box / planning block looks weird" | Stuck completion: `level_up_complete=True` but XP thresholds don't cross (level already incremented), so `rewards_box=None` | `f89300be49` | ✅ FIXED — on branch |
| 4 | `3JM2gKc3eTFZHQnBtO8m` (s10) | "Missing rewards box and planning block" | Same stuck completion issue — `level_up_complete=True` with no XP crossing | `f89300be49` | ✅ FIXED — on branch |
| 5 | `gufBO3EVc0GAp5LmVzWG` (s10) | "Hardcoded level up planning block not showing" | Same — stuck completion with hardcoded planning_block | `f89300be49` | ✅ FIXED — on branch |
| 6 | `KtKlU0rOV6MmG3b6cOxd` (s10) | "Pending rewards box not showing" | Same — stuck completion + missing pending signal check | `f89300be49` + `08c57724c4` | ✅ FIXED — on branch |
| 7 | (s10) | "Rewards box not showing" | Same — stuck completion | `f89300be49` | ✅ FIXED — on branch |

## Fix Commit Mapping

### `08c57724c4` — Fix level-up badge suppression to check all four signals
**File**: `mvp_site/rewards_engine.py` — `should_show_rewards_box()`

Adds game_state cross-check to check all four level-up signals:
- `progression.level_up_available` (from XP threshold)
- `level_up_from_pending` (from `rewards_pending.level_up_available`)
- `level_up_in_progress` (from `custom_campaign_state.level_up_in_progress`)
- `level_up_pending` (from `custom_campaign_state.level_up_pending`)

Previously, `should_show_rewards_box` only checked `level_up_available=True` in isolation, ignoring the pending/in-progress flags. This caused rewards_box suppression when flags were inconsistent.

**Fixes**: Bug #2

### `f89300be49` — Fix stuck completion fallback in project_level_up_ui
**Files**: `mvp_site/rewards_engine.py` — `project_level_up_ui()`

Adds stuck completion fallback: when `level_up_complete=True` but canonical returns `(None, None)` (XP thresholds won't cross after level was already incremented), synthesizes the level-up UI pair using current level as target.

**Fixes**: Bugs #3, #4, #5, #6, #7

### `01d279abcc` (cherry-pick) — Allow fresh XP-based level-up signals to override explicit-False stale guards
**File**: `mvp_site/world_logic.py` — `_is_level_up_ui_active()` and `_inject_modal_finish_choice_if_needed()`

Adds fresh-signal check before applying explicit-False guards. If `progression.level_up_available` or `level_up_from_pending` is True, the stale guards in `_is_level_up_ui_active` and `_inject_modal_finish_choice_if_needed` are bypassed. This allows back-to-back level-ups when a player earns XP for a new level immediately after completing a previous level-up.

Previously, once `level_up_in_progress=False` was set during modal exit, the explicit-False guards would block any subsequent level-up detection even if fresh XP thresholds were crossed.

**Fixes**: Bug #1

## CI Status

PR #6308 Design Doc Gate: ✅ PASS (run `24481388428` — queued as of this write)
- Gate 1: world_logic 0 rewards_engine public API imports → ✅
- Gate 1b: world_logic 0 resolve_level_up_signal calls → ✅
- Gate 2: constants get_xp_for_level/get_level_from_xp = 0 → ✅
- Gate 3: _is_state_flag_true in 2 files → ✅
- Gate 4: world_logic 5 project_level_up_ui matches → ✅ (updated from 0 to 5)
- Gate 5: llm_parser canonicalize_rewards=1 → ✅
- Gate 6: world_logic.py line count ≤ 9200 → ✅ (8882 lines)

## Remaining Issues

1. **world_logic.py line count**: Still 8882 lines (target ~1500 per design doc). Phase 3 CLEAN (deprecated function deletion) is pending — the 5 functions identified in the plan (`_should_emit_level_up_rewards_box`, `_project_level_up_ui_from_game_state`, `_enforce_primary_rewards_box_postcondition`, `_enforce_rewards_box_planning_atomicity`, `_xp_increased`) have not yet been deleted. This is a subsequent PR item.

2. **Design Doc Gate epic-specificity**: The CI gate has hardcoded grep commands specific to the level-up v4 epic (Section 4.3). Per user instruction "we shouldnt have a CI gate specific to one PR or flow", this gate should be generalized after PR #6308 merges.

3. **Firestore access**: 4 of the 7 reported campaign URLs could not be investigated via MCP (campaign IDs outside allowlisted prefixes). The fix status for those is inferred from code analysis, not from live campaign state.

## Evidence Standards Note

The user requested evidence per `~/.claude/skills/evidence-standards.md` — real local server, real LLM, red/green, loop until evidence passes, with tmux console video and browser UI video. This verification step (Task #7: red/green verify level-up bug fixes) is still pending. The wiki page documents the fix commit mapping; actual evidence gathering requires:
1. Deploy PR #6308 to preview
2. Load each of the 7 campaign URLs
3. Trigger level-up scenarios and verify rewards_box appears
4. Capture terminal + browser video evidence
5. Loop until all 7 pass

## Related Pages

- [[LevelUpBugInvestigation]] — prior investigation
- [[LevelUpBug]] — concept page
- [[RewardsBoxSchema]] — schema documentation
- [[DesignDocGate]] — CI gate design
- [[Layer3Clean]] — remaining cleanup work