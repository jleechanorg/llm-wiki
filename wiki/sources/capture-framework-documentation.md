---
title: "Capture Framework Documentation"
type: source
tags: [worldarchitect, testing, capture-framework, mock-validation, service-mocking, documentation]
source_file: "raw/capture-framework-documentation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Documentation for the Capture Framework enabling real service interaction recording during testing for mock validation and analysis. Provides environment-based capture mode, context managers for interaction recording, transparent service wrappers, and CLI tools for analysis and comparison.

## Key Claims
- **Capture Mode**: Activated via TEST_MODE=capture environment variable to automatically record all service interactions
- **JSON Storage**: Interactions stored with session_id, timestamp, service, operation, request/response, status, and duration_ms
- **Automatic Sanitization**: Sensitive fields (password, api_key, secret) automatically redacted for privacy
- **CLI Tools**: analyze, compare, baseline, list, cleanup commands for capture file management
- **Transparent Wrappers**: CaptureFirestoreClient and CaptureGeminiClient wrap existing services without changing test code

## Key Quotes
> "When running tests in capture mode, the framework records all service interactions (Firestore, Gemini API calls)"

> "Sensitive fields are automatically redacted: password -> \"[REDACTED]\", api_key -> \"[REDACTED]\""

## Connections
- [[DataCaptureFramework]] — core framework this documentation describes
- [[CaptureAnalyzer]] — analysis tool for captured data
- [[CaptureManager]] — central recording class

## Contradictions
- []
