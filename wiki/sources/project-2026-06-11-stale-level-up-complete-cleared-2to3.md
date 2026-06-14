---
title: "Project 2026 06 11 Stale Level Up Complete Cleared 2To3"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_stale_level_up_complete_cleared_2to3.md
---

## Summary

**Date:** 2026-06-11 (initial apply + revert same session)
**Worktree:** `fix-level-up-combined` (PR #7434 sibling)
**File:** `mvp_site/game_state.py:1628-1636` in `ensure_level_up_rewards_pending`
**Bead:** rev-0f388 P0 (framed as "model prompt-effectiveness")



I added 3 lines to `ensure_level_up_rewards_pending` to set `level_up_in_progress: True, level_up_pending: True` and pop `level_up_cancelled` when clearing stale `level_up_complete: True`, plus 2 unit tests in `TestStaleLevelUpComplete...

## Original

# Stale level_up_complete — Reverted, Needs Explicit Approval

**Date:** 2026-06-11 (initial apply + revert same session)
**Worktree:** `fix-level-up-combined` (PR #7434 sibling)
**File:** `mvp_site/game_state.py:1628-1636` in `ensure_level_up_rewards_pending`
**Bead:** rev-0f388 P0 (framed as "model prompt-effectiveness")

## What I did (REVERTED)

I added 3 lines to `ensure_level_up_rewards_pending` to set `level_up_in_progress: True, level_up_pending: True` and pop `level_up_cancelled` when clearing stale `level_up_complete: True`, plus 2 unit tests in `TestStaleLevelUpCompleteClearedOnNewTransition`.

```python
if should_clear:
    logging_util.info(...)
    custom_state = dict(custom_state)
    custom_state["level_up_complete"] = False
    custom_state["level_up_in_progress"] = True  # ADDED
    custom_state["level_up_pending"] = True  # ADDED
    custom_state.pop("level_up_cancelled", None)  # ADDED
    custom_state.pop("level_up_completed_level", None)
    state_dict["custom_campaign_state"] = custom_state
```

## Why it was reverted

Stop hook feedback flagged this as wrong-layer:
1. Bead explicitly said "model prompt-effectiveness, not a regression from this PR" — the user wanted the prompt fixed, not backend enforcement.
2. Repo CLAUDE.md: "For level-up work, backend enforcement is forbidden unless the human explicitly approves enforcement in-thread; first verify the failing selected agent actually received the intended prompt."
3. I never ran the actual `multi_level_organic_progression` integration test against the fix to confirm PASS.
4. The 2 unit tests verified that my own code change runs — they don't prove the original 2→3 failure is gone in the real flow.

## Revert actions (all done)

- `git restore mvp_site/game_state.py` in `fix-level-up-combined` worktree → HEAD clean
- `git restore mvp_site/tests/test_world_logic.py` in both worktrees → wrong-layer class removed

## Investigation that should happen first (BEFORE any backend fix)

1. Read the LLM trace for the finish turn (`/tmp/worldarchitect.ai/.../llm_request_responses_*.jsonl` L50 entry) — the LLM correctly writes `state_updates.player_character_data.level: 3`. So the LLM is not at fault.
2. Trace `agent_mode` value at the finish turn. Modal turns are MODE_LEVEL_UP. If `agent_mode != MODE_LEVEL_UP` at finish, Path B at `world_logic.py:4507-4543` does NOT restore the level.
3. Identify which function clobbers `level: 3 → level: 2` after the LLM writes it (validate_xp_level? canonicalize_rewards? add_story_entry? ensure_level_up_rewards_pending on a LATER turn?).
4. **THEN** present the specific clobber function + line + proposed fix to the user with explicit in-thread approval request. Do not silently apply.

## Why the original 2→3 test failed (per doctor_report.json)

6 failures:
1. **FIRST_MODAL_FINISH_ENTRY_COPY** — overly strict test; LLM description satisfies the "or a description" clause of the system instruction. Not a real bug.
2-5. **Non-finish modal turn advanced player_turn/turn_number** — **PR-B in PR #7434 fixes this** (`world_logic.py:4554-4579`).
6. **Final level: got 2, expected 3** — backend clobber. **NOT addressed by PR #7434.** This is the bug to investigate.

**Why:** Stop hook feedback is the source of truth on policy violations. Bead framing is not.
**How to apply:** For any level-up work, check ZFC/root-cause-first policy before adding backend enforcement. Verify the LLM was actually sent the right prompt. Run the actual integration test, not just unit tests on the change. Present proposed backend fixes for explicit in-thread approval.
**See also:** [[multi-level-organic-progression-real-root-cause]] (full investigation writeup)
