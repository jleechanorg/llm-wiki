---
title: "Stateless Operations"
type: concept
tags: [architecture, design-pattern, services]
sources: ["services-layer-architecture"]
last_updated: 2026-04-08
---

## Summary
Services maintain no internal state between calls. Each request contains all information needed for processing, enabling horizontal scaling and simplified testing.

## Connections
- [[SingleResponsibilityPrinciple]] — complementary service principle
- [[ServicesLayerArchitecture]] — architectural pattern applied to services
