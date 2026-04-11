---
title: "PR #90: refactor: share FastMCP server factory"
type: source
tags: [codex]
date: 2025-09-29
source_file: raw/prs-/pr-90.md
sources: []
last_updated: 2025-09-29
---

## Summary
- extract the FastMCP server bootstrap logic into `backend/src/createFastMCPServer.ts` for reuse
- update both the HTTP and stdio entrypoints to import the shared factory and remove duplicated tool/agent setup

## Metadata
- **PR**: #90
- **Merged**: 2025-09-29
- **Author**: jleechan2015
- **Stats**: +8457/-1181 in 23 files
- **Labels**: codex

## Connections
