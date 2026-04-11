---
title: "PR #1848: fix: ensure codex MCP servers register env blocks correctly"
type: source
tags: []
date: 2025-10-08
source_file: raw/prs-worldarchitect-ai/pr-1848.md
sources: []
last_updated: 2025-10-08
---

## Summary
- keep CLI args before env blocks when invoking `mcp add` to avoid swallowing `--stdio` and other arguments
- ensure all helper installs reuse cached env arrays instead of rebuilding order-specific lists
- fix memory/perplexity/worldarchitect setups to register their environment variables without leaking positional params

## Metadata
- **PR**: #1848
- **Merged**: 2025-10-08
- **Author**: jleechan2015
- **Stats**: +17/-11 in 1 files
- **Labels**: none

## Connections
