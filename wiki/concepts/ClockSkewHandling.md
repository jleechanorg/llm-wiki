---
title: "Clock Skew Handling"
type: concept
tags: [authentication, time, jwt]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
Detection and handling of JWT "Token used too early" errors that occur when client system time differs from server time.

## Implementation
- isClockSkewError function detects specific error message
- Triggers forceRefresh to obtain new token
- Initiates recursive retry with incremented retryCount

## Related Concepts
- [[AutoRetryMechanism]] — retry logic triggered by clock skew
- [[JWT]] — token system experiencing skew
