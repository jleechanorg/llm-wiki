---
title: "RealServiceProvider Unit Tests"
type: source
tags: [python, testing, unit-tests, service-provider, firestore, gemini]
source_file: "raw/test_real_service_provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating RealServiceProvider implementation of TestServiceProvider interface. Tests cover Firestore/Gemini client creation, auth handling, test collection tracking, cleanup logic, and API key validation.

## Key Claims
- **Interface implementation**: RealServiceProvider implements TestServiceProvider interface
- **Real service flag**: is_real_service returns True for real provider
- **Capture mode**: Supports capture_mode flag for test data recording
- **Firestore client**: Attempts real Firestore client creation (may fail on auth)
- **Gemini client**: Attempts real Gemini client creation (may fail on API key)
- **Test auth**: get_auth returns test user/session IDs
- **Collection tracking**: track_test_collection adds collections to cleanup list
- **Cleanup logic**: cleanup processes tracked test collections
- **API key validation**: Missing TEST_GEMINI_API_KEY raises ValueError

## Connections
- [[TestServiceProvider]] — interface being implemented
- [[RealServiceProvider]] — class under test
- [[GoogleFirestore]] — real Firestore client integration
- [[GoogleGemini]] — real Gemini client integration
