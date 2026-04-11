---
title: "PR #341: [agento] fix: worktree phase-2 scan when cwd is / (bd-d0la)"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-341.md
sources: []
last_updated: 2026-04-02
---

## Summary
Fixes `findRepoPathForWorktree` phase-2 when phase-1 does not find a `.git` directory (gitfile worktrees): phase-2 now walks `git worktree list` from **`workspacePath` upward to `/`**, not from `process.cwd()`. Daemon/launchd contexts where `cwd` is `/` still resolve the repo because the scan starts at the real worktree path. Also addresses CodeRabbit: `AO_WHOLESOME_PR_TITLE` is ignored in CI (`GITHUB_ACTIONS`); preferred env name `AO_WHOLESOME_PR_TITLE` with legacy `AO_WHOLLESOME_PR_TITLE` alia

## Metadata
- **PR**: #341
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +76/-31 in 4 files
- **Labels**: none

## Connections
