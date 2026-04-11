---
title: "Test Configuration Management"
type: source
tags: [testing, configuration, environment, test-isolation, python]
source_file: "raw/test-configuration-management.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python class providing configuration management for real service testing. Handles environment variables for Firestore, Gemini API, and Firebase Auth test credentials. Includes validation and test-specific collection naming with prefix support.

## Key Claims
- **TestConfig Class**: Static methods for retrieving test configuration across services
- **Firestore Config**: Uses TEST_FIRESTORE_PROJECT env var, defaults to "worldarchitect-test", adds collection prefix
- **Gemini Config**: Uses TEST_GEMINI_API_KEY env var, defaults to gemini-1.5-flash model, limits requests per test
- **Auth Config**: Provides test_user_id and test_session_id for Firebase Auth testing
- **Validation**: validate_real_service_config() ensures required env vars are present

## Key Quotes
> "TEST_GEMINI_API_KEY environment variable required for real service testing"

## Connections
- [[Firebase]] — Firestore and Auth configuration for test isolation
- [[Gemini]] — API key configuration for LLM testing
- [[CaptureAnalyzer]] — likely used alongside for test validation

## Contradictions
- None identified
