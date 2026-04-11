---
title: "PR #6114: fix(world_logic): gate level-up narrative on _resolve_level_up_signal"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldarchitect-ai/pr-6114.md
sources: []
last_updated: 2026-04-06
---

## Summary
- **Level-up narrative injection** now uses `_resolve_level_up_signal()` (same as choice injection) instead of only checking `rewards_pending.level_up_available`.
- Stops **stale** `rewards_pending` from injecting **LEVEL UP** banners when modal flags (e.g. `level_up_in_progress=False`) say level-up is inactive.
- Passes `rewards_box` into `_inject_levelup_narrative_if_needed` from both unified response paths.

## Metadata
- **PR**: #6114
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +743/-3 in 4 files
- **Labels**: none

## Connections
