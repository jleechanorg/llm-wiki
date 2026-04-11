---
title: "PR #6161: fix: rewards_box/planning_block atomicity and get_campaign_state"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6161.md
sources: []
last_updated: 2026-04-11
---

## Summary
PR #6161 fixes a stale polling issue where `rewards_box` and `planning_block` atomicity was broken during `get_campaign_state` polling. `rewards_box` was originally missing from the structured extraction utils, resulting in a badge without buttons state.

## Metadata
- **PR**: #6161
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +8846/-2128 in 67 files
- **Labels**: none

## Connections
