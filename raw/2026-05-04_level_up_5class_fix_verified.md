---
name: 5-class level-up bugs all fixed on origin/main
description: All 5 original level-up bug repro tests pass on origin/main at commit 733a44f1 — each class has a specific fix commit
type: project
originSessionId: 4dead5c2-ec54-43a4-ab39-dcd83a88d050
---
## Learning: Level-Up 5-Class Bug Fix Verification Complete

### Context
Ran the original 5 level-up bug repro tests (Classes 1-5) on `origin/main` (commit `733a44f186a7ce51e00abee76155c47a689e7ffb`, 2026-05-04) using `./testing_mcp/run_level_up_class_repro_suite.sh` with `LEVEL_UP_SUITE_PARALLEL=0`. All 5 exited 0 with real Firebase + real Gemini + streaming path.

### Bug Fixes Per Class

| Class | Bug | Fix Commit(s) | Evidence |
|-------|-----|---------------|----------|
| **Class 1** | Stale `lua=True` modal lockout — `level_up_available` from LLM overrode authoritative `level_up_pending=False` | `29a8e1f70`, `fd2ae7770` — `game_state_dict` precedence over `structured_fields` in modal detection | `inject_stale_rewards_box` passed; `post_rewards: null` confirmed stale flag cleared |
| **Class 2** | Story entry projection strip — `rewards_box` missing when `level_up_pending=True` (passthrough wrote unwrapped rewards_box) | `220a87eb0`, `6926ad40a` — projection logic projects canonical UI whenever `level_up_pending=True` | `bad_entries_count: 0`, `projected_bad_entries_count: 0` |
| **Class 3** | Narrative XP desync — LLM announces XP but `experience.current` doesn't update (`xp_delta=None` caused stale echo suppression) | `58098933a` — `_raw_rewards_box_looks_like_stale_echo()` returns `False` when `xp_delta is None` | `pre_xp: 400 → post_xp: 900` (+500 exact delta) |
| **Class 4** | Historical Firestore residue — pre-fix code wrote raw `lua=True` to story entries | `2542e16f6` — `_scrub_stale_story_level_up_entry` scrubs at projection; new entries written clean | `new_entry_has_residue: false`, `projected_bad_entries_count: 0`; old 9 entries persist but harmlessly scrubbed at read-time |
| **Class 5** | Signal resolver cascade — `level_up_complete=True` + XP overflow suppressed planner/rewards every turn | `3ca0875bd` — `is_level_up_active()` checks `_has_unapplied_xp_threshold_crossing()` bypassing stale suppression | Both scenarios passed with `planning_has_lu: true`, `rewards_has_lu: true` |

### Evidence Bundles
```
/tmp/worldarchitect.ai/origin_main/level_up_class_1_stale_flag_lockout/iteration_001/
/tmp/worldarchitect.ai/origin_main/level_up_class_2_story_entry_projection_strip/iteration_001/
/tmp/worldarchitect.ai/origin_main/level_up_class_3_narrative_xp_desync/iteration_001/
/tmp/worldarchitect.ai/origin_main/level_up_class_4_historical_residue/iteration_001/
/tmp/worldarchitect.ai/origin_main/level_up_class_5_signal_resolver_cascade/iteration_001/
```
Backed up to: `/Users/jleechan/evidence_backups/level_up_repro_5classes_20260504_011354/origin_main/`

### Key Architectural Pattern
Each fix follows NormalizationAtomicity: canonicalization happens at persistence layer, not just display. Class 4 is the exception — old Firestore data persists but is scrubbed at projection layer rather than migrated.

### Caveat
Evidence bundles include campaign export failures (`ModuleNotFoundError: No module named 'fpdf'`) — this is a post-test artifact step, not the tests themselves. All actual assertions passed before that step.

### Integrate Branch
After `/integrate`, used detached HEAD workaround: `git checkout 733a44f18 --detach && git checkout -b "dev1777883676"` since `origin/main` is ambiguous as a branch name.