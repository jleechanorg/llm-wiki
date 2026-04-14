---
title: "mvp_site integration_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/integration_utils.py
---

## Summary
Integration utilities for updating existing tests to support the Real-Mode Testing Framework. Provides dual_mode_test decorator for gradual migration and skip_in_real_mode decorator for tests unsuitable for real services.

## Key Claims
- dual_mode_test decorator makes existing tests work in dual mode
- skip_in_real_mode decorator skips tests in real mode with configurable reason
- Factory integration for service provider management in tests

## Connections
- [[Validation]] — test framework utilities
