---
title: "PR #34: fix(backend): strip {"thinking":...} and {"choices":[...]} JSON leaks from scene_text"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldai_claw/pr-34.md
sources: []
last_updated: 2026-03-03
---

## Summary
- `stripStructuredBlocks` previously only removed `planning_block` objects and code fences
- `test_full_lifecycle_video.py` `_JSON_LEAK_PATTERNS` also checks for `{"thinking":...}` and `{"choices":[...]}` embedded in prose
- Extended `stripPlanningBlocks` to strip valid JSON objects with `planning_block`, `thinking`, or `choices` (array) at root level
- Guard preserved: full valid JSON responses returned unchanged for normal parsing

## Metadata
- **PR**: #34
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +349/-11 in 6 files
- **Labels**: none

## Connections
