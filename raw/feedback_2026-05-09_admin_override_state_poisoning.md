---
name: Admin Override State Poisoning Pattern
description: God mode/admin actions short-circuit state machines leaving stale modal flags
type: feedback
bead: rev-admin-contract
---

God mode and admin override actions bypass state machine entry/exit protocols. After the override, stale flags (level_up_pending, character_creation_in_progress, combat_active) persist, trapping players in modal loops or skipping required transitions.

**Pattern seen in**: PR #6844 (combat loop from stale combat_state), PR #6842 (CC modal guard missing for god_mode), PR #6825 (stale level-up signal guard).

**Fix direction**: `ADMIN_OVERRIDE_CONTRACTS` dict maps each override action → required post-override invariants. `_validate_post_override_state()` enforces after each override execution.

**Why**: Three separate PRs independently discovered stale-flag bugs caused by admin short-circuits. Without a declarative contract, each override path must be individually audited — a constant source of regressions.

**How to apply**: Before adding any new admin/god_mode action in `world_logic.py`, add an entry to `ADMIN_OVERRIDE_CONTRACTS` and call `_validate_post_override_state()` after the action completes.
