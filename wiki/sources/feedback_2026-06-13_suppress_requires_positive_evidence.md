---
title: "Stale-Flag Suppression Requires Positive Evidence of Advancement"
type: source
tags: [feedback, level-up, suppression, rewards-engine, zfc, worldarchitect, pr-7516]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_suppress_requires_positive_evidence.md
---

## Summary
In `_compute_stale_level_up_suppression`, the clause `or (not rewards_box)` was wrong: absence of a field is not positive evidence of advancement. The hybrid CC+LevelUp modal (`level_up_stage="character_creation_approval"`) legitimately has `rewards_box=None` because the level-up hasn't been processed yet. The `or (not rewards_box)` clause fired on this state, making `is_level_up_active()` return `False`, which changed the routing path and caused `level_up_pending` to remain `True` after `finish_character_creation_start_game`. Fix commit `e652898218` in PR #7516 removed the clause. Suppression conditions must require positive evidence (e.g. `rewards_box_level > player_level`), not absence of data.

## Key Claims
- Never treat absence of a field as positive evidence of advancement in stale-flag suppression
- The test `test_character_creation_finish_clears_hybrid_level_up_approval_flags` passed locally (semantic routing enabled) but failed in CI (`ENABLE_SEMANTIC_ROUTING=false`) — the routing path without the classifier depends on `is_level_up_active()` returning the correct value
- Always test suppression conditions with `ENABLE_SEMANTIC_ROUTING=false` to catch routing differences that only surface without the classifier
- When adding "fallback" suppression for absent fields, ask: "Is this field absent because the state is complete, or because the state hasn't started yet?" If ambiguous → require positive evidence
- Verification: 295 total tests pass with `MOCK_SERVICES_MODE=true ENABLE_SEMANTIC_ROUTING=false`; orphaned CCS test (rev-toavb) PASS; hybrid CC test PASS

## Key Quotes
> "**Never treat absence of a field as positive evidence of advancement in stale-flag suppression.** In `_compute_stale_level_up_suppression`, the clause `or (not rewards_box)` was added to handle the runtime case where `rewards_box` is absent from the `game_states` Firestore document. The intent was: 'if there's no rewards_box, the level-up must be done.' This is wrong — absence means 'not written yet,' not 'already advanced.'"

> "Suppression conditions must require **positive evidence** of the state being 'done': ✅ `rewards_box_level > player_level` — the model wrote a higher level into rewards_box; ❌ `not rewards_box` — absence is not evidence of completion."

## Connections
- [[rewards_engine.py]] — file containing `_compute_stale_level_up_suppression`
- [[PR_7516]] — the PR that contained the fix
- [[HybridCCLevelUpModal]] — the modal that legitimately has `rewards_box=None`
- [[ENABLE_SEMANTIC_ROUTING]] — env flag that masks/uncovers the bug
- [[rev-jw8e4]] — bead for this feedback
- [[rev-toavb]] — orphaned CCS test
- [[ZeroFrameworkCognition]] — broader principle of evidence-based behavior
- [[RootCauseFirstEngineering]] — principle that backend logic should require positive evidence
