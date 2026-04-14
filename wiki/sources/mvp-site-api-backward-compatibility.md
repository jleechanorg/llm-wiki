---
title: "test_api_backward_compatibility.py"
type: source
tags: [testing, api, backward-compatibility, frontend]
date: 2026-04-14
source_file: raw/mvp_site_all/test_api_backward_compatibility.py
---

## Summary
Tests that API responses maintain backward compatibility with legacy frontend code. Critical for preventing breaking changes like forEach errors where frontend expects array directly, not wrapped in object.

## Key Claims
- GET /api/campaigns returns array directly: [campaign1, campaign2, ...]
- NOT wrapped as: {"campaigns": [...], "success": true}
- Response must support JavaScript forEach operation without TypeError
- POST /api/campaigns returns object with success field
- Testing mode removed - proper authentication now required

## Key Quotes
> "API must return array directly for backward compatibility"

## Connections
- [[mvp-site-main]] — Flask app with API endpoints
- [[mvp-site-firestore-service]] — Campaign data persistence

## Contradictions
- None identified in test file