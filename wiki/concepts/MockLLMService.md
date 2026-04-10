---
title: "Mock LLM Service"
type: concept
tags: [testing, mock, llm, gemini, api-mocking]
sources: [mock-gemini-api-service-function-testing]
last_updated: 2026-04-08
---

## Description
Testing pattern that provides a mock implementation of an LLM service API. Enables tests to run in isolation without making actual API calls, improving test speed and reliability.

## Key Benefits
- **Test Isolation**: Tests run without external API dependencies
- **Deterministic Responses**: Consistent responses for repeatable tests
- **Edge Case Testing**: Can force specific response patterns for error handling tests
- **Fast Execution**: No network latency or API rate limits

## Implementations
- [[MockLLMClient]] — pattern-based mock client
- [[MockGeminiServiceWrapper]] — alternative wrapper implementation

## Related Patterns
- [[TestFixtures]] — static test data
- [[ServiceMocking]] — general service mocking pattern
