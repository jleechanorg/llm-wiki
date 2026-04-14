---
title: "System Design Primer"
type: source
tags: [system-design, architecture, microservices, distributed-systems]
date: 2026-04-14
source_file: /tmp/gist_system_design.md
---

## Summary
A comprehensive system design primer covering fundamental concepts: API design, caching strategies, database sharding, and microservices architecture. Includes case studies of GitHub Stadium, GitHub Search, YouTube, and Dropbox.

## Key Claims
- APIs are the fundamental building blocks for system communication
- Caching reduces latency and load across all system layers
- Database sharding enables horizontal scaling of data storage
- Microservices decompose systems into independently deployable services
- GitHub Stadium handles massive concurrent connections with event-driven architecture
- GitHub Search uses prefix-based indexing and trigram-based ranking
- YouTube's recommendation system balances freshness and relevance
- Dropbox uses distributed hash tables for peer-to-peer file synchronization

## Key Sections

### API Design
- RESTful API principles
- Rate limiting and throttling
- Versioning strategies
- Request/response validation

### Caching
- Multi-layer caching (CDN, application, database)
- Cache invalidation strategies (TTL, event-driven)
- Consistency vs performance tradeoffs

### Database Sharding
- Horizontal partitioning by key range
- Consistent hashing for data distribution
- Cross-shard queries and joins

### Microservices
- Service discovery and registration
- Inter-service communication (sync vs async)
- Circuit breakers and graceful degradation
- Event-driven architecture patterns

## Case Studies

### GitHub Stadium
Real-time system handling 1000s of concurrent SSH connections. Uses event-driven architecture to multiplex connections over few OS threads. Connection state managed in-memory with Redis for pub/sub.

### GitHub Search
Prefix-based file search using trigram-based ranking. Elasticsearch backend with custom analyzers. Handles 10,000+ QPS at peak.

### YouTube
Video streaming with adaptive bitrate. Recommendation engine balancing freshness, user history, and engagement metrics.

### Dropbox
Distributed hash table (DHT) for peer-to-peer file sync. Metadata in SQLite per client, file chunks stored globally. Uses CRDTs for conflict resolution.

## Connections
- [[MicroservicesArchitecture]] — core architectural pattern
- [[DistributedSystems]] — underlying theory
- [[CachingStrategies]] — performance optimization

## Contradictions
- None identified
