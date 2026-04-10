---
title: "Service Provider Factory Pattern"
type: concept
tags: [design-pattern, factory, testing, service-provider]
sources: ["service-provider-factory-unit-tests"]
last_updated: 2026-04-08
---

## Description
Design pattern where a factory class manages creation of different service provider implementations based on configuration. Supports multiple modes: mock (testing), real (production), capture (record responses).

## Usage
Used in the testing framework to switch between mock and real service providers based on `TEST_MODE` environment variable or explicit mode parameter.

## Related Concepts
- [[SingletonPattern]] — factory maintains global state via `get_current_provider()`
- [[DependencyInjection]] — providers injected rather than hardcoded
