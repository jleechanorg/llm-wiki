---
title: "PR #6036: feat(statusline): add statusLine config and context caching to repo"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldarchitect-ai/pr-6036.md
sources: []
last_updated: 2026-03-21
---

## Summary
The Claude Code statusline was configured only in global `~/.claude/settings.json`, not in the repo. Contributors without that global config would not get the statusline. The global config uses `git-header.sh --status-only` to display branch, sync status, PR number, and context usage.

The repo's `git-header.sh` was also missing context percentage caching: when invoked from a terminal (no stdin), it showed `---%`. The global version caches ctx% to `/tmp/claude_ctx/<repo>/<branch>` via the Stop h

## Metadata
- **PR**: #6036
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +41/-29 in 3 files
- **Labels**: none

## Connections
