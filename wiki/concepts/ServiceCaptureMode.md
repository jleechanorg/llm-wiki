---
title: "Service Capture Mode"
type: concept
tags: [testing, service-mocking, api-recording]
sources: []
last_updated: 2026-04-08
---

## Definition
A testing mode that records all service interactions (API calls, responses, timing, errors) to JSON files for later analysis, comparison against mocks, and debugging.

## Use Cases
- **Regression Testing**: Compare captured real service responses against mock baselines to detect drift
- **Debugging**: Replay captured interactions to reproduce issues in isolation
- **Performance Analysis**: Analyze timing data across many interactions
- **Error Pattern Detection**: Identify recurring error patterns in service calls

## Implementation
- Enabled via TEST_MODE=capture environment variable
- Service provider creates a CaptureManager that intercepts all operations
- Each interaction stored as JSON with: timestamp, service, operation, request, response, status, duration_ms
- Capture files named: capture_{session_id}_{timestamp}.json

## Related Concepts
- [[MockValidation]] — comparing captures against mock responses
- [[ServiceProviderPattern]] — factory for creating providers in different modes
- [[IntegrationTesting]] — using captures for end-to-end test validation
