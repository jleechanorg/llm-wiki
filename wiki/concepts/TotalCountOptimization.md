---
title: "Total Count Optimization"
type: concept
tags: [performance, pagination, aggregation, firestore]
sources: []
last_updated: 2026-04-08
---

## Definition
A performance optimization strategy where expensive aggregation queries (counting total records) are only executed when necessary — specifically on the first page of paginated results.

## Key Properties
- **First Page**: include_total_count=True triggers aggregation query
- **Subsequent Pages**: include_total_count=False skips aggregation
- **Performance Impact**: Avoids Firestore COUNT aggregation on every request
- **Client Experience**: Users see total count on initial load without slower subsequent pages

## Why It Works
Firestore aggregation queries are expensive. By only calculating total_count on first page load, subsequent page fetches remain fast while users still get the total count information.

## Related Concepts
- [[CampaignPagination]] — the feature this optimizes
- [[FirestoreQueryOptimization]] — underlying query patterns
