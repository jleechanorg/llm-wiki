---
title: "Campaign Pagination"
type: concept
tags: [pagination, campaigns, api, firestore]
sources: []
last_updated: 2026-04-08
---

## Definition
A technique for retrieving large sets of campaign data in manageable chunks using cursor-based pagination instead of offset-based approaches.

## Key Properties
- **Cursor-Based**: Uses document cursors (timestamp + id) for efficient pagination
- **Default Limit**: 50 campaigns per page
- **Metadata Fields**: has_more, next_cursor for client-side pagination control
- **Total Count Optimization**: Calculates total_count only on first page

## Related Concepts
- [[CursorBasedPagination]] — technical implementation
- [[FirestoreQueryOptimization]] — backend efficiency patterns

## Used In
- Campaign list API endpoints
- Campaign management interfaces
