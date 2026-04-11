---
title: "PR #20: docs: living blog refactor design + TDD roadmap"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-/pr-20.md
sources: []
last_updated: 2026-03-27
---

## Summary
Design + TDD roadmap for the living blog repo redesign (Phase 1). Based on 2026-03-27 design session where Jeffrey specified:
- CLI owns GH API fetching (Option A): `blog-cli branch-entry --session ao-832 --pr 42 --repo owner/repo`
- CLI fetches PR events, commits, checks, reviews directly via GitHub REST API
- CLI writes `novel/workers/{sessionId}.md`, optionally POSTs to MCP via `--output=both`
- MCP server for non-AO repos and interactive chat (Path B + Path C)
- FIFO bidirectional chat for w

## Metadata
- **PR**: #20
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +1358/-0 in 4 files
- **Labels**: none

## Connections
