---
title: "mvp_site rate_limiting"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/rate_limiting.py
---

## Summary
Rate limiting logic separating business logic from Firestore service. Implements daily and 5-hour turn limits using TTLCache. jleechan@gmail.com is always exempt. Configurable via environment variables.

## Key Claims
- RATE_LIMIT_DAILY_TURNS = 50 (configurable via RATE_LIMIT_DAILY_TURNS env var)
- RATE_LIMIT_5HOUR_TURNS = 25 (configurable via RATE_LIMIT_5HOUR_TURNS env var)
- RATE_LIMIT_EXEMPT_EMAILS always includes jleechan@gmail.com
- Uses cachetools TTLCache for in-memory rate limit tracking

## Connections
- [[Validation]] — rate limiting for API usage
