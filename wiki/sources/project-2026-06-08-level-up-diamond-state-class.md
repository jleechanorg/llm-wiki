---
title: "Level-up diamond state bug class — months of failed fixes root cause"
type: source
tags: [level-up, diamond-state, bug-class, production-evidence, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_level_up_diamond_state_class.md
---

## Summary
A 'diamond state' is when a level-up finish commit writes pcd.level = N+1 atomically, but the top-level level_up_signal: {current_level: N, target_level: N+1} (or one of level_up_pending / level_up_in_progress / rewards_pending.level_up_available) is NOT cleared atomically. custom_campaign_state copy IS cleared → modal-reopen logic reads top-level signal misfires. 90-PR audit (2026-06-08): every PR targets ONE field, bug spans FOUR. Production evidence on vNU3AAXHd9N7adqWSM2p (level 18, turn 210) and mppfHseT9cy44Ywro4oJ (level 15). Action plan: rev-254ez 30-LOC invariant gate + rev-544i4 daily production observer.

## Key Claims
- Bug class: finish commit writes pcd.level=N+1 atomically but top-level signal not cleared → 'diamond' where pcd committed, signal dangling-stale
- PR audit of 90 level-up PRs in 60 days: every PR targets ONE field, bug spans FOUR. level_up_pending (3 PRs), level_up_in_progress (1 PR), level_up_complete (1 PR), rewards_pending.level_up_available (1 PR), level_up_signal (NO PR promotes to single source of truth)
- Meta-fix #7268 (+5477/-2382, 7,859 net LOC) has been OPEN since 2026-06-05 with reviewDecision=empty. Not reviewable at that size
- Production repros: vNU3AAXHd9N7adqWSM2p (Vespera Thul, level 18, pcd.level=18, XP 266,750/305,000, but level_up_signal={current_level:17, target_level:18} STALE), mppfHseT9cy44Ywro4oJ (Bg3 farming, level 15, case study)
- rev-254ez 30-LOC invariant gate: level_up_signal = (target > current) is canonical; if any of {pending, in_progress, complete, rewards_pending.level_up_available} is true while signal says no level-up active, FAIL the write (DiamondStateError)

## Connections
- [[project_2026-06-08_mppfHseT_finish_commit_real_bugs]]
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[DiamondStateBug]]
- [[LevelUpInvariantGate]]
