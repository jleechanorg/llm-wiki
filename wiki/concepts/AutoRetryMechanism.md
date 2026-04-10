---
title: "Auto-Retry Mechanism"
type: concept
tags: [resilience, retry, error-handling]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
Automatic retry logic in api.js that handles transient failures by retrying failed requests with fresh authentication tokens.

## Implementation Details
- retryCount parameter limits retries (retryCount < 2)
- Triggered by 401 response status
- Calls fetchApi(path, options, retryCount + 1) recursively
- forceRefresh obtains new JWT token before retry

## Related Entities
- [[ApiJs]] — implements the mechanism
- [[JWT]] — token refreshed on retry
