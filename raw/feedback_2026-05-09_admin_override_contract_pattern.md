---
name: Admin override contract pattern — declarative cleanup for bypass paths
description: Reusable pattern for any admin shortcut that bypasses LLM pipeline; contracts dict declares resets/sets/preserves/requires_clean; validated pre/post activation
type: feedback
bead: rev-gm1ax
originSessionId: 16b500e1-a771-4453-b0ce-894c7b015a54
---
When admin shortcuts bypass the LLM → state-transition → cleanup pipeline, they leave orthogonal modal flags dangling (state poisoning). The fix is declarative cleanup contracts — NOT ad-hoc flag clearing at each call site.

**Pattern:**
1. Add entry to `ADMIN_OVERRIDE_CONTRACTS` in `mvp_site/admin_override_contracts.py` declaring what the override `resets`, `sets`, `preserves`, and `requires_clean`
2. Call `validate_pre_override_state(game_state_dict, override_name)` BEFORE activation
3. Call `validate_post_override_state(game_state_dict, override_name)` AFTER state changes
4. Both return violation lists and LOG warnings — they don't raise or modify state
5. Add a parametric test row in `mvp_site/tests/test_state_intersection_matrix.py`

**Why:** PRs #6844 (God Mode Trap), #6842 (CC Modal Trap), #6839 (NameError Cooldown), #6841 (UI Premature Dismissal) — all 4 share the same structural disease: admin overrides without cleanup contracts. Same root cause as 17-day level-up saga (30+ PRs). Downstream guards patch symptoms; contracts prevent the class of bug.

**How to apply:** Before adding any new admin override or shortcut path (god_mode variant, template, quick-start, think_mode, cooldown_strip), FIRST add a contract entry declaring its cleanup obligations. If you can't state what it resets/sets/preserves, the override isn't well-defined enough to ship.

**Wired production paths (Phase 2 complete):**
- `_apply_level_up_entry_state()` — pre + post validation
- `_enforce_modal_lock_and_persistence()` — post validation on level_up_exit + character_creation_exit
- `create_campaign_unified()` prepopulated_template path — post validation
- `_ensure_modal_exclusivity()` — runtime enforcement with priority: level_up > character_creation > combat
