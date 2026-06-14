---
title: "Feedback 2026-06-03 Beads Rebase Duplication"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-06-03
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-03_beads_rebase_duplication.md
---

## Summary

After on a branch that has a custom , the rebase can produce a file where main's full entries are duplicated alongside branch-unique additions. In PR #7236 the post-rebase file was 3254 lines (1614 dupes, 26 unique-to-branch) instead of expected ~1665 (1639 main + 26 new). Strict CI gate fails with "duplicate id" lines.

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[beads]]
- [[rebase]]
