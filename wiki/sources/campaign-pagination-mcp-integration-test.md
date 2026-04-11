---
title: "Campaign Pagination MCP Integration Test with Evidence Bundles"
type: source
tags: [python, testing, mcp, pagination, evidence-bundles, firestore]
source_file: "raw/test_campaign_pagination_mcp_bundle.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite testing campaign pagination through MCP protocol with evidence bundle generation per evidence-standards.md. Validates pagination metadata (has_more, next_cursor), cursor-based pagination efficiency, and Firestore query behavior.


## Key Claims
- **Pagination Metadata**: Response includes has_more and next_cursor fields for client-side pagination
- **Default Limit**: 50 campaigns per page by default
- **Cursor-Based Pagination**: Efficient Firestore queries using document cursors
- **Evidence Bundles**: Captures request/response pairs with timestamps and provenance data
- **MCP Protocol**: Uses tools_call_async for async MCP tool invocation

## Key Quotes
> "Default limit: 50 campaigns per page" — test source
> "cursor-based pagination" — test source

## Connections
- [[CampaignListClickFunctionalityTests]] — related campaign list testing
- [[Firestore]] — backend storage for campaign persistence

## Contradictions
- None identified
