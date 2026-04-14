---
title: "GitHub Stadium"
type: entity
tags: [github, infrastructure, real-time]
sources: [system-design-primer]
last_updated: 2026-04-14
---

## Summary
GitHub's real-time infrastructure handling thousands of concurrent SSH connections using event-driven architecture. Multiplexes connections over few OS threads with in-memory state and Redis pub/sub.

## Key Characteristics
- Event-driven, non-blocking I/O
- Connection state in-memory with Redis coordination
- Handles peak traffic during major OSS events

## Connections
- [[MicroservicesArchitecture]] — architectural pattern used
- [[CachingStrategies]] — Redis caching layer
