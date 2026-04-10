---
title: "Rate Limiting"
type: concept
tags: [rate-limiting, throttling, access-control]
sources: []
last_updated: 2026-04-08
---

## Summary
Rate limiting controls how many requests a user can make within a time window. The system enforces daily turn limits (24-hour reset) and 5-hour window limits.

## Implementation
- **Daily limit**: RATE_LIMIT_DAILY_TURNS - total turns per day
- **5-hour window**: RATE_LIMIT_5HOUR_TURNS - turns within any 5-hour period
- **Email exemption**: Certain emails bypass rate limiting entirely via RATE_LIMIT_EXEMPT_EMAILS set
- **BYOK users**: Elevated limits for users providing their own API key

## Related Concepts
- [[BYOK]] - Bring Your Own Key model
- [[FirestoreService]] - Database storage for rate limit tracking
