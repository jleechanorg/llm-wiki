---
title: "PR #1619: Reduce MCP server verbosity"
type: source
tags: [codex]
date: 2025-09-19
source_file: raw/prs-worldarchitect-ai/pr-1619.md
sources: []
last_updated: 2025-09-19
---

## Summary
- add shared environment flags in `claude_mcp.sh` to suppress verbose MCP tool discovery logs
- propagate the quiet flags to all MCP server registrations and the fallback memory wrapper script
- ensure every `claude mcp add` invocation passes the quiet flags before the server name so the CLI honors them

## Metadata
- **PR**: #1619
- **Merged**: 2025-09-19
- **Author**: jleechan2015
- **Stats**: +33/-17 in 1 files
- **Labels**: codex

## Connections
