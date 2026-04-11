---
title: "PR #5975: fix: actor-keyed merge for background_events prevents field stripping on partial LLM updates"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5975.md
sources: []
last_updated: 2026-03-15
---

## Summary
- `_merge_background_events()` + Case 10b in `update_state_with_changes()`  
- 29 unit tests pass (2 new: partial update preserves fields, new actor appended)  
- E2E: 2/2 scenarios pass; Turn 7 merge verified

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Metadata
- **PR**: #5975
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +136/-0 in 3 files
- **Labels**: none

## Connections
