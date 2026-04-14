---
title: "PR #6245: fix: stabilize level-up regressions and xp synthesis"
type: test-pr
date: 2026-04-13
pr_number: 6245
files_changed: [game_state.py, world_logic.py, test_world_logic.py, PR-6245.md]
---

## Summary
Fixes regressions from PRs #6233 and #6214 involving boolean casting rejecting numeric `1` or string `"1"` causing level-up blocking, and XP rewards synthesis failing on missing keys. Re-widens validations to ensure backward compatibility with production Firestore payloads.

## Key Changes
- **game_state.py**: Widened `_is_state_flag_true` to again allow `1` and `"1"`
- **world_logic.py**: Integrated `_parse_numeric` legacy logic into `extract_character_xp` for robust comma string parsing, updated `synthesize_generic_rewards_box` to safely pluck fallback XP from `combat_summary` and `encounter_summary['xp_awarded']`, fixed linter failures

## Diff Snippets
```python
# extract_character_xp now handles legacy nested objects
def extract_character_xp(player_data: dict) -> Optional[int]:
    # Handles "850", "850XP", "850 XP", nested experience.current objects
    ...
```

## Motivation
PR #6233 tightened semantics but broke backward compatibility - LLM commonly uses `1` / `"1"` for boolean fields.