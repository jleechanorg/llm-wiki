---
title: "Data Capture Framework"
type: concept
tags: [testing, capture-framework, service-mocking, real-mode-testing]
sources: []
last_updated: 2026-04-08
---

## Definition
A testing infrastructure that transparently records real service interactions (Firestore, Gemini, Auth) during test execution, enabling mock validation and baseline generation. Designed for zero-impact integration where test code remains unchanged.

## Key Components
- **CaptureManager**: Central orchestrator using context manager pattern for automatic recording
- **Service Wrappers**: Transparent wrappers (CaptureFirestoreClient, CaptureGeminiClient) that intercept operations without API changes
- **CaptureAnalyzer**: Analysis engine comparing real captures against mock baselines
- **CLI Tools**: Command-line interface for analyze, compare, baseline, list, cleanup operations

## Technical Details
- **Data Format**: JSON with session_id, timestamp, total_interactions, and per-interaction details (service, operation, request, response, status, duration_ms)
- **Sanitization**: Automatic redaction of sensitive fields (email, password, tokens)
- **Storage**: Session-based organization in configurable directory with automatic cleanup
- **Performance**: ~1-2ms overhead per interaction due to capture logic

## Use Cases
1. Generate mock baselines from real service responses
2. Validate mock accuracy against production behavior
3. Identify missing mocks or behavioral drift
4. Analyze service performance patterns

## Related Concepts
- [[MockValidation]] — comparing captured data against mock responses
- [[ServiceInteractionRecording]] — capturing Firestore/Gemini/Auth operations
- [[RealModeTesting]] — testing framework mode using real services with capture
