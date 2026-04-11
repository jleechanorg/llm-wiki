---
title: "PR #6130: [agento] feat(cursor): portable AO metadata hooks for Cursor sessions"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6130.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Add `.cursor/metadata-updater.sh` (executable) for Agent Orchestrator session metadata updates on `gh pr create`, branch switches, and allowed merges.
- Configure workspace-relative Cursor `PreToolUse` / `PostToolUse` hooks using `${workspaceFolder}` so clones and worktrees do not embed absolute paths.
- Resolve `~/.agent-orchestrator/*-worldarchitect.ai/sessions` automatically when `AO_DATA_DIR` is unset.

## Metadata
- **PR**: #6130
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +612/-2 in 4 files
- **Labels**: none

## Connections
