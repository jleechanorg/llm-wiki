---
name: mppfhset-14-15-finish-commit-real-bugs-scout-capture-2026-06-08
description: "Raw LLM trace disproved the \"LLM omitted level bump\" hypothesis for mppfHseT 14→15 finish commit limbo. Real bugs are backend-side: schema re-mapping, organic misclassification, diamond state."
metadata: 
  node_type: memory
  type: project
  originSessionId: 54224e21-8040-4407-a0e1-209703cd5b39
---

# mppfHseT 14→15 finish commit — real bug signature (2026-06-08)

**Bead:** rev-d3gqg · **Issue:** #7361 · **Source:** `evidence/scene_160_to_161_raw_llm.json` + `evidence/scene_161_garbage_string.txt`

**Why:** The scout's raw LLM capture (against s9 / branch `codex-pr-7268-sync`, test copy campaign `eF2Bk834MTPDFdFlsBfb` reset to pre-Scene-160 state) **disproved the original hypothesis** that the LLM omitted `state_updates.player_character_data.level` on the finish turn. The model returned a valid 6103-char JSON response with `level: 15` present and parsed cleanly. The "The story continues…" stub is NOT a fail-open parse — it's a different (later) code path.

**How to apply:** When investigating a finish-commit or level-up limbo, **always capture the raw LLM trace first** before designing the fix. The original 3-behavior add-on (B1 retention, B2 fail-closed, B3 limbo re-hydrate) was based on the wrong root cause. The real bugs are all backend-side:

1. **`STATE_UPDATE_SCHEMA_GATE` silently re-maps `level_up_signal` → `level_up_stage`** under "strict overlay policy" (canonical LLM field lost in the process). Backend bug, not a model bug. Fix is in the schema gate or the overlay policy, not the model emission.

2. **Finish commit misclassified as "organic level-up for rewards_pending"** in `LEVEL_UP_CHECK`. The finish branch (PHASE_CONCLUDE on `finish_level_up_return_to_game`) needs a dedicated path that doesn't go through the organic-rewards re-creation flow.

3. **Diamond state inconsistency**: `player_character_data.level=15` but `level_up_complete=True` + `completed_level=0` + `level_up_signal` still `{current_level:14, target_level:15}` (signal NOT cleared after commit). Multiple writers racing for the same fields; the "complete" flag and the "level" field update independently. The "Awaiting LLM to commit level change" log shows the system is waiting on a commit that already happened.

**Implication for the proposed split PRs** (PR-A B1 retention, PR-B B2 contract, B3 deleted as drawn):
- **B1 (signal retention)** may help prevent the schema re-mapping race, but the real fix is in `STATE_UPDATE_SCHEMA_GATE`. B1 alone won't address the root cause.
- **B2 (finish contract via system_corrections)** may help with the misclassification, but the real fix is in `LEVEL_UP_CHECK`'s finish-vs-organic branch. B2 alone won't address the root cause.
- **B3 (limbo re-hydrate via XP-synthesized signal)** was already deleted as a ZFC violation.
- Both proposed PRs need **rescoping** after the redline memo (task #2) determines whether #7268's recent commits (`70275309ec`, `0effe23d34`, `5b62068e1c`, `216e9df015`) already address any of these specific bugs.

**Related:** `feedback_2026-06-06_code_analysis_vs_live_capture.md` (root cause discipline: anchor to real wire evidence before filing root cause). The god-mode repro showed a similar pattern — analysis was wrong, live capture was right.
