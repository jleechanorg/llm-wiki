---
name: levelup-cleanup-state-2026-06-10
description: Level-up train shipped (4 merges) then MERGE FREEZE + cleanup plan M0-M4; M1 audit found 8 unregistered adjusters + 1 banned pattern; trim/unfreeze sequencing
metadata: 
  node_type: memory
  type: project
  originSessionId: d1fe8f3f-4d95-42f6-92c4-4a7a1018530c
---

State as of 2026-06-10 end of session:
- **MERGED:** #7370 (PR2+3 combined), #7376 (god-mode split), #7442 (dispatcher → god_mode_level_up.py, world_logic −439), #7416. All 8 evidence audits COMPLIANT (real Gemini, SHA-matched).
- **MERGE FREEZE** on level-up PRs until cleanup M1–M3 land. Plan: repo `roadmap/level-up-main-cleanup-2026-06-10.md` (on branch cleanup-level-up-main-zfc-cleanup, PR [#7443](https://github.com/jleechanorg/worldarchitect.ai/pull/7443) = M0, exempt+being greened).
- **M1 audit DONE** (table /tmp/worldarchitect.ai/m1-guard-audit-2026-06-10.md — copy into M1.5 PR, /tmp volatile): 35 sites — 16 mechanics, 12 registered, 8 unregistered (C), 1 banned (D = `resolve_level_up_signal` rewards_engine:1499-1576 threshold-derived detection).
- **Sequence:** #7443 merge → M1.5 register (rev-ksl9x) → M2 delete override+spec paired, Gate 2b auto-tightens (rev-zn7qu) → M2.5 remove current_level from signal schema, deletes Inv-11 apparatus (rev-a8ko2) → M3/PR6 legacy-writer deletion (rev-37xca) → M4 unfreeze: #7441 first (prompt fix), then #7374 (3 Bugbot fixes pending + world_logic-minimization directive), #7377 (APPROVED, verdict PASS @101b109ab0, base retargeted to main; merge gated on dark-factory validation graph rev-ghrm4: testing_mcp/core/test_level_up_organic.py + routing evidence, Claude cold reviewer), #7252, #7247/#7424 (latter needs /zfclevel), #7357 rescope.
- **Hazard:** unidentified background automation force-pushes level-up branches under shared jleechan2015 credential (3 incidents 2026-06-10); detect via `gh api repos/jleechanorg/worldarchitect.ai/activity?ref=refs/heads/<branch>`.
- Validation pipeline spec: `~/roadmap/pr7377-e2e-validation-pipeline-2026-06-10.md`. Nextsteps: `~/roadmap/nextsteps-2026-06-10-levelup-train-cleanup.md`. Related: [[review-loops-ratchet-backend]], [[stacked-pr-single-writer-rule]].
