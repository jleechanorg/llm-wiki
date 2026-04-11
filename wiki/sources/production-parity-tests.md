---
title: "Production Parity Tests"
type: source
tags: [python, testing, production, firebase, frontend, compatibility]
source_file: "raw/test_production_parity.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Tests that catch differences between test and production environments, specifically response format compatibility issues. Validates campaigns list endpoint response structure and direct calls mode response format.

## Key Claims
- **Campaigns list response format**: Frontend expects `const { data: campaigns } = await fetchApi('/api/campaigns')` destructuring to work — response must be either directly an array or have a `campaigns` field.
- **Direct calls mode**: Production configuration where world_logic.py functions are called directly without HTTP overhead must maintain response format compatibility.
- **Firebase credentials detection**: Tests check for GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_SERVICE_ACCOUNT_KEY, or application default credentials before running.

## Key Quotes
> "This is the critical test - verify frontend expectations"

## Connections
- [[Firebase]] — mocked in tests to prevent initialization errors
- [[Firestore]] — fake client used for test isolation

## Contradictions
- None identified
