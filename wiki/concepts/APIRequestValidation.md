---
title: "API Request Validation"
type: concept
tags: [validation, api, error-handling, data-integrity]
sources: [llm-request-class-gemini-api.md]
last_updated: 2026-04-08
---

## Definition
A validation-first design pattern for API requests that checks required fields, data types, and payload size before sending to the API, raising custom exceptions with appropriate error codes.

## Implementation in This Source
The LLMRequest class uses dataclass `__post_init__` to validate:
- Required fields (user_id, game_mode) cannot be empty/whitespace
- Field types must match expected types (dict, list)
- String lengths must not exceed MAX_STRING_LENGTH (1MB)
- Total payload must not exceed MAX_PAYLOAD_SIZE (10MB)

## Exception Hierarchy
- `LLMRequestError` (base) — status_code parameter for HTTP response
- `PayloadTooLargeError` — payload exceeds size limits
- `ValidationError` — field validation failures

## Related Concepts
- [[Input Validation Utilities]] — UUID/format validation patterns
- [[Enhanced Post-Generation Validation with Retry]] — validation for generated content
