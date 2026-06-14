---
title: "Project 2026 06 11 Level Up 2To3 Routing Real Root Cause"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_level_up_2to3_routing_real_root_cause.md
---

## Summary

**Symptom**: `testing_mcp/core/test_level_up_organic.py` (multi_level_organic_progression) reports `Expected to finish at level 3, got level 2` for the 2→3 transition. Also: 4× `level-up non-finish turn advanced story/world state` failures. **Not** a bad prompt.

## Original

# Level-up 2→3 finish turn routing root cause (2026-06-11)

**Symptom**: `testing_mcp/core/test_level_up_organic.py` (multi_level_organic_progression) reports `Expected to finish at level 3, got level 2` for the 2→3 transition. Also: 4× `level-up non-finish turn advanced story/world state` failures.

**Not** a bad prompt. The LLM is correctly following the schema and writing the canonical `level_up_session.status="in_progress"` (top-level). The schema correctly marks `custom_campaign_state.level_up_in_progress` as `"deprecated": true` (see server.log:565 — full JSON schema emitted in the system prompt chunk). The LLM obeys the deprecation and does NOT write the legacy field.

But the backend reads the LEGACY field. Result: routing thinks the modal is inactive, falls through to `CombatAgent`, the level mutation gets reverted by `block_unauthorized_level_mutations`, final state = level 2.

**The 1→2 modal works** because the LLM happens to set both canonical AND legacy fields there. The 2→3 modal fails because it only sets the canonical field.

## Code locations — 4 backend paths read the legacy field

| Path | File:line | Status | Notes |
|------|-----------|--------|-------|
| Modal lock routing | `mvp_site/agents.py:3329-3355` | **FIXED at d766ae177e** | Added `canonical_session_active = rewards_engine.is_session_active(game_state)` to the modal active check |
| Modal state filter (top-level level_up_session preserved across non-finish turns) | `mvp_site/world_logic.py:2261+` (`_filter_level_up_non_finish_state_changes`) | **FIXED at d766ae177e** | Added canonical_session preservation |
| Time-freeze context | `mvp_site/world_logic.py:3267` (`_is_level_up_time_freeze_context`) | **NOT FIXED** | Reads `custom.level_up_in_progress`, `custom.level_up_pending`, `custom.character_creation_stage`, planning_block. Source of 4× "non-finish turn advanced story/world state" failures. Mirror routing fix. |
| Mutation safety net | `mvp_site/rewards_engine.py:1016-1053` (`block_unauthorized_level_mutations`) | **NOT FIXED** | `_LEVEL_MUTATION_AUTHORIZED_MODES = {MODE_LEVEL_UP, MODE_GOD, MODE_CHARACTER_CREATION}`. Needs to also accept when canonical session is active. Source of `UNAUTHORIZED_LEVEL_MUTATION: Agent mode 'combat' attempted to change level from 2 to 3. Reverting.` in v3 server.log:212139. |

## The inlined `is_session_active` 

`mvp_site/level_up_session.py` (canonical reducer) was **deleted in PR #7447** (MERGED 2026-06-11). The function was re-inlined in `mvp_site/rewards_engine.py` (post-d766ae177e) as a pure-function status check:

```python
_LEVEL_UP_SESSION_ACTIVE_STATUSES = frozenset(
    {"available", "in_progress", "committing", "error"}
)

def is_session_active(game_state: Any) -> bool:
    if not isinstance(game_state, dict):
        return False
    session = game_state.get("level_up_session")
    if not isinstance(session, dict) or not session:
        return False
    return session.get("status") in _LEVEL_UP_SESSION_ACTIVE_STATUSES
```

This is the canonical signal the backend should consult everywhere. **Use this in items 2 and 3 of the work queue.**

## Evidence (v3, pre-fix)

- Branch: `fix/level-up-daily-cron-combined` (commit `317189350c`)
- Path: `/tmp/worldarchitect.ai/fix_level-up-daily-cron-combined/multi_level_organic_progression_v3/iteration_001/`
- 8 failures in doctor_report.json
- server.log shows 0× `MODAL_LOCK: LevelUpAgent locked` for the 2→3 modal
- The 1→2 modal had 4× `MODAL_LOCK: LevelUpAgent locked` (worked)
- 2→3 finish turn (server.log:212139): `UNAUTHORIZED_LEVEL_MUTATION: Agent mode 'combat' attempted to change level from 2 to 3. Reverting.`

## Evidence (v4, in-flight at handoff time)

- Branch: `fix/level-up-modal-turn-revert` (commit `d766ae177e`)
- PID: 7919 (still running at 14:38 elapsed when handoff was written)
- Path: `/tmp/worldarchitect.ai/fix_level-up-modal-turn-revert/multi_level_organic_progression_v4/iteration_001/` (will appear when test finishes)

**Why:** the 2→3 modal failure was mis-attributed to "prompt" by multiple agents because the LLM response text looked correct. The actual failure was the agent routing layer's stale-flag read — a backend bug masquerading as a prompt issue.

**How to apply:** whenever a canonical field deprecates a legacy field, audit EVERY backend reader of the legacy field. Schema changes propagate down to readers, not just writers. The canonical session-active signal must propagate through all 4 paths above before the 2→3 finish turn can land cleanly.
