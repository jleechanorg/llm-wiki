---
title: "fix(mcp): use worldai_mcp_stdio as entry point for global install"
type: source
tags: [worldarchitect.ai, mcp, stdio, entry-point, packaging]
date: 2026-04-11
source_file: raw/worldarchitect.ai/pr-6213.md
---

## Summary
Changes the `worldarchitect-mcp` global CLI entry point from `mvp_site.mcp_api:run_server` to `mvp_site.worldai_mcp_stdio:main`. This enables proper global uv installation while retaining admin tools like `admin_download_campaign`. The MCP now uses the WorldAIToolsProxy stdio adapter instead of the full game logic server.

## Key Claims
- Global `worldarchitect-mcp` command now works without requiring repo cwd
- Admin tools (admin_download_campaign, etc.) remain accessible via MCP
- The stdio-based proxy adapter is the new runtime mode

## Key Quotes
> "Switches the `worldarchitect-mcp` global CLI entry point in `setup.py` from `mvp_site.mcp_api:run_server` to `mvp_site.worldai_mcp_stdio:main`"

## Connections
- [[worldarchitect-ai-MCP]] — MCP entry point change
- [[worldai-mcp-stdio]] — New stdio adapter module

## Changed Files
- setup.py: Entry point changed (+1 line, -1 line)
