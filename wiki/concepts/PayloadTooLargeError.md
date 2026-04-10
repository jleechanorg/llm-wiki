---
title: "PayloadTooLargeError"
type: concept
tags: [python, exception, payload, size]
sources: [llm-request-validation-tests]
last_updated: 2026-04-08
---

## Definition
Exception raised when the JSON payload exceeds MAX_PAYLOAD_SIZE limit. Indicates the request body is too large to send to the LLM API.

## Related Concepts
- [[LLMRequest]] — class that raises this error
- [[ValidationError]] — related exception for field validation
- [[MAX_PAYLOAD_SIZE]] — constant defining the size limit
