---
title: "Daily LevelUp Suite Stale Test Contract (PR #7257)"
type: source
tags: ["levelup", "test-contract", "worldarchitect-ai", "pr-7257", "testing"]
date: 2026-06-04
source_file: project_2026-06-04_daily_levelup_suite_stale_test_contract_pr7257.md
---

## Summary
2026-06-05 'Daily Level Up Test' GCP cron failed 4/8. Evidence split: STALE TEST (atomicity_e2e, projected_level_up_button_text) — harness required `xp_gained>0` while production uses `level_up_available=true`. PR #7257 fixes test-harness only.

## Key Claims
- STALE TEST: real XP rose (295→345, level 1→2, rewards_box.xp_total positive, level_up_available=true) but harness `_visible_rewards_box` required xp_gained>0
- PR #7172 deliberately stopped synthesizing `xp_gained` in `ensure_rewards_box`
- `god_mode_reward_visibility` = PRE-EXISTING + intermittent (failed 06-04 too, before any 06-05 deploy) — bead rev-tspwq
- Fix: test-harness only (2 files: `testing_mcp/core/test_level_up_organic.py` + `.beads`); zero mvp_site/** change

## Key Quotes
> Visibility now mirrors `should_show_rewards_box()`; atomicity's 'real XP increase' assertion switched from the removed synthetic `rewards_box.current_xp` to a persisted `experience.current`/`xp_total` delta

## Connections
- [[LevelUpTesting]] — test contract concept
- [[PR7257]] — fix PR
