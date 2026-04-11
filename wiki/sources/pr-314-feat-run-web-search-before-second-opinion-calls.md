---
title: "PR #314: feat: run web search before second opinion calls"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-314.md
sources: []
last_updated: 2025-10-13
---

## Summary
- add a shared helper in mcp-server-utils to run web search and build prompt context for second opinion flows
- have SecondOpinionAgent call the helper before dispatching to the primary and secondary models, recording telemetry about search results
- cover the helper with unit tests and export it through the shared package entry point
- tighten web search sanitization and align streaming telemetry to avoid duplicate context blocks while capturing stage latency

## Metadata
- **PR**: #314
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +66/-10 in 3 files
- **Labels**: codex

## Connections
