---
title: "PR #47: Add regression tests for thread index compatibility"
type: source
tags: [codex]
date: 2025-11-15
source_file: raw/prs-/pr-47.md
sources: []
last_updated: 2025-11-15
---

## Summary
- add regression tests that cover `create_performance_indexes` with and without `messages.thread_id`
- ensure the new tests verify the guarded index creation path so legacy snapshots stay compatible

## Metadata
- **PR**: #47
- **Merged**: 2025-11-15
- **Author**: jleechan2015
- **Stats**: +75/-0 in 1 files
- **Labels**: codex

## Connections
