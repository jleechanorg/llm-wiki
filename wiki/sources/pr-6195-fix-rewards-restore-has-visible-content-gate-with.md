---
title: "PR #6195: fix(rewards): restore has_visible_content gate with progress_percent support"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6195.md
sources: []
last_updated: 2026-04-11
---

## Summary
- PR #6193 removed the `has_visible_content` gate from `normalize_rewards_box_for_ui` entirely, breaking the `None`-sentinel contract used by `_process_rewards_followup` (world_logic.py:1767-1774)
- Without the gate, `normalize_rewards_box_for_ui({})` returns non-None, causing `rewards_already_in_response=True` for any primary response without rewards, silently skipping the rewards followup
- Restores the gate but adds `progress_percent > 0` (the actual missing condition from the original regres

## Metadata
- **PR**: #6195
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +131/-1 in 2 files
- **Labels**: none

## Connections
