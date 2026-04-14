---
title: "PR #6212: fix(ui+state): keep final launch CTA visible and harden level-up atomicity"
type: test-pr
date: 2026-04-11
pr_number: 6212
files_changed: [campaign-wizard.js, world_logic.py, test_level_up_stale_flags.py, test_milestone_4_interactive_features.py, pr-6212.md, pr-6165.md, green-gate.yml]
---

## Summary
Bug-fix PR hardening two verified defects: (1) campaign wizard's final step had "Next" button hidden, breaking user muscle memory, and (2) stale level-up choices weren't being scrubbed from planning_block when game state didn't support level-up.

## Key Changes
- **campaign-wizard.js**: Keep `#wizard-next` visible on final step, relabel to match launch CTA, route both through new `attemptLaunch()` gate that validates, disables to prevent double-submit, calls launchCampaign()
- **world_logic.py**: `_enforce_rewards_box_planning_atomicity()` - replace no-op `pass` with active scrubbing, check `_resolve_level_up_signal()` and remove stale choices only when game state doesn't support level-up
- **test_level_up_stale_flags.py**: New unit tests for scrubbing behavior
- **test_milestone_4_interactive_features.py**: DOM tests for CTA visibility and double-submit prevention

## Diff Snippets
```python
# world_logic.py - active scrubbing instead of pass
if not rb_has_level_up and planning_has_lu:
-    # Preserve level-up planning here.
-    pass
+    # Scrub stale level-up choices when game state doesn't support level-up
+    if not _resolve_level_up_signal(game_state_dict):
+        planning_block = _remove_stale_level_up_choices(planning_block)
```

## Motivation
Both bugs were reproduced on origin/main with real local server and Firebase. The hidden CTA broke user flow, and stale level-up choices caused incorrect UI state.