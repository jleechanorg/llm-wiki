---
title: "Service Interaction Capture"
type: concept
tags: [testing, service-mocking, integration-testing]
sources: [capture-analyzer-service-interaction-analysis]
last_updated: 2026-04-08
---

## Definition
The practice of recording actual HTTP requests/responses or service calls during real runtime, then saving them as JSON files for later analysis or replay in tests.

## Key Characteristics
- Captures service name, operation, duration, timestamp, and status
- Enables post-hoc analysis of service behavior
- Supports mock validation by comparing captured vs expected responses
- Files named with pattern `capture_YYYY-MM-DD.json`

## Related Concepts
- [[MockValidation]] — comparing captures against mock responses
- [[IntegrationTesting]] — using captures in test scenarios
- [[PerformanceAnalysis]] — measuring service operation timing
