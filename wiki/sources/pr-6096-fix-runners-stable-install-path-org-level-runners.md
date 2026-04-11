---
title: "PR #6096: fix(runners): stable install path + org-level runners + status --clean"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6096.md
sources: []
last_updated: 2026-04-05
---

## Summary
Self-hosted runners were silently capping at 2 despite expecting 6, and the launchd agent pointed to a worktree path that could be deleted. Runners were also repo-scoped instead of org-scoped.

## Metadata
- **PR**: #6096
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +195/-48 in 6 files
- **Labels**: none

## Connections
