---
title: "PR #1906: feat: Add Secondo MCP server plugin for Claude Code"
type: source
tags: []
date: 2025-10-30
source_file: raw/prs-worldarchitect-ai/pr-1906.md
sources: []
last_updated: 2025-10-30
---

## Summary
Creates a Model Context Protocol (MCP) server plugin for the `/secondo` command, enabling system-wide installation via Claude Code's `/plugin install` workflow.

**Key Changes:**
- ✅ MCP server with Express (implements GET /tools, POST /execute endpoints)
- ✅ Plugin manifest for Claude Code plugin system
- ✅ Wraps existing secondo-cli.sh (no code duplication)
- ✅ OAuth authentication via auth-cli.mjs
- ✅ Comprehensive documentation with architecture diagrams
- ✅ Fixed /localexportcommands to exp

## Metadata
- **PR**: #1906
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +2147/-5 in 10 files
- **Labels**: none

## Connections
