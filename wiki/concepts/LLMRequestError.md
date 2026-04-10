---
title: "LLMRequestError"
type: concept
tags: [error-handling, http, api]
sources: []
last_updated: 2026-04-08
---

Custom exception class for LLM API request failures. Carries HTTP status code and error message. Used to convert provider-specific errors into standardized HTTP responses.

## Usage
- 422 status: ContextTooLargeError conversion
- 500 status: Generic provider failures

## Related Concepts
- [[ContextTooLargeError]] — converted to this for HTTP standardization
- [[Provider Fallback]] — graceful degradation when primary provider fails
