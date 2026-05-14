---
name: Canonical field registry anti-pattern — never duplicate field sets locally
description: Local field tuple/set definitions duplicated across files cause NameError on rebase; single canonical frozenset imported everywhere is the fix
type: feedback
bead: rev-gm1ax
originSessionId: 16b500e1-a771-4453-b0ce-894c7b015a54
---
Never define a local tuple/set of field names when a canonical frozenset exists elsewhere. Duplicated field definitions cause NameError on rebase when one copy is updated and another isn't.

**Why:** `_AUTHORITATIVE_LIVING_WORLD_FIELDS` was defined in 3 independent locations:
1. `firestore_service.py:1451` — canonical frozenset (source of truth)
2. `world_logic.py:7580` — local `_cooldown_lw_fields` tuple
3. `world_logic.py:7831` — local `_cooldown_lw_fields_resp` tuple
4. `structured_fields_utils.py:217` — local inline set

When PR #6839 rebased, a merge conflict on the local tuple caused NameError during cooldown strip.

**How to apply:**
- `_AUTHORITATIVE_LIVING_WORLD_FIELDS` — always import from `mvp_site.firestore_service`
- `_TURN_SCOPED_LIVING_WORLD_FIELDS` — always import from `mvp_site.firestore_service`
- Before defining any field set locally, grep for `_AUTHORITATIVE_` or `_TURN_SCOPED_` — if a canonical source exists, import it
- After fixing: `grep -rn "_cooldown_lw_fields" mvp_site/world_logic.py` should return 0 local definitions
- Verification: `python -c "from mvp_site import world_logic"` must succeed

**Fixed files:**
- `mvp_site/world_logic.py` — both local tuples replaced with canonical import
- `mvp_site/structured_fields_utils.py` — local `allowed_keys` set replaced with `_AUTHORITATIVE_LIVING_WORLD_FIELDS`

**Phase 3 TODO:** CI lint check that `_AUTHORITATIVE_*` and `_TURN_SCOPED_*` must be imported, not locally defined.
