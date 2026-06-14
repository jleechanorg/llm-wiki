---
title: "mppfHseT 14→15 finish commit real bug signature"
type: source
tags: [level-up, finish-commit, raw-llm-trace, real-bugs, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_mppfHseT_finish_commit_real_bugs.md
---

## Summary
Scout's raw LLM capture (against s9 / branch codex-pr-7268-sync, test copy campaign eF2Bk834MTPDFdFlsBfb reset to pre-Scene-160 state) disproved the original 'LLM omitted level bump' hypothesis for mppfHseT 14→15 finish commit limbo. Model returned a valid 6103-char JSON response with level: 15 present and parsed cleanly. Real bugs are all backend-side: (1) STATE_UPDATE_SCHEMA_GATE silently re-maps level_up_signal → level_up_stage under 'strict overlay policy'; (2) finish commit misclassified as 'organic level-up for rewards_pending' in LEVEL_UP_CHECK; (3) diamond state inconsistency (pcd.level=15 but level_up_complete=True + completed_level=0 + level_up_signal still {current_level:14, target_level:15}).

## Key Claims
- Raw LLM capture disproved 'LLM omitted level bump' hypothesis — model returned valid 6103-char JSON with level: 15 present
- Real bug 1: STATE_UPDATE_SCHEMA_GATE silently re-maps level_up_signal → level_up_stage under 'strict overlay policy' (canonical LLM field lost in process)
- Real bug 2: finish commit misclassified as 'organic level-up for rewards_pending' in LEVEL_UP_CHECK — finish branch (PHASE_CONCLUDE on finish_level_up_return_to_game) needs dedicated path
- Real bug 3: diamond state inconsistency — pcd.level=15 but level_up_complete=True + completed_level=0 + level_up_signal still {current_level:14, target_level:15}
- Implication for proposed split PRs: B1 (signal retention) helps prevent schema re-mapping race but real fix is in STATE_UPDATE_SCHEMA_GATE; B2 (finish contract via system_corrections) helps with misclassification but real fix is in LEVEL_UP_CHECK finish-vs-organic branch; B3 (limbo re-hydrate) was already deleted as ZFC violation

## Connections
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[feedback_2026-06-06_code_analysis_vs_live_capture]]
- [[project_2026-06-08_level_up_diamond_state_class]]
- [[FinishCommitLimbo]]
