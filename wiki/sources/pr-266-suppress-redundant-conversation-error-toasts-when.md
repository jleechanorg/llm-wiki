---
title: "PR #266: Suppress redundant conversation error toasts when MCP offline"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-266.md
sources: []
last_updated: 2025-11-17
---

## Summary
- treat conversation errors as secondary signals and suppress them whenever the MCP transport is already reporting an outage so we only surface the underlying connection failure once
- keep the existing toast dedupe helper but make placeholders/error badges derive from the filtered conversation error state so users no longer see duplicate "Load failed" messaging

## Metadata
- **PR**: #266
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +35/-7 in 2 files
- **Labels**: codex

## Connections
