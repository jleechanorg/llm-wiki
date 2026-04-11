---
title: "PR #6197: fix(debug_info): emit debug_info on all turns, not just when rewards_box present"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6197.md
sources: []
last_updated: 2026-04-11
---

## Summary
- **Bug**: `debug_info` was gated inside `if hasattr(structured_response, "rewards_box")`, so it was silently absent on turns with no combat/XP rewards (most turns), even when `debug_mode=True`
- **Fix**: Moved to the outer `if structured_response:` block alongside `dice_rolls` and other per-turn fields
- **TDD**: Red to Green via `TestDebugInfoIndependentOfRewardsBox`

## Metadata
- **PR**: #6197
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +152/-3 in 2 files
- **Labels**: none

## Connections
