---
name: stuck-levelupagent-root-cause-no-cap-prompt-fix-pr
description: Real cause of mXhtOccHYGHgV2Tdf0lc loop = PROHIBITED_CONTENT block (not level-20 cap / not thinking-exhaustion); prompt-only no-cap fix GREEN-validated on benign copy
metadata: 
  node_type: memory
  type: project
  originSessionId: 15c06163-394b-4d82-97e5-d551f8fa1350
---

Dev campaign `mXhtOccHYGHgV2Tdf0lc` (Itachi V3; UID `vnLp2G3m21PJL6kxcuAqmWSOtm73`) stuck at level 20, `experience.current=6,432,000` (XP implies level 141 via unbounded `level_from_xp`), `level_up_pending=True`, `_agent_selection_tracker.count≈20` = ~20-turn LevelUpAgent loop.

**Root cause (PROVEN):** the campaign's prompt is rejected by Gemini `promptFeedback.blockReason: PROHIBITED_CONTENT` — generation never starts → zero candidates → empty SSE stream → silent "The story continues..." fallback → `level_up_pending` never clears. Block lives only in **recent story entries seq ~1111–1123** (bisected); earlier turns were not blocked (validated user's "earlier it wasn't blocked"). `safetySettings: BLOCK_NONE` **cannot** disable PROHIBITED_CONTENT (non-configurable category).

**REFUTED prior misdiagnoses:** "level-20 hard cap" and "thinking-token exhaustion" — both disproven. No prompt fix can run on the real campaign because the model emits nothing there.

**Decision (user):** "Keep only the no-cap prompt fix." Ship the prompt change; do NOT add server block-surfacing, content mitigation, or backend enforcement. Real campaign documented (not fixed) in `testing_mcp/test_stuck_levelup_target_level_capture.py`.

**Fix = prompt-only**, `mvp_site/prompts/level_up_instruction.md` (+60/-9): "Availability Recognition — No Level Cap" section; unbounded `target_level = 20 + floor((experience.current − 355000)/50000)` (e.g. 6,432,000 → 141); flag-driven availability; multi-level catch-up commits `player_character_data.level = target_level` only on finish turn. No backend logic → no ZFC violation; mirrors already-unbounded `game_state.level_from_xp`.

**GREEN validated** (real local server + real Gemini, streaming) on a fresh **benign** seeded level-20 / 6.4M-XP Wizard (`test_levelup_nocap_benign_validation.py`): 2/2 pass, classification FULL_CATCHUP(141), `rewards_box = {current_level:20,new_level:141,resolved_target_level:141,level_up_available:true,source:"model"}`. Frozen HEAD `e67aa4fa709b65faff21b7a689c071b1a6b0a878`, clean-tree provenance, 49 stream chunks.

PR [#7251](https://github.com/jleechanorg/worldarchitect.ai/pull/7251) (branch `fix/level-up-no-max-level-catchup`). Evidence gist https://gist.github.com/jleechan2015/b7de386f4d2cab06bc93946186480f69 . Bead rev-94r2j. Known limitation in PR: does NOT fix the real blocked campaign; helps future non-blocked level-20+ characters. See [[feedback_2026-06-04_rewards_box_canonical_target_not_signal]].
