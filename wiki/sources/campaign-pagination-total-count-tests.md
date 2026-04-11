---
title: "Campaign Pagination Total Count Tests"
type: source
tags: [python, testing, unittest, pagination, campaigns, firestore]
source_file: "raw/test_campaign_pagination_total_count.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite testing total campaign count functionality in pagination. Validates that total_count is calculated only on the first page (include_total_count=True) and not calculated on subsequent pages (include_total_count=False) for performance optimization.

## Key Claims
- **First Page Total Count**: total_count included when start_after is not provided (first page request)
- **Subsequent Pages Skip Total**: total_count not calculated on subsequent pages to avoid expensive aggregation queries
- **API Response Integration**: total_count included in API response when available
- **Graceful Handling**: Handles aggregation failures without breaking pagination
- **Performance Optimization**: Only calculates total when necessary to avoid Firestore aggregation overhead

## Key Quotes
> "Test that total_count is included in response on first page" — test_total_count_included_on_first_page

> "include_total_count should be True on first page" — assertion in test

> "include_total_count should be False on subsequent pages" — assertion in test

## Connections
- [[Campaign Pagination MCP with Evidence Bundles]] — related pagination test
- [[Firestore Query Optimization]] — backend implementation for pagination

## Contradictions
- None identified
