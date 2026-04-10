---
title: "Service Interaction Recording"
type: concept
tags: [testing, mocking, integration-testing]
sources: []
last_updated: 2026-04-08
---

## Definition
The practice of capturing real API calls and responses during test execution to enable later comparison against mock implementations. Forms the foundation of Real-Mode Testing, where tests run against actual services but record interactions for validation.

## Capture Framework Implementation
1. **Session Organization**: Each capture session gets unique timestamp-based ID
2. **Interaction Metadata**: Records service name, operation, request/response, duration, status
3. **Error Tracking**: Captures exception type and message for failed interactions
4. **JSON Persistence**: Saves complete interaction history for later analysis

## Related Concepts
- [[MockValidation]] — comparing recorded interactions against mocks
- [[CaptureManager]] — the class implementing this pattern
- [[RealModeTesting]] — testing paradigm that uses interaction recording
