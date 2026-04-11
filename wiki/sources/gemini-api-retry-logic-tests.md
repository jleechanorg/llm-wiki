---
title: "Gemini API Retry Logic Tests"
type: source
tags: [python, testing, gemini, retry, bug-fix, pr-4099]
source_file: "raw/test_gemini_api_retry_logic.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for Gemini API retry logic in llm_service. Tests the retry functions added in PR #4099 including error classification, retry logging, and user-visible warning injection after successful retries.

## Key Claims
- **_is_retriable_gemini_error**: Returns True for FAILED_PRECONDITION status, falls back to string check, returns False for PERMISSION_DENIED, INVALID_ARGUMENT, RESOURCE_EXHAUSTED
- **_log_retry_attempt**: Logs at WARNING level with attempt count, model name, error status, and delay
- **_add_api_retry_warning_to_response**: Adds user-visible warning after retry succeeds
- **Constants**: GEMINI_RETRIABLE_STATUSES, GEMINI_RETRY_BASE_DELAY_SECONDS, GEMINI_RETRY_MAX_ATTEMPTS

## Key Quotes
> "Related commits: a1a2d8c83, 34315e3a7"

## Connections
- [[GeminiLLMService]] — module under test
- [[PR4099]] — PR that introduced retry logic
- [[RetryLogic]] — concept for retry behavior
- [[ErrorClassification]] — concept for error type determination

## Contradictions
- None detected
