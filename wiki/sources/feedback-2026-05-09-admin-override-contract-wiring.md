# Admin Override Contract Wiring — Phase 2 Production Integration

**Source:** `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-09_admin_override_contract_pattern.md`
**Ingested:** 2026-05-09
**Bead:** rev-gm1ax

## Summary

When admin shortcuts bypass the LLM pipeline, they leave orthogonal modal flags dangling (state poisoning). The fix is declarative cleanup contracts — NOT ad-hoc flag clearing at each call site.

## Pattern

1. Add entry to `ADMIN_OVERRIDE_CONTRACTS` in `admin_override_contracts.py`
2. Call `validate_pre_override_state()` BEFORE activation
3. Call `validate_post_override_state()` AFTER state changes
4. Both return violation lists and LOG warnings — they don't raise or modify state
5. Add a parametric test row in `test_state_intersection_matrix.py`

## Wired Production Paths (Phase 2)

- `_apply_level_up_entry_state()` — pre + post validation
- `_enforce_modal_lock_and_persistence()` — post validation on level_up_exit + character_creation_exit
- `create_campaign_unified()` prepopulated_template path — post validation
- `_ensure_modal_exclusivity()` — runtime enforcement with priority: level_up > character_creation > combat

## Related Concepts

- [[AdminOverrideContract]]
- [[ModalIntersection]]
