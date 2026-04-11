---
title: "PR #6204: fix(world-logic): hoist 5 fields out of rewards_box block"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6204.md
sources: []
last_updated: 2026-04-11
---

## Summary
5 fields were incorrectly nested inside `if hasattr(structured_response, "rewards_box"):` block in `world_logic.py:6707-6738`. They are now independent conditionals at the same level.

## Metadata
- **PR**: #6204
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +76/-26 in 2 files
- **Labels**: none

## Connections
