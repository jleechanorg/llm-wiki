---
title: "Caching Strategies"
type: concept
tags: [caching, performance, distributed-systems]
sources: [system-design-primer]
last_updated: 2026-04-14
---

## Summary
Multi-layer caching approaches to reduce latency and backend load. Covers CDN caching, application-level caching, and database query caching with various invalidation strategies.

## Key Strategies
- Cache-aside (lazy loading)
- Write-through / write-behind
- TTL-based expiration
- Event-driven invalidation

## Connections
- [[GitHubStadium]] — Redis pub/sub for real-time caching
