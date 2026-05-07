# Level-Up 5-Class Bug Fix Verification — 2026-05-04

**Date**: 2026-05-04
**Commit**: `733a44f186a7ce51e00abee76155c47a689e7ffb`
**Branch**: `dev1777883676` (created after `/integrate` from 733a44f18)

## Summary

Ran the original 5 level-up bug repro tests (`./testing_mcp/run_level_up_class_repro_suite.sh`) on `origin/main` at commit 733a44f1. All 5 exited 0 with real Firebase + real Gemini + streaming path.

## Bug Fix Map

| Class | Bug | Fix Commit(s) | Key Mechanism |
|-------|-----|---------------|---------------|
| 1 | Stale `lua=True` modal lockout | `29a8e1f70`, `fd2ae7770` | `game_state_dict` precedence over `structured_fields` in modal detection |
| 2 | Story entry projection strip | `220a87eb0`, `6926ad40a` | Projection projects canonical UI when `level_up_pending=True` |
| 3 | Narrative XP desync | `58098933a` | `_raw_rewards_box_looks_like_stale_echo()` returns `False` when `xp_delta is None` |
| 4 | Historical Firestore residue | `2542e16f6` | `_scrub_stale_story_level_up_entry` at projection; new writes clean |
| 5 | Signal resolver cascade | `3ca0875bd` | `is_level_up_active()` checks `_has_unapplied_xp_threshold_crossing()` bypass |

## Evidence Bundles

- `/tmp/worldarchitect.ai/origin_main/level_up_class_1_stale_flag_lockout/iteration_001/`
- `/tmp/worldarchitect.ai/origin_main/level_up_class_2_story_entry_projection_strip/iteration_001/`
- `/tmp/worldarchitect.ai/origin_main/level_up_class_3_narrative_xp_desync/iteration_001/`
- `/tmp/worldarchitect.ai/origin_main/level_up_class_4_historical_residue/iteration_001/`
- `/tmp/worldarchitect.ai/origin_main/level_up_class_5_signal_resolver_cascade/iteration_001/`

Backup: `/Users/jleechan/evidence_backups/level_up_repro_5classes_20260504_011354/origin_main/`

## Caveats

- Campaign export fails with `ModuleNotFoundError: No module named 'fpdf'` — post-test artifact step only, not the tests themselves.
- Class 4: old Firestore entries persist (9 bad entries in cloned campaign) but are harmlessly scrubbed at read-time. New entries written clean.
- Review prompt copied to clipboard for independent agent review of fix durability.

## Relevance

- [[normalization-atomicity]] — Classes 1-3, 5 demonstrate the pattern
- [[level-up-flow]] — all 5 classes are level-up flow bugs
- [[rewards-engine]] — Classes 3, 5 involve rewards_engine.py fixes