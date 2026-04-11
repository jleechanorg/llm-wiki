---
title: "PR #6179: fix(living-world): inject persisted world events for all users on page reload"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6179.md
sources: []
last_updated: 2026-04-11
---

## Summary
- inject_persisted_living_world_fallback was gated by debug_mode=True, preventing non-debug users from seeing living world updates after a page reload
- The frontend comment explicitly says living world is always visible when data is present (not debug-gated) — this was a backend bug
- Remove the debug_mode parameter entirely (was unused after fix) and update all callers

## Metadata
- **PR**: #6179
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +33/-27 in 3 files
- **Labels**: none

## Connections
