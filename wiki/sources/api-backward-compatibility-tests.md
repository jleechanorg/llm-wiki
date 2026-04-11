---
title: "Test API Backward Compatibility"
type: source
tags: [python, testing, unittest, api, backward-compatibility, firestore, firebase]
source_file: "raw/api-backward-compatibility-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file that ensures API responses maintain backward compatibility with legacy frontend code. Tests the /api/campaigns endpoint to verify it returns an array directly rather than wrapped in an object, which prevents breaking changes like JavaScript forEach errors.

## Key Claims
- **Array Response Format**: /api/campaigns must return array directly for backward compatibility with legacy frontend code using forEach
- **No Object Wrapper**: API must NOT return object wrapper like {"campaigns": [...], "success": true}
- **forEach Compatibility**: Response format must support JavaScript forEach operation without TypeError
- **Firebase Mocking**: Uses FakeFirestoreClient for testing without real Firebase credentials
- **Authentication Enforcement**: Properly enforces authentication requirements in the API

## Key Quotes
> "campaigns.forEach(...); // Expects campaigns to be an array" — legacy frontend expectation

## Connections
- [[Firebase]] — mocked for testing without credentials
- [[Google]] — parent company of Firebase/auth services
- [[FakeFirestoreClient]] — test implementation for Firestore
- [[APIBackwardCompatibility]] — concept for maintaining legacy frontend support

## Contradictions
- []
