---
title: "PR #289: feat: share second opinion latency instrumentation"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-289.md
sources: []
last_updated: 2025-10-13
---

## Summary
- add per-stage and per-model latency instrumentation to the second-opinion flow with structured logging and persistence
- relocate the latency tracker implementation and tests into @ai-universe/mcp-server-utils with a shared verbose logging flag
- document the MCP_VERBOSE_LATENCY_LOGGING toggle for backend consumers and ensure logger wiring flows through the shared utility

## Metadata
- **PR**: #289
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +469/-38 in 7 files
- **Labels**: codex

## Connections
