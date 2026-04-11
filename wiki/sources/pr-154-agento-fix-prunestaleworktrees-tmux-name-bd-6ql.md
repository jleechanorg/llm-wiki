---
title: "PR #154: [agento] fix: pruneStaleWorktrees tmux name (bd-6ql)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-154.md
sources: []
last_updated: 2026-03-24
---

## Summary
`pruneStaleWorktrees` in `session-manager.ts` called `tmux has-session -t {worktreeName}` using the bare worktree directory name (e.g. `ao-748`). But AO tmux sessions are named `{12-char-hash}-ao-748` (e.g. `bb5e6b7f8db3-ao-748`). This mismatch meant the tmux check always returned "no session" — causing ALL AO worktrees to be incorrectly identified as stale and deleted.

## Metadata
- **PR**: #154
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +412/-145 in 5 files
- **Labels**: none

## Connections
