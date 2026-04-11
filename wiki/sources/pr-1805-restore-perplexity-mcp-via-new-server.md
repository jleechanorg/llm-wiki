---
title: "PR #1805: Restore Perplexity MCP via new server"
type: source
tags: [codex]
date: 2025-10-02
source_file: raw/prs-worldarchitect-ai/pr-1805.md
sources: []
last_updated: 2025-10-02
---

## Summary
- reintroduce Perplexity coverage in `/perp`, `/presentation`, `/research`, and related orchestration docs using the new `perplexity_search_web` tool
- update `claude_mcp.sh`, token loading, and MCP search tests to install and validate the `@jschuller/perplexity-mcp` server when a Perplexity API key is present
- adjust the MCP health check to treat Perplexity as a premium server while maintaining backward compatibility with the legacy name

## Metadata
- **PR**: #1805
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +180/-101 in 11 files
- **Labels**: codex

## Connections
