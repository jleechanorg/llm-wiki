---
title: "Action Resolution Backward Compatibility End-to-End Test"
type: source
tags: [python, testing, end-to-end, backward-compatibility, api, firestore, gemini]
source_file: "raw/action-resolution-backward-compat-end2end-test.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file testing the full application stack flow from LLM response through API to ensure backward compatibility between outcome_resolution and action_resolution fields, plus null safety in API responses. Only mocks external services (Gemini API and Firestore DB) at the lowest level.

## Key Claims
- **Backward Compatibility**: Tests that outcome_resolution maps to action_resolution for legacy support
- **Null Safety**: Validates that None values don't leak to API responses
- **Unified Response**: Verifies both fields appear in unified_response when present
- **Property Fallback**: Tests llm_response.action_resolution property falls back correctly
- **Low-Level Mocking**: Uses FakeFirestoreClient and FakeLLMResponse for test isolation

## Key Test Scenarios
- action_resolution (new field) appears in API response
- outcome_resolution (legacy field) maps to action_resolution
- Both fields coexist in unified_response
- Null values properly handled and not exposed

## Connections
- [[FakeFirestoreClient]] — mock Firestore client for test isolation
- [[FakeLLMResponse]] — mock LLM response builder
- [[End2EndBaseTestCase]] — base test case class
- [[Unified Response Format]] — combined response structure

## Contradictions
- None identified
