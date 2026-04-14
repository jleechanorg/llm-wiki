---
title: "test_campaign_pagination_mcp.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Integration tests for campaign pagination through MCP protocol interface. Tests end-to-end pagination works correctly through the MCP tool interface.

## Key Claims
- MCP get_campaigns_list returns first page with pagination metadata (50 campaigns, has_more=True, next_cursor)
- MCP returns second page using cursor parameters (start_after timestamp and id)
- MCP returns has_more=False when no more results
- Empty user returns empty campaigns array

## Connections
- [[world_logic]] — provides get_campaigns_list_unified