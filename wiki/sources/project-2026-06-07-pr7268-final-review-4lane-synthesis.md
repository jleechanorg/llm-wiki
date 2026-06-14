---
title: "PR #7268 level-up clean-flags 4-lane review synthesis"
type: source
tags: [pr-7268, level-up, final-review, 4-lane, not-ready, worldarchitect-ai]
date: 2026-06-07
source_file: raw/project_2026-06-07_pr7268_final_review_4lane_synthesis.md
---

## Summary
PR #7268 level-up clean-flags refactor (head 7d22459fc7, worktree codex-pr-7268-sync) 4 parallel lanes (ZFC+new-flag, /zfclevel, /root-cause-first, uncommitted/CI) plus earlier /thermo + code-standards/DRY + net-additions audit. User criterion 'less flags, less backend logic' NOT MET: +553 net production LOC across 7 core files (rewards +442/-212, world_logic +283/-150, game_state +275/-65, agents +123/-166, llm_parser +195/-54, narrative +50/-44, llm_service +8/-12). 10 cross-lane blockers. Verdict: NOT READY FOR MERGE. Default action: CLOSE in favor of two narrower PRs (flag-deletion-only, derived-state-only) gated on /es at new head.

## Key Claims
- +553 net production LOC across 7 core files: rewards +442/-212, world_logic +283/-150, game_state +275/-65, agents +123/-166, llm_parser +195/-54, narrative +50/-44, llm_service +8/-12
- 10 cross-lane blockers: test_character_creation_matches_string_flags fails (is_level_up_active False for mock, is_stale_level_up_pending gates it, proposed agents.py:1298-1303 reorder does NOT fix root cause); test_level_up_modal_exit_end2end.py shard-2 unknown trace; schema strip downgraded raise→warn at f2621a0c86 (5d1b92eb was hard reject); rewards_engine.py:1722-1733 threshold-derived XP T6 violation; agents.py:1298-1303 CC/level-up priority reorder no prompt basis; API contract freeze 6+ new public symbols; HP-alias scope creep; /es evidence stale at 5d1b92eb; 12 author comments unaddressed; Continue_story include_continue_story=not level_up_modal_active line 399
- T6 XP-threshold still primary decision; T7 no /es evidence at PR head
- Do NOT recommend merge until /es evidence exists at current head AND net production LOC ≤ 0 OR per-line justification documented

## Connections
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[project_2026-06-07_pr7268_cleanup_followups]]
- [[project_2026-06-08_mppfHseT_finish_commit_real_bugs]]
- [[ZFCLevelUp]]
- [[Pr7268]]
