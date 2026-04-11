---
title: "PR #3967: fix: Remove mcpServers from .claude/settings.json"
type: source
tags: []
date: 2026-01-23
source_file: raw/prs-worldarchitect-ai/pr-3967.md
sources: []
last_updated: 2026-01-23
---

## Summary
- Removed incorrect `mcpServers` section from `.claude/settings.json`
- Follows Claude CLI best practices: MCP servers belong in `~/.claude.json` (user-scoped) or `.mcp.json` (project-scoped)
- Per [GitHub issue #4976](https://github.com/anthropics/claude-code/issues/4976), the documentation was incorrect about MCP configuration location

## Metadata
- **PR**: #3967
- **Merged**: 2026-01-23
- **Author**: jleechan2015
- **Stats**: +0/-74 in 1 files
- **Labels**: none

## Connections
