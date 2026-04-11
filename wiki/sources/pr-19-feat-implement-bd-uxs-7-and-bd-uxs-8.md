---
title: "PR #19: feat: implement bd-uxs.7 and bd-uxs.8"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldai_claw/pr-19.md
sources: []
last_updated: 2026-03-19
---

## Summary
Implements two orchestration beads:

- **bd-uxs.7**: Add .ao-managed ignore list to worktree porcelain check
  - Adds `setupAoManagedExclude()` function to workspace-worktree plugin
  - Creates `.git/info/exclude` with AO-managed file patterns on worktree creation
  - Prevents worktree dirty regressions

- **bd-uxs.8**: Configurable merge-gate hook
  - Adds `MergeGateConfig` interface to `ProjectConfig`
  - Supports `requiredLabels`, `blockedLabels`, `requiredChecks`
  - Supports `minApprovals`,

## Metadata
- **PR**: #19
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +1038/-18 in 8 files
- **Labels**: none

## Connections
