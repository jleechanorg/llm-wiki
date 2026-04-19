---
title: "Level-Up Evidence Phase 1 Results — 2026-04-18"
type: source
tags: [level-up, evidence, testing, worldarchitect, bug-repro]
date: 2026-04-18
source_file: session-nextsteps-2026-04-18
---

## Summary

Phase 1 of the level-up evidence run completed using PR #6378 test suite (5-class repro tests) against current `main`. Class 5 (signal resolver cascade) is **confirmed REPRODUCED** on main — `_resolve_level_up_signal` suppresses `planning_block` emission when XP overflows with `level_up_complete=True`. Class 1 inconclusive (stale flag cleared unexpectedly). Class 3 incomplete (LLM world_events warning). Phase 2 (fix branch #6370) not started. testing_ui browser video not yet captured.

## Key Claims

- Class 5 REPRODUCED on main: `post_planning_block_present=False` + `post_rewards_box_present=False` on both XP-overflow scenarios
- Baseline XP-overflow path also suppressed — regression beyond Class 5 scope
- Class 1 test ran but showed `level_up_available=False` after turn (stale flag was cleared) — bug not observed; may be masked
- Class 3 hit LLM `world_events` omission warning mid-run, no checkpoint produced
- All Phase 1 tests used real local MCP server, real Gemini LLMs, MCPTestBase — base class requirement confirmed met
- Gate 6 (evidence) not CI-enforced for `mvp_site/*.py` PRs — only covers `testing_mcp/**` in `evidence-gate.yml`

## Key Quotes

> "Class 5 REPRODUCED: XP over threshold with level_up_complete=True, but _resolve_level_up_signal emitted no planning_block (suppression cascade)" — scenario_results_checkpoint.json

> "Baseline XP-overflow path ALSO suppressed — regression beyond Class 5" — scenario_results_checkpoint.json

## Connections

- [[LevelUpSignalResolver]] — `_resolve_level_up_signal` in world_logic.py is the root cause
- [[EvidenceGate]] — Gate 6 gap: evidence-gate.yml scope too narrow; needs expansion to cover production code
- [[MCPTestBase]] — base class requirement for all testing_mcp evidence runs

## Next Steps

- Phase 2: run same test suite against fix branch #6370 → bead `rev-beix`
- Rerun Class 3 (world_events warning causes incomplete)
- Run testing_ui browser video for planning_block UI path
- Expand evidence-gate.yml to `mvp_site/*.py` → bead `rev-08ks`
