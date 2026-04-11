---
title: "LLM Service Error Handling Tests"
type: source
tags: [python, testing, llm-service, error-handling]
source_file: "raw/test_llm_service_error_handling.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating llm_service._call_llm_api error handling, covering mock mode response validation, context-too-large errors, provider overload errors without retry, and rate limit errors without retry.

## Key Claims
- **Mock mode response schema**: Validates planning_block contains valid choices schema with text and description fields
- **ContextTooLargeError surfaces as 422**: When context exceeds limits, raises LLMRequestError with status_code 422
- **Provider overload surfaces as 503 without retry**: Overloaded provider error propagates immediately with 503 status
- **Rate limit surfaces as 429 without retry**: Rate limit error propagates with 429 status and "rate limit" message
- **Error diagnostics includes status code**: Error logging includes the API error code for debugging

## Key Test Cases
- test_mock_mode_response_contains_valid_planning_choice_schema: Validates mock mode returns valid planning_choice schema
- test_model_call_surfaces_context_too_large_error: Tests ContextTooLargeError raises 422
- test_model_call_surfaces_provider_overload_without_retry: Tests 503 error without retry logic
- test_model_call_surfaces_rate_limit_without_retry: Tests 429 rate limit error
- test_error_code_type_validation_with_valid_int: Tests error.code conversion to int


## Connections
- [[LLMResponse Object TDD Tests]] — related test suite for LLM response parsing
- [[Provider Settings Selection Tests]] — provider configuration tests
