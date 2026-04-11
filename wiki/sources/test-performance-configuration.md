---
title: "Test Performance Configuration"
type: source
tags: [python, testing, performance, mocking, ci, fast-mode]
source_file: "raw/test_performance.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing aggressive mocking of expensive operations to speed up test execution. Uses FAST_TESTS and CI environment variables to enable performance-optimized test runs with mocked file operations and Gemini service calls.

## Key Claims
- **Fast mode activation**: Set via FAST_TESTS=1 environment variable or auto-detected in CI environments
- **Aggressive mocking**: Mocks file_cache.load_file_cached, world_loader.load_world_content, and llm_service operations
- **Diagnostic tooling**: print_performance_config() reports current performance configuration
- **Modular design**: Tests choose when to enable fast mode rather than auto-enabling on import

## Key Quotes
> "This module provides aggressive mocking of expensive operations to speed up tests." — module docstring

## Connections
- [[MVP Test Optimization Recommendations]] — related test performance work
- [[Test Performance Configuration]] — concept page for fast mode testing

## Contradictions
- None identified
