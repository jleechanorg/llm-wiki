---
title: "PR #603: Remove redundant .mcp.json configuration file"
type: source
tags: []
date: 2025-07-15
source_file: raw/prs-worldarchitect-ai/pr-603.md
sources: []
last_updated: 2025-07-15
---

## Summary
- Remove outdated `.mcp.json` file that was incomplete and redundant
- Claude CLI manages MCP servers directly via `claude mcp add/list` commands  
- The `.mcp.json` only contained 5 servers while Claude CLI registry has 9 servers
- Eliminates confusion between two MCP configuration systems

## Metadata
- **PR**: #603
- **Merged**: 2025-07-15
- **Author**: jleechan2015
- **Stats**: +0/-45 in 1 files
- **Labels**: none

## Connections
