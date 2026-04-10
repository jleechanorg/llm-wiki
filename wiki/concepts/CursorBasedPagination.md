---
title: "Cursor-Based Pagination"
type: concept
tags: [pagination, database, firestore, performance]
sources: []
last_updated: 2026-04-08
---

## Description
Cursor-based pagination is a technique where each page of results is fetched using a cursor (typically the last document's ID or a timestamp) rather than offset-based pagination. This is more efficient for large datasets as it avoids re-counting skipped rows.

## Key Benefits
- Performance: O(1) vs O(n) for offset-based pagination
- Consistency: Stable results even with data changes during pagination
- Efficiency: Only fetches needed fields

## Implementation
- Uses `start_after` parameter with last document's cursor
- Returns `has_more` flag and `next_cursor` for client-side pagination
- [[FirestoreService]] implements this for campaign lists
