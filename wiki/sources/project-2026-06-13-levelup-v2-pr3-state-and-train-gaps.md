---
title: "2026-06-13 Levelup V2 Pr3 State And Train Gaps"
type: source
tags: ["project", "worldarchitect", "level-up"]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_v2_pr3_state_and_train_gaps.md
---

## Summary
Level-up v2 PR-3 (#7530 rewards_engine shim) landed + two systemic train-level gaps that block organic routing

## Key Claims
- PR-3 = #7530, branch feat/levelup-v2-rewards-engine, head ee0a67e16a (2026-06-13). The branch is STACKED (contains PR-1's level_up_session.py + schema + 4 test files, not just rewards_engine).
- - v2 shim contract green: test file is `test_rewards_engine_v2_shim.py` (NOT test_levelup_rewards_v2.py as the goal stated), 14/14.
- - Bug fix `d12bee21ce`: `_canonicalize_core` had TWO `canonical_signal` promotion sites with inconsistent gates — the later (overwriting) one at ~line 2783 still required `planning_supports_level_up`; after the shim removed server planning synthesis (`format_model_level_up_signal` returns `(rb, None)`), that gate was always False for signal-only inputs → canonical_signal cleared → `apply_model_level_up_signal` reducer never ran → no session landed (the half-write bug). Fixed to gate on model signal + `not false_positive_detected` (matches the earlier site at ~2682). Independent ZFC review PASS.
- - Test cleanup `ee0a67e16a`: 29 obsolete tests retired across test_rewards_engine{,_wiring,_stale_flag}.py — 15 deleted (legacy flag-OR/XP-threshold activation), 14 rewritten to v2 (activate via level_up_session.review_open; assert planning_block None). All 4 rewards_engine test files green (323 passed).
- 1. **review_open not wired into organic flow** — seam (canonicalize_rewards → apply_model_level_up_signal) creates a STATUS-based session (`status="available"`), but v2 routing predicate `is_review_open` only checks `review_open is True`. `apply_level_up` (sets review_open=True, level_up_session.py:205) is NOT called organically. So after a model level-up, is_level_up_active=False → routing does NOT fire in production. Owner: organic-co-write PR (the one [[project_2026-06-13_levelup_v2_execution_spec_audit]] says "doesn't exist yet"). project_legacy_level_up_fields DOES handle both status- and review_open-based sessions (display works), only routing predicate is review_open-only.
- 2. **Server-side rewards_box⟺planning_block atomicity RETIRED** — v2 format returns (rb, None); atomicity is now the model's job. `test_canonicalize_invariants.py` (bead rev-9lge) + `test_bug_rewards_box_atomicity.py` still assert the old server-enforced guarantee and fail. Retiring that documented "fundamental guarantee" needs explicit sign-off — left untouched.

## Connections
- [[feedback_2026-06-13_design_doc_gate0_artifact_inside_tenets]]
- [[project_2026-06-13_levelup_v2_execution_spec_audit]]
