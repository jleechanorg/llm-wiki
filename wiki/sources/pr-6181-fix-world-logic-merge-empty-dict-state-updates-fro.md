---
title: "PR #6181: fix(world-logic): merge empty dict state_updates from Dragon Knight template"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6181.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Fix falsy check on `state_updates` dict that skipped merging when the dict was empty `{}`
- `isinstance(state_updates, dict) and state_updates` is falsy for `{}` -- removed the truthy guard since `isinstance` already excludes `None` and non-dict types
- Fixed both occurrences: Dragon Knight template path (line 4803) and LLM response path (line 4890)

## Metadata
- **PR**: #6181
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
