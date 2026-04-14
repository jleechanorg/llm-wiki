---
title: "test_campaign_pagination_end2end.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
End-to-end integration tests for campaign pagination. Tests full flow from API endpoint through all service layers, only mocks Firestore DB.

## Key Claims
- First page returns 50 campaigns with cursor when 60+ exist
- Second page loads using cursor with start_after_timestamp and start_after_id parameters
- total_count included on first page
- has_more is False when all campaigns fit in one page
- Custom limit parameter works (e.g., limit=25)
- Empty user returns empty array with has_more=False
- Non-paginated requests return array directly (backward compatibility)
- Multiple pages can be loaded sequentially

## Connections
- [[main]] — Flask app being tested
- [[FakeFirestoreClient]] — test mock
- [[test_end2end]] — base test case