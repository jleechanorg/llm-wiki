---
title: "Fast Mode Testing"
type: concept
tags: [testing, performance, mocking, fast-mode]
sources: ["test-performance-configuration"]
last_updated: 2026-04-08
---

## Definition
Test execution mode that uses aggressive mocking to bypass expensive operations (file I/O, network calls, LLM service invocations) for faster test runs.

## Related Concepts
- [[Test Mocking]] — the technique used to achieve fast mode
- [[CI Performance Optimization]] — the runtime context where fast mode is most valuable

## Usage
Enabled via FAST_TESTS=1 environment variable. When active, tests use pre-configured mock return values instead of actual file loading and LLM service calls.
