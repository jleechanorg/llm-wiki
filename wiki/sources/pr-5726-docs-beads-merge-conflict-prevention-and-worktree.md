---
title: "PR #5726: docs: beads merge conflict prevention and worktree drift guidance"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5726.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Switch `.beads/issues.jsonl` merge driver from `merge=beads` to `merge=union` (git built-in) — eliminates merge conflict markers permanently
- Document the union driver setup, recovery steps, and how the pre-commit hook auto-stages beads with every code commit
- Document worktree drift pattern: main repo dir beads can safely be discarded with `git checkout -- .beads/issues.jsonl`

## Metadata
- **PR**: #5726
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +39/-2 in 3 files
- **Labels**: none

## Connections
