---
title: "Service Provider Factory for Tests"
type: source
tags: [python, testing, provider, factory, mock, configuration]
source_file: "raw/service-provider-factory.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a factory pattern for creating service providers based on TEST_MODE environment configuration. Manages global provider state across test runs with functions for setting, getting, and resetting the current provider. Supports mock, real, and capture modes for different testing scenarios.

## Key Claims
- **Factory Pattern**: get_service_provider() creates appropriate provider based on TEST_MODE env var (mock/real/capture)
- **Global State Management**: Global _current_provider tracks active provider across test suite
- **Dual Mock Support**: Imports either full MockServiceProvider or SimpleMockServiceProvider as fallback
- **Capture Mode**: RealServiceProvider supports capture_mode for recording real API interactions

## Key Functions
- `get_service_provider(mode)` — Factory function returning TestServiceProvider based on TEST_MODE
- `set_service_provider(provider)` — Sets global provider instance
- `get_current_provider()` — Gets or creates default global provider
- `reset_global_provider()` — Cleans up and resets global provider state

## Connections
- [[MockServiceProvider]] — Used for unit tests with mocked services
- [[RealServiceProvider]] — Used for real API integration tests
- [[TestServiceProvider]] — Protocol defining provider interface
- [[ServiceProviderFactory]] — This module implements the factory pattern

## Contradictions
- []
