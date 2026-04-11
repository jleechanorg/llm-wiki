---
title: "PR #5986: fix(living-world): CodeRabbit followups — key-presence checks, state_updates creation, full scene filter"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5986.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Fix key-presence vs truthiness bug in streaming `world_events` extraction
- Create `state_updates` when absent before mirroring `world_events` (both propagation points)
- Extend scene filter to cover all event types: `faction_updates`, `time_events`, `complications`, `scene_event`

## Metadata
- **PR**: #5986
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +255/-35 in 5 files
- **Labels**: none

## Connections
