---
title: "PR #289: [agento] fix(workspace-worktree): pre-flight disambiguate origin/main ref before git worktree add"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-289.md
sources: []
last_updated: 2026-03-29
---

## Summary
ao spawn failed with ambiguous object name origin/main — a local branch named refs/heads/origin/main shadowed refs/remotes/origin/main, making origin/main ambiguous to git ref resolution.

## Metadata
- **PR**: #289
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +166/-550 in 4 files
- **Labels**: none

## Connections
