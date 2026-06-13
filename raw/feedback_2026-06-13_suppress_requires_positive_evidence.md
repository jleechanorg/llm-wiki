---
name: suppress-requires-positive-evidence
description: "Stale-flag suppression must require positive evidence of advancement, not absence of data — empty rewards_box fires on valid hybrid CC+LevelUp states"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-jw8e4
  originSessionId: cc529d80-6799-46a8-9cd4-e0efc53d964b
---

## Rule

**Never treat absence of a field as positive evidence of advancement in stale-flag suppression.**

In `_compute_stale_level_up_suppression`, the clause `or (not rewards_box)` was added to handle
the runtime case where `rewards_box` is absent from the `game_states` Firestore document. The
intent was: "if there's no rewards_box, the level-up must be done." This is wrong — absence
means "not written yet," not "already advanced."

## Why

The hybrid CC+LevelUp modal (`level_up_stage="character_creation_approval"`,
`character_creation_in_progress=True`) legitimately has `rewards_box=None` because the level-up
hasn't been processed yet. The `or (not rewards_box)` clause fired on this state, making
`is_level_up_active()` return `False`, which changed the routing path and caused
`level_up_pending` to remain `True` after `finish_character_creation_start_game`.

The test `test_character_creation_finish_clears_hybrid_level_up_approval_flags` passed locally
(semantic routing enabled) but failed in CI (`ENABLE_SEMANTIC_ROUTING=false`) because the routing
path without the classifier depends on `is_level_up_active()` returning the correct value.

**PR**: [#7516](https://github.com/jleechanorg/worldarchitect.ai/pull/7516)
**Fix commit**: `e652898218` — removed `or (not rewards_box)` from `rewards_box_already_advanced`

## How to Apply

- Suppression conditions must require **positive evidence** of the state being "done":
  - ✅ `rewards_box_level > player_level` — the model wrote a higher level into rewards_box
  - ❌ `not rewards_box` — absence is not evidence of completion
- When adding "fallback" suppression for absent fields, ask: "Is this field absent because the
  state is complete, or because the state hasn't started yet?" If ambiguous → require positive evidence.
- Always test suppression conditions with `ENABLE_SEMANTIC_ROUTING=false` to catch routing
  differences that only surface without the classifier.

## Verification

Running with `MOCK_SERVICES_MODE=true ENABLE_SEMANTIC_ROUTING=false`:
- Orphaned CCS test (rev-toavb): PASS (rewards_box.current_level=6 > player_level=5 still fires)
- Hybrid CC test: PASS (rewards_box absent → no suppression → modal exit works)
- 295 total tests pass
