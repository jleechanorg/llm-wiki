---
name: PR 6844 Root Cause — God Mode Combat Trap
description: God mode left stale combat_state because no cleanup path existed when Combat Mode was introduced
type: feedback
bead: rev-kpm5u
---

PR #6844: God Mode turns bypass combat resolution but never clear `in_combat=True` / `combat_phase=active`. This permanently routes to CombatAgent (priority 5c) instead of StoryMode.

**Breaking PR**: #3020 (God Mode level-up) and #2553 (Combat Mode agent). The architectural gap existed from the initial intersection — there was never a backend safety net to force-clear combat state when entering God Mode.

**Lesson**: When adding a new modal/agent that bypasses existing state machines, the override path MUST clear all competing modal flags. This is exactly what `ADMIN_OVERRIDE_CONTRACTS` (bead `rev-kpm5u`) is designed to enforce.

**How to apply**: Every new `god_mode_*` path in `world_logic.py` must call `_validate_post_override_state()` which asserts that competing modal flags (combat, CC, level-up) are cleared.

**Verification**: PR #6844 adds `test_god_mode_combat_trap_end2end.py` (147 LOC). Test proves the fix by simulating God Mode turn during active combat and asserting combat flags are cleared.
