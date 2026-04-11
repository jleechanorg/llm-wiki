---
title: "Rate Limiting Logic Unit Tests"
type: source
tags: [python, testing, unit-tests, rate-limiting, firestore]
source_file: "raw/test_rate_limiting.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests covering rate limiting logic in the mvp_site rate_limiting module. Tests verify email exemption parsing, BYOK provider detection, user turn limit calculation, and rate limit checking with Firestore integration.


## Key Claims
- **Email exemption parsing**: _parse_rate_limit_exempt_emails correctly handles None, empty strings, and comma-separated email lists.
- **Rate limit exemption**: is_rate_limit_exempt checks if email is in RATE_LIMIT_EXEMPT_EMAILS set (case-insensitive).
- **BYOK provider detection**: is_byok_provider_active checks if user settings have matching API key for their provider.
- **Default turn limits**: Non-BYOK users receive RATE_LIMIT_DAILY_TURNS and RATE_LIMIT_5HOUR_TURNS.
- **Elevated turn limits**: BYOK users receive RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS and RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS.
- **Rate limit checking**: check_rate_limit returns allowed status with daily remaining count.
- **Firestore integration**: Rate limit documents stored in rate_limits collection.

## Connections
- [[RateLimiting]] — core rate limiting concept
- [[BYOK]] — Bring Your Own Key model with elevated limits
- [[FirestoreService]] — database backing rate limit storage
