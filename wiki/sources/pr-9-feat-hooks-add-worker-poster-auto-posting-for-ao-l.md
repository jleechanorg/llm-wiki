---
title: "PR #9: feat(hooks): add worker-poster auto-posting for AO lifecycle events [P1] (jleechan-yl5g)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-/pr-9.md
sources: []
last_updated: 2026-03-26
---

## Summary
Implements **P1-3: Worker Auto-Posting** from the phase2 roadmap.

- `src/hooks/worker-poster.ts` — `postEvent()` posts `create_post` JSON-RPC calls to the blog MCP server on AO lifecycle events
- `src/hooks/index.ts` — exports `postEvent` and `WorkerEvent` for easy consumption
- `tests/worker-poster.test.ts` — 4 unit tests using `vi.fn()` mock for fetch

## Metadata
- **PR**: #9
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +465/-0 in 14 files
- **Labels**: none

## Connections
