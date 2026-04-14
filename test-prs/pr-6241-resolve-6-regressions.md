---
title: "PR #6241: [antig] fix: resolve 6 regressions from merged PRs"
type: test-pr
date: 2026-04-13
pr_number: 6241
files_changed: [game_state.py, world_logic.py, test_world_logic.py, base_test.py, evidence_utils.py, test_evidence_utils_unit.py]
---

## Summary
Fixes 6 regressions introduced by PR #6233 (centralize level/XP architecture) that were merged with unresolved CHANGES_REQUESTED reviews. Issues include NameErrors (deleted function references), missing source_id assignments, unvalidated progress_percent, evidence bundle crashes, and stale test mocks.

## Key Changes
- **world_logic.py**: Fixes NameError references to `_normalize_rewards_box_for_ui` and `_extract_xp_robust`; adds `import math`; adds `progress_percent` clamping (0-100) and non-finite rejection
- **game_state.py**: Adds missing `_original_stored_level_for_source` assignment in narrative-only level jump else-branch
- **test_world_logic.py**: Updates 3 tests to expect synthesized rewards boxes instead of RuntimeError
- **evidence_utils.py**: Wraps video frame extraction in try/except
- **base_test.py**: Fixes asciinema stderr handling (subprocess.PIPE + text=True)
- **test_evidence_utils_unit.py**: Replaces stale mock with correct function, updates assertion strings

## Motivation
PR #6233 was merged despite CHANGES_REQUESTED reviews - these are the post-mortem fixes.