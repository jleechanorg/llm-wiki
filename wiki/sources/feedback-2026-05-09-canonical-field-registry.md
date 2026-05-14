# Canonical Field Registry Anti-Pattern — Never Duplicate Field Sets

**Source:** `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-09_canonical_field_registry_antipattern.md`
**Ingested:** 2026-05-09
**Bead:** rev-gm1ax

## Summary

Local field tuple/set definitions duplicated across files cause NameError on rebase when one copy is updated and another isn't. The fix: a single canonical frozenset imported everywhere.

## Context

`_AUTHORITATIVE_LIVING_WORLD_FIELDS` was defined independently in 4 locations:
1. `firestore_service.py:1451` — canonical frozenset (source of truth)
2. `world_logic.py:7580` — local `_cooldown_lw_fields` tuple
3. `world_logic.py:7831` — local `_cooldown_lw_fields_resp` tuple
4. `structured_fields_utils.py:217` — local inline set

When PR #6839 rebased, a merge conflict on the local tuple caused NameError during cooldown strip.

## Rule

Always import from the canonical source (`mvp_site.firestore_service`). Before defining any field set locally, grep for `_AUTHORITATIVE_` or `_TURN_SCOPED_` — if a canonical source exists, import it.

## Related Concepts

- [[DuplicatedConstantLists]]
