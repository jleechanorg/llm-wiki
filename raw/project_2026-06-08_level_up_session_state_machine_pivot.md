---
name: level-up-session-state-machine-north-star-2026-06-08
description: "User designated the level-up session state machine design (~/roadmap/level-up-session-state-machine-design-2026-06-08.md) as the north star for the mppfHseT 14→15 work. Supersedes the 2-PR split (PR-A schema gate + PR-B LEVEL_UP_CHECK finish branch) and the flag-cleanup-only sub-PR surgery. New plan: 6 sequential PRs."
metadata: 
  node_type: memory
  type: project
  originSessionId: 54224e21-8040-4407-a0e1-209703cd5b39
---

# Level-up session state machine — north star (2026-06-08)

**Source:** User pointed at `~/roadmap/level-up-session-state-machine-design-2026-06-08.md` as the actual north star for the mppfHseT 14→15 finish-commit work. Design doc was created 2026-06-08.

**Why:** The 2-PR split (PR-A schema gate preservation + PR-B LEVEL_UP_CHECK finish branch) and the flag-cleanup-only sub-PR surgery were both scoped against the wrong hypothesis. The scout's raw-LLM capture (`evidence/scene_160_to_161_raw_llm.json`) showed the model did the right thing; the bugs are all backend-side, and the design doc prescribes a 6-PR migration that addresses all 5 failure classes (A through F) at once by making invalid level-up states impossible. Patching boolean flags one at a time has already failed repeatedly; the design replaces it with a single canonical `level_up_session` current-state object and hard invariants at parser, router, and persistence boundaries.

**How to apply:** When working on level-up / rewards / XP / state persistence, ALWAYS check `~/roadmap/level-up-session-state-machine-design-2026-06-08.md` first. The canonical state is `game_state.level_up_session` with status enum `available | in_progress | committing | complete | cancelled | error`. All legacy fields (`level_up_signal`, `rewards_box.level_up_available`, `rewards_pending`, `custom_campaign_state.level_up_*`) become derived compatibility outputs from `project_compatibility_fields()`. XP threshold math is validation only, not primary. New module: `mvp_site/level_up_session.py` with reducer functions.

**The 6-PR plan (sequential, stacked):**
1. **PR 1: Reducer Skeleton + Read-Only Projection** — new file `mvp_site/level_up_session.py` (~300-500 LOC) + fixture tests for mppf + vNU3. No production routing changes. Base: `origin/main`.
2. **PR 2: Finish Commit Fail-Closed** — route `finish_level_up_return_to_game` through `begin_finish_commit()` + `complete_finish_commit()`. PR-A's existing commit `9e33720d60` (schema-gate canonical preservation) lands as part of this. PR-B's LEVEL_UP_CHECK finish branch also lands here.
3. **PR 3: Atomic Persistence Boundary** — modal choices + rewards projected together
4. **PR 4: God Mode Contract Split** — admin commit vs modal handoff separation (bead `rev-s7olw`, issue #7363)
5. **PR 5: Routing Migration** — `agents.py` reads `level_up_session.status` only
6. **PR 6: Delete Legacy Writers** — grep-gated deletion of legacy field writes. This is where the flag cleanup from #7268 lands.

**Tracking issues:** #7334 (Class A: offer missing), #7361 (Class C: finish commit limbo), #7362 (Class D: stale current signal), #7363 (Class E: god-mode mixing), #7364 (Class B: atomic pair split).

**ZFC review:** Compliant. Reducer accepts explicit model fields; never classifies user intent; no synthetic state from free text; no XP-threshold primary; model owns the signal via `apply_model_level_up_signal()`.

**Beads:** `rev-d3gqg` (parent), `rev-yi5hn` (PR-A → PR 2), `rev-4ll30` (PR-B → PR 2), `rev-5ec62`, `rev-ugnha`, `rev-s7olw`, `rev-yj01x`. New design-beads for the 6 PRs to be created.

**PR #7268 status:** left alone (per user "leave this current PR alone"). Now obsolete once the 6-PR migration lands. Will be closed/superseded.

**Related:** `project_2026-06-07_pr7268_final_review_4lane_synthesis.md`, `project_2026-06-08_mppfHseT_finish_commit_real_bugs.md`, `project_2026-06-07_pr7268_cleanup_followups.md`, `feedback_2026-06-06_code_analysis_vs_live_capture.md` (root-cause-first discipline).
