---
title: "PR #7366 vs PR #7368 (PR 1) — competing level_up_session reducer PRs"
type: source
tags: [level-up, competing-prs, pr-7366, pr-7368, subsumption, worldarchitect-ai]
date: 2026-06-09
source_file: raw/project_2026-06-09_pr7366_supersedes_pr1_conflict.md
---

## Summary
PR #7366 (jleechan2015, 2026-06-08T19:58Z) and PR #7368 (PR 1 of 6-PR chain) both touch the same production files. PR #7366 is a strict superset (reducer + schema + roadmap + CI gate); PR #7368 is the subset (reducer only). Per memory 'competing-pr-subsumption-close-subset' rule, the subset should close as subsumed — BUT closing PR 1 orphans PRs 2-5.5 which all depend on PR 1's reducer. 4 resolution paths: (1) close PR 1 as subsumed (breaks chain), (2) rebase PR 7366 onto PR 1's head (preserves chain), (3) keep both deconflict manually (high risk), (4) close PR 7366 (preserves chain). Do NOT close either PR without user approval — strategic PR closure is a user decision.

## Key Claims
- PR #7366 overlaps 12 files with PR 1; PR 7366 is the strict superset (reducer + schema + roadmap + CI gate), PR 7368 is the subset (reducer only)
- If we close PR 1, the 6-PR chain (1→2→3→4→5.5→5→6) becomes orphaned because PRs 2-5.5 all depend on PR 1's reducer
- Realistic resolution paths: close PR 1 as subsumed (clean) but break the chain, rebase PR 7366 onto PR 1's head (preserves chain), keep both (high conflict risk), or close PR 7366 (preserves chain, schema infra as follow-up)
- Strategic PR closure is a user decision — do NOT close either PR autonomously

## Connections
- [[feedback_2026-06-07_competing_pr_subsumption_close_subset]]
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[LevelUpChain]]
