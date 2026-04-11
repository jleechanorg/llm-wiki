---
title: "Service Provider Framework Integration Tests"
type: source
tags: [python, testing, integration, service-provider, mock-mode]
source_file: "raw/test_service_provider_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Integration example demonstrating how existing tests can use the TestServiceProvider framework for backwards compatibility and easy migration. Shows mock/real mode switching through the provider interface without changing test code.

## Key Claims
- **Framework provides unified interface**: get_current_provider() returns either mock or real services based on TEST_MODE environment variable
- **Mock mode is default for testing**: Tests can safely run without external dependencies by setting TEST_MODE=mock
- **Seamless mode switching**: Same test code works with both mock and real services by changing environment variables
- **Service isolation**: reset_global_provider() ensures clean state between tests
- **Interface consistency**: Both mock and real providers implement identical method signatures

## Key Quotes
> "The same test could run with real services by just setting: os.environ['TEST_MODE'] = 'real'" — demonstrates framework flexibility

## Connections
- [[TestServiceProvider]] — the framework this integration test demonstrates
- [[MockModeTesting]] — testing pattern enabled by the provider framework
- [[FirebaseMocking]] — related Firestore mocking techniques

## Contradictions
- []
