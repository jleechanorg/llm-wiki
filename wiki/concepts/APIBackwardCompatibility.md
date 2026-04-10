---
title: "API Backward Compatibility"
type: concept
tags: [api, compatibility, testing, frontend, legacy]
sources: [api-backward-compatibility-tests]
last_updated: 2026-04-08
---

## Definition
Practice of maintaining consistent API response formats to ensure existing frontend code continues to work after backend changes. Critical for preventing runtime errors like JavaScript forEach failing on object instead of array.

## Key Principles
- Response format changes require comprehensive test coverage
- Legacy format takes precedence over cleaner new formats
- Frontend code expectations must be documented and tested

## Related Concepts
- [[LegacyCodeSupport]] — maintaining support for older client versions
- [[ContractTesting]] — verifying API contracts don't break
---
