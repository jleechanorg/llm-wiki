---
title: "Campaign List Pagination Tests"
type: source
tags: [python, testing, unittest, pagination, campaigns, firestore]
source_file: "raw/test_campaign_pagination_list.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite testing campaign list pagination functionality with cursor-based pagination. Validates default limit of 50 campaigns per page, custom limit support, and minimal field selection for query efficiency.

## Key Claims
- **Default Limit 50**: Default limit is 50 campaigns per page for display full list with minimal fields
- **Custom Limit**: Custom limit parameter allows specifying different page sizes
- **Minimal Field Selection**: Campaigns query selects only required fields (title, last_played) for efficiency
- **Cursor-Based Pagination**: Uses Firestore document cursors for efficient pagination
- **has_more Flag**: Indicates whether more results exist beyond current page
- **next_cursor**: Provides cursor for fetching next page of results

## Test Methods
- `test_default_limit_is_50` - Validates default 50 campaign limit
- `test_custom_limit` - Validates custom limit parameter
- `test_campaign_list_selects_minimal_fields` - Validates minimal field selection

## Connections
- [[FirestoreService]] - Service being tested for campaign retrieval
- [[MVPSite]] - Project containing the pagination logic
- [[CursorBasedPagination]] - Pagination technique used
