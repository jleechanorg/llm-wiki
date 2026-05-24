---
title: "Retry Logic"
type: concept
tags: [gemini, api, error-handling, reliability]
sources: ["gemini-api-retry-logic-tests"]
last_updated: 2026-04-08
---

## Description
Pattern for handling transient failures in Gemini API calls. Includes error classification to determine if an error is retriable, exponential backoff with configurable delays, and user-visible warning injection after successful retries.

## Key Functions
- **_is_retriable_gemini_error**: Classifies errors - FAILED_PRECONDITION is retriable, PERMISSION_DENIED/INVALID_ARGUMENT/RESOURCE_EXHAUSTED are not
- **_log_retry_attempt**: Logs retry attempts at WARNING level with model name, attempt count, and error details
- **_add_api_retry_warning_to_response**: Injects user-visible warning after retry success

## Constants
- GEMINI_RETRIABLE_STATUSES
- GEMINI_RETRY_BASE_DELAY_SECONDS
- GEMINI_RETRY_MAX_ATTEMPTS

## Mutating vs. Idempotent Retry (2026-05-24)

**Critical distinction**: stream path (`/interaction/stream`) is mutating — it writes to Firestore. Retrying `ConnectionResetError` on a mutating path duplicates game effects (double dice rolls, double story entries).

Fix: injectable `is_retryable_fn` param in `_run_with_transport_retry`. Stream path passes `_is_stream_retryable_transport_error` (only pre-connection failures: `ConnectionRefused`, `"Errno 61"`). Non-stream path uses default `_is_mcp_transient_transport_error` (includes `ConnectionResetError`).

Source: PR #7074 commit `c02561c7b1`, `testing_mcp/lib/base_test.py`.

## Connections
- [[GeminiLLMService]] — implements retry logic
- [[PR4099]] — introduced retry logic
- [[ErrorClassification]] — determines retry eligibility
