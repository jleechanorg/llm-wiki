---
title: "PR #1835: MCP: automate campaign testing and harden Firestore integration"
type: source
tags: []
date: 2025-10-08
source_file: raw/prs-worldarchitect-ai/pr-1835.md
sources: []
last_updated: 2025-10-08
---

## Summary
- move the MCP HTTP endpoint from `/rpc` to `/mcp`, updating the server, client, CLI scripts, docs, and sample configs while returning 410 on the old path
- harden Firestore access by replacing ad-hoc in-module mocks with an in-memory client for `MOCK_SERVICES_MODE`, adding write verification and stricter UTC handling, and smoothing legacy imports through shims
- refactor deployment utilities (shared `deploy_common.sh`, revamped `deploy.sh`/`deploy_mcp.sh`, expanded `claude_mcp.sh`) and expand t

## Metadata
- **PR**: #1835
- **Merged**: 2025-10-08
- **Author**: jleechan2015
- **Stats**: +1055/-560 in 26 files
- **Labels**: none

## Connections
