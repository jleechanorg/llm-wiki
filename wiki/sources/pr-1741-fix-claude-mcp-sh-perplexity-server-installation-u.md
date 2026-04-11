---
title: "PR #1741: Fix claude_mcp.sh Perplexity Server Installation - Use Working Package"
type: source
tags: []
date: 2025-09-25
source_file: raw/prs-worldarchitect-ai/pr-1741.md
sources: []
last_updated: 2025-09-25
---

## Summary
✅ **CRITICAL FIX**: Update claude_mcp.sh to install the working Perplexity MCP server package instead of the problematic one causing 401 authentication errors

**Problem Solved**:
- Original `server-perplexity-ask` package causes persistent 401 Unauthorized errors
- Users experience "total failure" with Perplexity MCP integration out of the box  
- Fresh installations via claude_mcp.sh get non-functional Perplexity servers

**Solution Implemented**:
- Replace `server-perplexity-ask` with working

## Metadata
- **PR**: #1741
- **Merged**: 2025-09-25
- **Author**: jleechan2015
- **Stats**: +7/-5 in 1 files
- **Labels**: none

## Connections
