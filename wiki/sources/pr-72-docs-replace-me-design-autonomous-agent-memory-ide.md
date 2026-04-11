---
title: "PR #72: docs: Replace Me design — autonomous agent memory & identity"
type: source
tags: []
date: 2026-03-10
source_file: raw/prs-worldai_claw/pr-72.md
sources: []
last_updated: 2026-03-10
---

## Summary
- Augment OpenClaw memory: `memoryFlush` now writes to both MEMORY.md (existing) AND a structured knowledge graph (`memory-server` MCP)
- Add 7 `memory-server_*` tools to `alsoAllow` enabling OpenClaw to write/query the graph at compaction
- 12-question memory quality test suite — 12/12 passing
- Phased memory upgrade roadmap (daily cron → knowledge graph → Zoe context injection)

## Metadata
- **PR**: #72
- **Merged**: 2026-03-10
- **Author**: jleechan2015
- **Stats**: +3476/-82 in 35 files
- **Labels**: none

## Connections
