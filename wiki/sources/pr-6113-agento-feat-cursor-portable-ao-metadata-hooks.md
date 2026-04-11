---
title: "PR #6113: [agento] feat(cursor): portable AO metadata hooks"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6113.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Align Cursor `PreToolUse` / `PostToolUse` Bash hooks with the existing portable pattern in `.claude/settings.json` (invoke `.claude/hooks/run-metadata-updater.sh` via `git rev-parse --show-toplevel`).
- Removes machine-specific absolute paths to worktrees and AO session directories so clones and CI behave consistently.

## Metadata
- **PR**: #6113
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +25/-1 in 3 files
- **Labels**: none

## Connections
