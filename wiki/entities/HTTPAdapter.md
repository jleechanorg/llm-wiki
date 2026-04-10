---
title: "HTTPAdapter"
type: entity
tags: [http, requests, library]
sources: []
last_updated: 2026-04-08
---

## Description
Part of the requests library. Provides HTTP connection pooling and retry logic for requests.Session.

## Attributes
- **_pool_connections**: Number of connection pools to cache
- **pool_maxsize**: Maximum connections per pool
- **max_retries**: Retry configuration object

## Connections
- [[MCPClient]] — uses HTTPAdapter for connection pooling
- [[ConnectionPooling]] — concept implemented by this adapter
