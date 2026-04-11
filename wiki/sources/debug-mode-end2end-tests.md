---
title: "Debug Mode End-to-End Integration Tests"
type: source
tags: [python, testing, integration, debug, settings, ui-state]
source_file: "raw/test_debug_mode_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration tests validating the complete debug mode functionality flow from settings API through UI state consistency. Tests mock external services (Gemini API and Firestore) at the lowest level to test the full application stack.

## Key Claims
- **Full Stack Testing**: Tests debug mode through complete request pipeline from API to UI state
- **Settings API Validation**: Tests turning debug mode on/off via `/api/settings` endpoint
- **External Service Mocking**: Gemini API and Firestore mocked at lowest level for isolation
- **User Settings Integration**: Validates user-level settings override game state defaults

## Key Test Cases
- `test_turn_on_debug_mode`: Verify debug mode can be enabled via settings API
- `test_turn_off_debug_mode`: Verify debug mode can be disabled via settings API

## Connections
- [[DebugMode]] — the feature being tested
- [[SettingsAPI]] — the API endpoint for toggling debug mode
- [[FakeFirestoreClient]] — test utility mocking Firestore
- [[End2EndBaseTestCase]] — base test class providing auth and client setup

## Contradictions
- None
