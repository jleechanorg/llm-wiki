---
title: "PR #31: feat(blog): IP-based rate limiting (design doc Section C)"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-31.md
sources: []
last_updated: 2026-03-29
---

## Summary
The living blog design doc (Section C, Rate limiting) specifies IP-based rate limits for the MCP server:
- Global: 100 req/min/IP
- Write operations: 20 req/min/IP  
- `chat_worker`: 10 req/min/IP

This was not yet implemented in any open PR.

## Metadata
- **PR**: #31
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +150/-4 in 5 files
- **Labels**: none

## Connections
