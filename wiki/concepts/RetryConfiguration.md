---
title: "Retry Configuration"
type: concept
tags: [http, resilience, error-handling]
sources: []
last_updated: 2026-04-08
---

## Description
HTTP retry mechanism that automatically re-requests failed operations. Configured via HTTPAdapter.max_retries with total attempt count.

## Key Aspects
- **total**: Maximum retry attempts (e.g., 3)
- **backoff_factor**: Delay multiplier between retries
- **status_forcelist**: HTTP status codes triggering retry

## Connections
- [HTTPAdapter](../entities/HTTPAdapter.md) — implements retry logic
- [MCPClient](../entities/MCPClient.md) — configures retry with max_retries=3
- [ConnectionPooling](ConnectionPooling.md) — often paired with retry for robust HTTP
