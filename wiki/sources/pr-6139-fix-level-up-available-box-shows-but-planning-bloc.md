---
title: "PR #6139: fix: level-up available box shows but planning block missing"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6139.md
sources: []
last_updated: 2026-04-09
---

## Summary
- Fixed the bug where frontend shows "LEVEL UP AVAILABLE!" but planning block with clickable choices is missing
- Root cause: `_infer_level_up_target_from_xp` ignored `rewards_box.level_up_available=True` when game_state XP didn't support level-up
- The fix checks rewards_box internal consistency using `xp_needed_for_level()` canonical thresholds and avoids double-counting XP

## Metadata
- **PR**: #6139
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +351/-20 in 5 files
- **Labels**: none

## Connections
