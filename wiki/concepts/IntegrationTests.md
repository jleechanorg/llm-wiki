---
title: "Integration Tests"
type: concept
tags: [testing, software-quality, verification]
sources: ["tdd-tests-concurrent-request-handling"]
last_updated: 2026-04-08
---

## Definition
Tests that verify multiple components of an application work together correctly. Unlike unit tests which isolate individual functions, integration tests exercise the entire stack.

## Characteristics
- **Full Stack**: Tests Gunicorn + Flask + MCP client together
- **Real Dependencies**: Uses actual HTTP server, not mocked
- **Concurrent Execution**: ThreadPoolExecutor simulates load
- **End-to-End**: Request → app → response verified

## In This Context
The concurrent request handling tests are integration tests because they verify:
1. Gunicorn worker×thread configuration
2. Flask application request handling
3. MCP client connection pooling
4. All components working together under load

## Related Concepts
- [[ConcurrentRequestHandling]] — what these tests verify
- [[Gunicorn]] — part of stack under test
- [[Flask]] — web framework under test
- [[ThreadPoolExecutor]] — test execution mechanism
