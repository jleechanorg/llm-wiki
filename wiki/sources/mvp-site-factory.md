---
title: "mvp_site factory"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/factory.py
---

## Summary
Service provider factory for creating appropriate providers based on TEST_MODE environment. Manages global provider state for tests, providing MockServiceProvider or RealServiceProvider based on configuration.

## Key Claims
- get_service_provider() creates MockServiceProvider (default) or RealServiceProvider
- Global provider instance management: set_service_provider, get_current_provider, reset_global_provider
- TEST_MODE options: "mock" (default), "real", "capture"

## Connections
- [[Validation]] — test provider configuration
