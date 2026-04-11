---
title: "PR #77: feat: add Morgan logging + fix MCP race condition, favicon, and COOP headers"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-/pr-77.md
sources: []
last_updated: 2025-10-30
---

## Summary
This PR includes two major contributions:

### 1. **Morgan Proxy Logging** (Original Work)
- Install Morgan and register request/response logging with proxy-specific tokens
- Add detailed start/finish logging around `/api/mcp` proxy handling with response size and timing metrics
- Capture proxy errors with centralized error-logging middleware
- Sanitize sensitive headers (authorization, cookie, x-api-key, etc.)

### 2. **Critical Bug Fixes** (New Work)
- **Fix MCP client race condition** during

## Metadata
- **PR**: #77
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +1107/-32 in 13 files
- **Labels**: codex

## Connections
