---
title: "PR #6259: [antig] fix: resolve missed serious PR audit findings"
type: test-pr
date: 2026-04-14
pr_number: 6259
files_changed: [skeptic-evaluate.sh, game_state.py, world_logic.py, test_world_events_real_repro.py]
---

## Summary
Proactively resolves several serious issues identified in recent PR audits that were merged despite "Major" findings. Improves diagnostic reliability, skeptic cron observability, state flag semantics handling, and reward precision.

## Key Changes
- **test_world_events_real_repro.py**: Added explicit guard checks for `"error"` keys when fetching campaign state - prevents KeyError crashes when campaigns are deleted/inaccessible
- **skeptic-evaluate.sh**: Refactored `gh api` calls to capture and log stderr on failure, hardened `VERDICT_LINE` extraction for multi-line skeptic bodies
- **game_state.py**: Updated `_is_state_flag_true` and `_is_state_flag_false` to accept `1.0` and `0.0` (floats) while remaining strict against non-integer floats like `0.5`
- **world_logic.py**: Refactored gold and XP reward fallbacks to use explicit `is not None` checks - ensures intentional `0 gold` is respected and not overwritten by stale rewards_pending data

## Diff Snippets
```bash
# skeptic-evaluate.sh - stderr capture
-          --jq '.id' > /dev/null 2>&1; then
+          --jq '.id' > /dev/null 2> "$API_ERR_FILE"; then
+            echo "API Error Details:"
+            cat "$API_ERR_FILE" >&2

# game_state.py - float boolean handling
+    if isinstance(value, float) and value in (1.0, 0.0):
+        return value == 1.0
```

## Motivation
PR audits found issues that were merged despite "Major" findings - this fixes the technical debt from rapid merge cycles.