---
title: "PR #221: chore: skip redundant hook checks when tree unchanged"
type: source
tags: [codex]
date: 2025-10-07
source_file: raw/prs-/pr-221.md
sources: []
last_updated: 2025-10-07
---

## Summary
- cache the tree hash after successful presubmit runs in the generated pre-commit hook
- skip running pre-push tests when the recorded tree matches HEAD and the working tree is clean

## Metadata
- **PR**: #221
- **Merged**: 2025-10-07
- **Author**: jleechan2015
- **Stats**: +95/-1 in 1 files
- **Labels**: codex

## Connections
