---
title: "Connection Pooling"
type: concept
tags: [http, networking, performance]
sources: []
last_updated: 2026-04-08
---

## Description
HTTP connection reuse pattern that maintains persistent connections across requests. Reduces latency by avoiding TCP handshake overhead for repeated requests to the same host.

## Key Aspects
- **pool_connections**: Number of distinct host connection pools to cache
- **pool_maxsize**: Maximum number of connections per pool
- **TTL handling**: Connections expire after idle timeout

## Connections
- [MCPClient](../entities/MCPClient.md) — implements connection pooling via HTTPAdapter
- [HTTPAdapter](../entities/HTTPAdapter.md) — provides connection pooling implementation
- [RetryConfiguration](RetryConfiguration.md) — companion feature for failure handling
