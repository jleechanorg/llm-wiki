---
title: "Stuck LevelUpAgent — Clearing Mechanism Already on Main, Evaded by `in_progress=true`"
type: source
tags: ["levelup", "stuck-agent", "worldarchitect-ai", "bead-rev-vcd2u"]
date: 2026-06-04
source_file: project_2026-06-04_stuck_levelupagent_already_on_main.md
---

## Summary
Answer to 'would one of these open PRs fix the stuck LevelUpAgent?': **No open PR is a proven net-new fix.** The stale-flag clearing mechanism already exists on main and is already wired (`rewards_engine.py:1430` + `agents.py:3352`).

## Key Claims
- `mvp_site/rewards_engine.py:1430` — `def is_stale_level_up_pending(game_state_like)`
- `mvp_site/agents.py:3352` — `... and not rewards_engine.is_stale_level_up_pending(game_state)` in routing
- Why L20 case stays stuck: early-return gate at `rewards_engine.py:1441-1452` — when `level_up_in_progress=true` the detector returns False = 'not stale'
- Stuck case = `level_up_pending=true` AND `level_up_in_progress=true`
- Per-PR: #7239 (prompt consolidation) = emission/skip/surfacing only; #7199 carries Bug A level merge-back (UNPROVEN); #7221/#7214 refine logic that already exists
- RCF proof (2026-06-03): Bug B refuted (already canonicalized game_state.py:824-873); Bug A unproven (campaign hit L20 max, no clean repro)

## Key Quotes
> Prevents the recurring false claim that a prompt PR 'fixes the stuck agent' — it can't touch persisted flags

## Connections
- [[LevelUpStuck]] — concept
- [[StaleFlagClear]] — concept
