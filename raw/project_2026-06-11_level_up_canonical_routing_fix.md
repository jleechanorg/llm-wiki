---
name: level-up-canonical-routing-fix
description: "Multi-level 2→3 regression fixed at routing layer — modal lock at agents.py:3351-3358 now consults canonical level_up_session (NOT just legacy custom_campaign_state.level_up_* flags). LLM correctly wrote level:3, routing picked CombatAgent, block_unauthorized_level_mutations reverted."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2a383e2c-90a3-49e7-ba3a-2d3b68ec68b5
---

# Level-Up Canonical Session Routing Fix (2→3 multi-level)

**Date:** 2026-06-11
**Worktree:** `fix-level-up-combined` (PR #7434 sibling)
**Commit:** `317189350c` on `fix/level-up-daily-cron-combined`
**Files:** `mvp_site/agents.py:3348-3362`, `mvp_site/rewards_engine.py:44,279-288`, `mvp_site/world_logic.py:2266-2301`, `mvp_site/tests/test_level_up_canonical_routing.py` (8 new tests)

## Root Cause

The `multi_level_organic_progression` daily-cron RED "Expected to finish at level 3, got level 2" was caused by routing state-machine drift, NOT a ZFC enforcement violation. Timeline from server log:

1. **Turn N (1→2 modal finish)**: `level_up_complete=true` set, modal exit clears the session
2. **Turn N+1..N+5 (combat continues, XP builds to 918)**: legacy `level_up_complete=true` is stale
3. **Turn N+6 (2→3 modal entry)**: LLM emits `state_updates.level_up_session={status: in_progress, target_level: 3, current_level: 2}` AND `custom_campaign_state.level_up_in_progress=true`. Routing picked `agent_mode='combat'`. Modal envelope **stripped** the `level_up_session` field (server log: "suppressed non-finish state updates: ['level_up_session', 'world_data']") and **reverted** the `level_up_in_progress` mutation ("UNAUTHORIZED_LEVEL_UP_IN_PROGRESS_CCS_MUTATION: Agent mode 'combat' attempted to change level_up_in_progress in custom_campaign_state from False to True. Reverting.")
4. **Turn N+7 (2→3 modal finish)**: LLM correctly wrote `state_updates.player_character_data.level=3` in `finalize_level_up` response. But routing STILL picked `agent_mode='combat'` (server log line 189619: "UNAUTHORIZED_LEVEL_MUTATION: Agent mode 'combat' attempted to change level from 2 to 3. Reverting."). The modal lock at `agents.py:3351-3358` did NOT fire.

## The Fix (3 minimal changes)

This is a **state-machine read** fix, not a ZFC enforcement violation. The LLM wrote `level: 3` correctly; the routing picked the wrong agent because the modal lock only consulted the **legacy** `custom_campaign_state.level_up_*` flags. Per the schema:
- `level_up_session` is the authoritative current-state machine
- `custom_campaign_state.level_up_*` are DEPRECATED derived outputs

### 1. `mvp_site/rewards_engine.py` — re-export `is_session_active()`
```python
from mvp_site.level_up_session import (
    ...
    is_session_active as _is_session_active,
)

def is_session_active(game_state: Any) -> bool:
    """Re-export of the canonical level_up_session session-active check.
    ...
    """
    return _is_session_active(game_state)
```

### 2. `mvp_site/agents.py:3348-3362` — modal lock fires on canonical session
```python
canonical_session_active = rewards_engine.is_session_active(game_state)
level_up_modal_active = (
    level_up_in_progress
    or pending_level_up_transition
    or canonical_session_active  # NEW
    or (
        level_up_pending_flag
        and not rewards_engine.is_stale_level_up_pending(game_state)
    )
)
```

### 3. `mvp_site/world_logic.py:_filter_level_up_non_finish_state_changes` — preserve canonical session
The modal envelope was STRIPPING `level_up_session` from non-finish turn state_changes. Now it preserves the top-level `level_up_session` field so the next routing decision sees the active session.

## Test Coverage

`mvp_site/tests/test_level_up_canonical_routing.py` (8 tests, all passing):
- `test_canonical_session_active_function` — direct helper
- `test_canonical_session_absent_returns_false` — None session
- `test_canonical_session_complete_returns_false` — terminal status
- `test_canonical_session_cancelled_returns_false` — terminal status
- `test_canonical_session_available_returns_true` — pre-modal offer
- `test_canonical_session_committing_returns_true` — finalize phase
- `test_envelope_preserves_top_level_session` — modal envelope fix
- `test_envelope_drops_empty_session` — defensive

End-to-end routing test (`test_get_agent_for_input_with_active_canonical_session`) is skipped in unit env because it requires a live GameState object — would run in `testing_mcp/core/test_level_up_organic.py` integration.

Full modal + world_logic suite: **419 passed, 13 skipped, 0 failed**. PR-B tests (`test_level_up_modal_turn_revert.py`) still pass — fix is compatible with the player_turn/turn_number revert on non-finish level-up turns.

## Why this is NOT a ZFC enforcement violation

Per CLAUDE.md: "backend enforcement is forbidden unless the human explicitly approves enforcement in-thread; first verify the failing selected agent actually received the intended prompt."

This is NOT enforcement — the LLM correctly wrote `level: 3` in state_updates. The bug was that routing picked the wrong agent (CombatAgent) and the SAFETY NET (`block_unauthorized_level_mutations`) reverted the legitimate level write. The fix routes to the correct agent (LevelUpAgent), which has the authority to commit level changes per the schema's `MODE_LEVEL_UP` design.

This is a **routing state-machine fix** — consulting the canonical `level_up_session.status` to decide which agent to invoke. The LLM still owns the decision of WHAT value to write; the routing just needs to pick the right agent that has authority to commit it.

## Related Memory
- [[multi-level-organic-progression-real-root-cause]] — earlier investigation, wrong framing
- [[stale-level-up-complete-cleared-2to3]] — earlier (reverted) backend enforcement attempt that Stop hook caught as wrong-layer
- [[NFBaxQ3mIUe17UlAAGlE level 5/6 bug]] — LLM prompt defect, NOT backend override (different class of bug)

## How to apply

For ANY level-up routing issue:
1. Check if the routing picked the right agent (`LevelUpAgent` vs `CombatAgent`)
2. If the LLM wrote the right value but routing picked the wrong agent, the fix is in the **modal lock** (consulting canonical state), NOT in `block_unauthorized_level_mutations` (which is the safety net that reverts wrong-agent writes)
3. The canonical state is `level_up_session.status` (not the legacy `custom_campaign_state.level_up_*` flags)
4. Modal envelope `_filter_level_up_non_finish_state_changes` must preserve the top-level `level_up_session` for cross-turn routing
