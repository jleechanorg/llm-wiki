---
title: "PR #51: refactor: codebase simplification — 1,518 lines removed"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-51.md
sources: []
last_updated: 2026-03-05
---

## Summary
Whole-codebase /simplify sweep using 5 parallel Sonnet subagents. Each agent reviewed a major directory, reported findings, then executed fixes in isolated git worktrees.

**51 files changed, +156 -1,518 lines (net -1,362)**

### Bugs fixed
- `mcp/server.ts` JSONL capture wrote `\\n` (literal) instead of `\n` (newline) — corrupted capture output
- `mcp.campaign.test.ts` had swallowed try/catch tests that always passed regardless of behavior

### Deduplication (backend)
- Extracted shared `choice

## Metadata
- **PR**: #51
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +157/-1518 in 52 files
- **Labels**: none

## Connections
