---
title: "mvp_site simple_mock_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/simple_mock_provider.py
---

## Summary
Simplified mock service provider implementation avoiding dependency issues while providing the same interface as real providers. Provides SimpleMockDocument and SimpleMockCollection for Firestore mocking.

## Key Claims
- SimpleMockDocument: mock Firestore document with set/get/to_dict
- SimpleMockCollection: mock Firestore collection with document management
- SimpleMockServiceProvider for full mock service layer
- Avoids dependency issues while maintaining interface compatibility

## Connections
- [[Validation]] — mock provider for testing
