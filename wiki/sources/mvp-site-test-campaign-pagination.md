---
title: "test_campaign_pagination.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Tests for campaign list pagination functionality - cursor-based pagination with default limit of 50 campaigns.

## Key Claims
- Default limit is 50 campaigns (display full list with minimal fields)
- Query selects only required fields: title, created_at, last_played, initial_prompt, prompt
- initial_prompt returned for snippet display, truncated to 103 chars (100 + "...") for large prompts
- Cursor structure: timestamp and id fields
- has_more flag accurate, next_cursor is None when no more results
- get_campaigns_list_unified returns pagination metadata
- Fallback logic uses "<=" for duplicate timestamps

## Connections
- [[firestore_service]] — provides get_campaigns_for_user
- [[world_logic]] — provides get_campaigns_list_unified