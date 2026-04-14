---
title: "PR #6261: Rewards Box Visibility Regression"
type: source
tags: [worldarchitect, rewards-box, numeric-extraction, regression]
date: 2026-04-14
source_file: raw/pr-6261-rewards-box-visibility-regression.md
---

## Summary
PR #6261 fixes rewards box visibility regression where campaign `WQEl4sJb7RqWLndJK4GU` was not rendering rewards box due to LLM units ("1,000 gp") tricking the coercer into returning 0. Centralizes robust numeric extraction in `DefensiveNumericConverter` with regex pass.

## Key Claims
- **Root cause**: `_get_raw` helper and `_extract_reward_value` were fragile localized hacks bypassing Pydantic schema
- **Fix**: `DefensiveNumericConverter.convert_value` now includes regex pass `re.search(r"[-+]?[0-9]*\.?[0-9]+", value.replace(",", ""))` for strings like "850 XP", "10/20", "1,000"
- **Removed**: `_extract_reward_value` and `_get_raw` helper methods from world_logic.py
- **Key change**: Uses `coerce_int` for `next_level_xp` to avoid DNC's 300 default for invalid values

## Connections
- [[LevelUpBug]] — bug chain
- [[RewardsBox]] — rewards_box numeric fields
- [[DefensiveNumericConverter]] — robust numeric extraction
