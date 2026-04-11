---
title: "PR #2588: fix(test): Fix arc_milestones extraction path in E2E test"
type: source
tags: []
date: 2025-12-26
source_file: raw/prs-worldarchitect-ai/pr-2588.md
sources: []
last_updated: 2025-12-26
---

## Summary
- Fixed bug where E2E test was looking for `arc_milestones` in wrong location
- Test was checking `game_state.custom_campaign_state.arc_milestones`
- Actual location is `game_state.arc_milestones`
- Now checks both locations for robustness

## Metadata
- **PR**: #2588
- **Merged**: 2025-12-26
- **Author**: jleechan2015
- **Stats**: +1075/-326 in 8 files
- **Labels**: none

## Connections
