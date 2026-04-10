---
---
title: "Request Timeout"
type: concept
tags: [api, networking, timeout, configuration]
sources: []
last_updated: 2026-04-08
---

Request timeout configuration for API calls, centralized to align browser client with backend and Cloud Run limits.


## Default Configuration
- **Standard requests**: 600000ms (10 minutes)
- **Health checks**: 5000ms (5 seconds) — fast to avoid masking backend outages

## Implementation
- Mirrors timeout_config.sh exports from backend
- Supports caller-provided timeout override
- Uses AbortController for timeout cancellation
- Chains external abort signals for caller control

## Related Concepts
- [[ClockSkewDetection]] — Uses timeouts for skew detection requests
- [[fetchApi]] — Primary API caller using timeout configuration
