---
title: "Error Handling"
type: concept
tags: [error-handling, api, exceptions]
sources: []
last_updated: 2026-04-08
---

Error handling patterns in LLM service API calls. Covers ContextTooLargeError, provider overload (503), rate limit (429), and general API errors. Errors are wrapped in LLMRequestError with appropriate HTTP status codes.

## Connections
- [LLMService](LLMService.md) — module implementing error handling
- [ContextTooLargeError](ContextTooLargeError.md) — error for token limit exceeded
- [LLMRequestError](LLMRequestError.md) — custom exception for API errors
