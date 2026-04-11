---
title: "Service Provider Factory Unit Tests"
type: source
tags: [python, testing, service-provider, factory-pattern, mocking]
source_file: "raw/test_service_provider_factory.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying the service provider factory pattern used in the testing framework. Tests validate provider selection logic, environment variable configuration, global state management, and mode-based provider instantiation (mock, real, capture).

## Key Claims
- **Default Behavior**: `get_service_provider()` returns MockServiceProvider by default without any configuration
- **Mode Selection**: Factory supports 'mock', 'real', and 'capture' modes for different testing scenarios
- **Environment Integration**: `TEST_MODE` environment variable controls provider selection
- **Global State**: `get_current_provider()` maintains singleton instance across multiple calls
- **Capture Mode**: RealServiceProvider can operate in capture mode to record API interactions

## Key Quotes
> "Test that get_service_provider returns MockServiceProvider by default"

> "Test that get_service_provider raises ValueError for invalid mode"

## Connections
- [[MockServiceProvider]] — mock implementation for testing without API calls
- [[RealServiceProvider]] — real implementation for actual API testing
- [[ServiceProviderFactory]] — factory class managing provider instantiation

## Contradictions
- []
