---
title: "Correlation ID"
type: concept
tags: [logging, debugging, distributed-systems]
sources: ["services-layer-architecture"]
last_updated: 2026-04-08
---

## Summary
Unique identifier attached to all log messages for a single request, enabling distributed tracing across service calls. Passed through request context or generated at entry point.

## Connections
- [[ErrorHandling]] — logged with correlation ID for debugging
- [[StructuredLogging]] — part of logging integration
- [[ServicesLayerArchitecture]] — development guideline
