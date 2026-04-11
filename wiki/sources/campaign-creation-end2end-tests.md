---
title: "Campaign Creation End-to-End Integration Tests"
type: source
tags: [python, testing, e2e, integration, campaign-creation, flask, mocking]
source_file: "raw/test_campaign_creation_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test suite for campaign creation through the full application stack. Tests validate the complete flow from API endpoint through all service layers, with external services (Gemini API and Firestore DB) mocked at the lowest level.

## Key Claims
- **Full Stack Testing**: Tests entire request pipeline from `/api/campaigns` POST endpoint through service layers
- **Mock Strategy**: Mocks external services at lowest level to test real integration points
- **Dual Test Coverage**: Tests both successful campaign creation and error handling paths
- **Auth Stubbing**: Uses `TESTING_AUTH_BYPASS` for authentication bypass in tests

## Key Quotes
> "With testing mode removed, expect 401 (auth required) or 201 if properly mocked"

## Connections
- [[End2EndBaseTestCase]] — base test case providing test client and authentication headers
- [[FakeFirestoreClient]] — fake Firestore implementation for testing database operations
- [[FakeLLMResponse]] — fake LLM response object for mocking Gemini API responses
- [[CampaignCreationV2]] — production component being tested

## Contradictions
- []
