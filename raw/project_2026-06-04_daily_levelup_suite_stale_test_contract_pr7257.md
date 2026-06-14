---
name: daily-levelup-suite-stale-test-contract-after-7172-pr7257
description: Daily level-up cron 4/8 red was test-contract drift (harness required xp_gained>0) not a #7172 over-strip regression; fix = mirror should_show_rewards_box; PR #7257
metadata:
  node_type: memory
  type: project
  originSessionId: 15c06163-394b-4d82-97e5-d551f8fa1350
---

The 2026-06-05 "Daily Level Up Test" GCP cron failed 4/8. Evidence (GCS `gs://wa-test-evidence/daily/2026-06-05`, compared against 2026-06-04) split the failures:

- **STALE TEST** (`atomicity_e2e`, `projected_level_up_button_text`): real XP genuinely rose (e.g. `experience.current` 295→345, level 1→2, `rewards_box.xp_total` positive, `level_up_available=true`), but the harness `_visible_rewards_box`/`_persisted_visible_rewards_box` only treated a box as "visible" when `xp_gained > 0`. Merged PR [#7172](https://github.com/jleechanorg/worldarchitect.ai/pull/7172) deliberately stopped synthesizing `xp_gained` in `ensure_rewards_box`; the model also stopped emitting it on the trigger/poll turn. Production `should_show_rewards_box()` (`mvp_site/rewards_engine.py:1761`) treats `level_up_available=true` as sufficient — the test was STRICTER than production.
- **#7172 over-strip theory REFUTED**: its `merged_rb_no_lu.pop("xp_gained"...)` only runs on the *state-backed fallback* branch, NOT on model-emitted boxes. The god_mode immediate API response still carried `xp_gained=300, source=model`. No genuine award is stripped.
- **`god_mode_reward_visibility` = PRE-EXISTING + intermittent** (failed identically on 06-04, before any 06-05 deploy): the *persisted Firestore story entry* sometimes carries no `rewards_box` at all. Separate production persistence gap, tracked by bead **rev-tspwq**. NOT fixed in this PR.
- **`multi_level_organic_progression` = UNRELATED** cluster (story-freeze turn advance + finish-copy assertion). Out of scope.

**Fix (PR [#7257](https://github.com/jleechanorg/worldarchitect.ai/pull/7257), branch `fix/daily-levelup-test-contract`, head `e192400c30`, OPEN/MERGEABLE, NOT merged):** test-harness only (2 files: `testing_mcp/core/test_level_up_organic.py` +62/-30 + `.beads`). Visibility now mirrors `should_show_rewards_box()`; atomicity's "real XP increase" assertion switched from the removed synthetic `rewards_box.current_xp` to a persisted `experience.current`/`xp_total` delta vs `pre_trigger_xp` (stronger, not weaker). Zero `mvp_site/**` change. GREEN on real Gemini+Firebase streaming: atomicity (1→2, 295→345), god_mode (0→300), projected (1→2→300). `projected_level_up_button_text` is **LLM-flaky** in code paths the change doesn't touch (`level_up_in_progress` not set) — matches the cron's nondeterministic RED.

Bead rev-tspwq (P1) tracks the suite-red issue; rev-ufb13's acceptance criteria are now stale (predate #7172, still demand `xp_gained>0`) — commented. See [[feedback_2026-06-04_rewards_box_canonical_target_not_signal]] and [[stuck-levelupagent-root-cause-no-cap-prompt-fix-pr]].
