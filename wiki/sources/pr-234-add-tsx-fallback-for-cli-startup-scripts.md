---
title: "PR #234: Add tsx fallback for CLI startup scripts"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-234.md
sources: []
last_updated: 2025-11-13
---

## Summary
- update the Claude CLI wrapper and MCP stdio wrapper so they no longer depend on pre-built `dist/` files and instead fall back to running the TypeScript entrypoints with `tsx` when needed
- add the `tsx` dev dependency so the repository can execute backend scripts without committing build artifacts

## Metadata
- **PR**: #234
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +75/-11 in 4 files
- **Labels**: codex

## Connections
