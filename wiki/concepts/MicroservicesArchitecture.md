---
title: "Microservices Architecture"
type: concept
tags: [architecture, distributed-systems, services]
sources: [system-design-primer]
last_updated: 2026-04-14
---

## Summary
Decomposing applications into independently deployable services that communicate via well-defined APIs. Each service owns its data and can be developed, deployed, and scaled independently.

## Key Patterns
- Service discovery (Consul, etcd, ZooKeeper)
- API gateways for request routing and aggregation
- Circuit breakers (Hystrix, Resilience4j patterns)
- Event-driven communication for loose coupling
- Saga pattern for distributed transactions

## Trade-offs
- **Pros**: Independent scaling, fault isolation, technology heterogeneity, team autonomy
- **Cons**: Distributed system complexity, data consistency challenges, operational overhead

## Connections
- [[DistributedSystems]] — underlying distributed theory
- [[ServiceDiscovery]] — how services find each other
- [[GitHubStadium]] — real-world microservices case study
