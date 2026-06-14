---
title: "Level-up session state machine — north star pivot"
type: source
tags: [level-up, state-machine, north-star, pivot, worldarchitect-ai, 6-pr-migration]
date: 2026-06-08
source_file: raw/project_2026-06-08_level_up_session_state_machine_pivot.md
---

## Summary
User designated ~/roadmap/level-up-session-state-machine-design-2026-06-08.md as the north star for the mppfHseT 14→15 finish-commit work. Supersedes the 2-PR split (PR-A schema gate + PR-B LEVEL_UP_CHECK finish branch) and the flag-cleanup-only sub-PR surgery. New plan: 6 sequential PRs (PR 1 reducer skeleton + read-only projection, PR 2 finish commit fail-closed, PR 3 atomic persistence boundary, PR 4 god-mode contract split, PR 5 routing migration, PR 6 delete legacy writers). Canonical state = game_state.level_up_session with status enum available | in_progress | committing | complete | cancelled | error. New module mvp_site/level_up_session.py with reducer functions. ZFC compliant.

## Key Claims
- 2-PR split (PR-A schema gate + PR-B LEVEL_UP_CHECK finish branch) and flag-cleanup-only sub-PR surgery both scoped against wrong hypothesis
- Scout's raw-LLM capture (evidence/scene_160_to_161_raw_llm.json) showed model did the right thing; bugs are all backend-side
- 6-PR plan: PR 1 reducer skeleton + read-only projection, PR 2 finish commit fail-closed, PR 3 atomic persistence boundary, PR 4 god-mode contract split, PR 5 routing migration, PR 6 delete legacy writers
- Canonical state = game_state.level_up_session with status enum: available | in_progress | committing | complete | cancelled | error
- All legacy fields (level_up_signal, rewards_box.level_up_available, rewards_pending, custom_campaign_state.level_up_*) become derived compatibility outputs from project_compatibility_fields()

## Connections
- [[project_2026-06-08_mppfHseT_finish_commit_real_bugs]]
- [[project_2026-06-07_pr7268_final_review_4lane_synthesis]]
- [[project_2026-06-07_pr7268_cleanup_followups]]
- [[feedback_2026-06-06_code_analysis_vs_live_capture]]
- [[LevelUpStateMachine]]
