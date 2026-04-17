---
title: "PR #6275 — fix(level-up): Synthesize rewards_box When level_up_complete=True but box missing"
type: source
tags: [level-up, rewards-box, streaming, bugfix, stuck-completion]
date: 2026-04-15
source_file: ../raw/pr6275_fix_stuck_level_up_2026-04-15.md
---

## Summary
PR #6275 fixes the "stuck level-up" bug where `level_up_complete=True` is set by LevelUpAgent but the streaming path fails to emit `rewards_box`, causing the polling path to silently return `(None, None)`. The fix synthesizes `rewards_box` from game state when this stuck-completion scenario is detected.

## Problem
When LevelUpAgent completes a level-up, it sets `level_up_complete=True` in custom_campaign_state. However:
1. The streaming path may fail to emit `rewards_box`
2. The polling path calls `resolve_level_up_signal` which returns `level_up_detected=False`
3. The polling path then silently returns `(None, None)` — no level-up UI shown to player

## Solution
Added stuck-completion detection in `rewards_engine.resolve_level_up_signal`:
- When `level_up_complete=True` but `raw_rewards_box=None`
- Synthesize `rewards_box` from game state with `source='level_up_stuck_completion'`
- Include `planning_block` with ASI (Ability Score Improvement) choices at ASI levels (4, 8, 12, 16, 19)

## Also Added
- `_total_character_level()` function for multiclass ASI eligibility
- `_ASI_CHOICE_IDS` and `_ASI_DESCRIPTIONS` constants for ASI injection
- `normalize_rewards_box_for_ui()` — canonicalizer for rewards_box before Firestore persistence

## Key Files Changed
- `mvp_site/rewards_engine.py` — stuck completion fallback in `resolve_level_up_signal`
- `mvp_site/world_logic.py` — 479 additions for level-up v4 changes
- `mvp_site/llm_parser.py` — 44 additions for canonicalization

## Test Coverage
76/76 tests pass — the stuck completion scenario is now covered by `test_level_up_stale_flags.py`

## Connections
- [[LevelUpBugChain]] — root cause of the stuck level-up bug
- [[StreamingPassthrough]] — the streaming path that was failing to emit rewards_box
- [[NormalizeRewardsBox]] — the canonicalizer added to fix the normalization gap
- [[PR6338]] — autor PR that scored 87/100 using PRM technique on a similar stuck completion issue
