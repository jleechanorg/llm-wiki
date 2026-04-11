---
title: "Common Test Utilities"
type: source
tags: [python, testing, utilities, firebase, mocking]
source_file: "raw/test_common.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Shared test utilities module providing common functions for test files across the project. Contains Firebase credentials detection and base test classes for common testing patterns.

## Key Claims
- **Firebase Credentials Check**: `has_firebase_credentials()` always returns False to ensure tests use mocked services rather than real Firebase
- **Mocked Services Pattern**: End-to-end tests should use complete mocking and never require real Firebase credentials
- **Test Environment Safety**: Returning False guarantees tests run against mock providers, preventing accidental real API calls

## Key Test Cases
- `test_firebase_credentials_check`: Verifies that `has_firebase_credentials()` returns False, ensuring mocked test environment

## Connections
- [[FirebaseCredentials]] — the concept this utility manages
- [[MockedServices]] — testing pattern this utility enforces

## Contradictions
- None
