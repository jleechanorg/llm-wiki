---
title: "mvp_site config"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/config.py
---

## Summary
Configuration management for real service testing. Provides TestConfig class with real service configuration including Firestore project, Gemini API key, and test user IDs.

## Key Claims
- get_real_service_config() returns dict with firestore project, gemini api key, auth settings
- validate_real_service_config() checks TEST_GEMINI_API_KEY is set
- get_test_collection_name() applies test prefix to collection names for isolation

## Connections
- [[Validation]] — test configuration validation
