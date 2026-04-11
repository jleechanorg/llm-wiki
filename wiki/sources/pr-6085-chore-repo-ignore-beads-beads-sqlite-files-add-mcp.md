---
title: "PR #6085: chore(repo): ignore .beads/.beads/ SQLite files + add MCP installer script"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6085.md
sources: []
last_updated: 2026-04-04
---

## Summary
Two cleanup items found as untracked files in the worktree:
1. `.beads/.beads/` directory created by `br` (beads_rust) when running in worktrees — contains SQLite DB and WAL files that must not be committed
2. `scripts/install_worldai_mcp.sh` was authored on `feat/update-beads-skill-docs` but never merged to main

## Metadata
- **PR**: #6085
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +123/-0 in 2 files
- **Labels**: none

## Connections
