---
title: "Mock Services"
type: concept
tags: [testing, mocking, service-doubles]
sources: ["global-pytest-configuration-mvp-site-tests", "capture-framework-documentation", "data-capture-framework-implementation"]
last_updated: 2026-04-08
---

## Definition
Mock services are test doubles that simulate real service behavior (APIs, databases, authentication) without making actual network calls. They enable fast, deterministic, and isolated test execution.

## Key Patterns
- **USE_MOCKS environment variable**: Flag to enable mock services
- **MOCK_SERVICES_MODE**: Comprehensive mock mode for test execution
- **Transparent wrappers**: Services that switch between real and mocked implementations based on configuration

## Related Concepts
- [[CaptureFrameworkDocumentation]] — framework for capturing real service interactions for mock validation
- [[RealModeTesting]] — testing pattern using actual services with captured responses
- [[TestIsolation]] — ensuring tests don't depend on each other or external state

## Usage in WorldArchitect.AI
The pytest configuration forces mock services to ensure tests run reliably without network dependencies or API key requirements.
