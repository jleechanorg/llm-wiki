# PR 4 (god-mode contract split) — CodeRabbit review loop pattern

Bead: `rev-pctz8.4`. Worktree: `/Users/jleechan/projects/wt-level-up-session-pr4`. PR [#7376](https://github.com/jleechanorg/worldarchitect.ai/pull/7376).

## Two-call-site defects CR caught on the same PR (heads 1d39614088 + 510e17148f)

When a dispatcher returns a NEW `updated_game_state_dict` (e.g. admin commit
path mutates a deep copy), the caller's local rebind is **not enough** — any
captured reference (lambda, callback, downstream function call bound to the
original dict name) still points to the OLD dict. The mutation is silently
lost when the caller does the next `dict[] = ...` assignment.

**Fix pattern (canonical)**:
```python
(sf, sc, _new_gs, gm_warnings) = _god_mode_level_up_dispatch(...)
if _new_gs is not updated_game_state_dict:
    updated_game_state_dict.clear()
    updated_game_state_dict.update(_new_gs)
```

Mirrors the "single source of truth" guidance from PR 3 (atomic persistence
boundary) — clear-and-update in place keeps the dict's identity stable.

## Two parallel fail-closed paths must stay symmetric

`_god_mode_level_up_dispatch` has THREE failure paths:
- Path A success → returns `new_state_changes` (deep copy + new PCD)
- Path A failure (`except (TypeError, ValueError)`) → returns `cleaned_structured` (level_up_signal + modal choices stripped)
- **Mixed-contract failure** (admin commit + signal/choices, reducer rejected) → also returns `cleaned_structured`

CR caught that branches 2 and 3 had drifted: branch 2 stripped
`level_up_signal`/modal choices from `structured_fields`, branch 3 did not.
Result: a rejected mixed-contract response would still leak a half-built
modal handoff into the API surface.

**Rule**: when introducing a new fail-closed branch in an existing dispatcher,
audit all sibling rejection paths for the same cleanup contract. Drift between
sibling branches is a silent-failure class.

## CR workflow re-review cadence

1. Push fix commit
2. `gh workflow run green-gate.yml -f pr_number=<N> -f head_sha=<SHA>` (BOTH inputs required — `head_sha` alone gives HTTP 422)
3. `gh pr comment <N> --body "@coderabbitai ... please re-review"`
4. Wait for `reviewDecision` to flip from `CHANGES_REQUESTED` → `APPROVED`
5. CR can take 2-5 minutes to re-review; the Green Gate polls for the verdict
6. Don't claim 7-green until `reviewDecision: APPROVED` AND no `ci_fail` AND `ci_pending: 0`

## Reducer-frozen scope boundary

The level-up reducer in `mvp_site/level_up_session.py` is FROZEN after PR 1-3
merge. PR 4 can only CALL into it. CR flagged 3 reducer-internal defects in
the reducer (admin commit int guards, dict-keyed modal choice detection) —
those are explicitly OUT of scope for PR 4 and tracked as follow-up beads.
Don't get drawn into "while I'm here" reducer edits; the teammate assignment
is a hard contract.

## Test fixture invariant: "Inv-3" vs "Inv-9"

In `vnu3_stale_signal/manifest.json`, `expected_invariants` was "Inv-9" but
the test asserts "Inv-3" (canonical for `status=complete` with a leftover
`level_up_signal`). Invariant numbers are case-specific — the stale-signal
test is "Inv-3" not "Inv-9". The fixture drifted from the test; the test is
canonical (asserts on the level_up_session state shape), the fixture is the
description (was updated).

## Phantom rewards_box.level_up_available after admin commit (510e17148f -> 0a3390d098)

After `apply_god_mode_admin_commit()` COMPLETES the session in place, the
model may have ALSO emitted `rewards_box.level_up_available` in the same
turn (it doesn't know the admin commit will close the session). If not
stripped, the canonicalize_rewards persistence path writes a level-up-shaped
rewards_box alongside a `status=complete` session, and the frontend renders
a phantom level-up prompt.

**Fix pattern (canonical)** — small in-place helper that drops the field
and the whole key if it becomes empty:

```python
def _strip_level_up_rewards_box_offer(structured_fields):
    if not isinstance(structured_fields, dict):
        return
    rb = structured_fields.get("rewards_box")
    if not isinstance(rb, dict) or "level_up_available" not in rb:
        return
    rb = {k: v for k, v in rb.items() if k != "level_up_available"}
    if not rb:
        structured_fields.pop("rewards_box", None)
    else:
        structured_fields["rewards_box"] = rb
```

Apply at the end of BOTH Path A success and mixed-contract success branches
(symmetric with the existing level_up_signal / modal-choices strip). Apply
on the deep-copied `new_structured`, not on the original `structured_fields`
input.
