---
title: "CaptureAnalyzer — Service Interaction Analysis and Mock Comparison"
type: source
tags: [worldarchitect, testing, mock-validation, service-capture, performance-analysis]
source_file: "raw/capture-analyzer-service-interaction-analysis.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python class that analyzes captured service interactions from JSON files and compares them against mock responses. Provides performance metrics, error tracking, and pattern detection across service operations.

## Key Claims
- **Capture File Analysis**: Analyzes JSON capture files from the last N days, loading interactions from files matching `capture_*.json` pattern
- **Multi-Service Metrics**: Groups interactions by service with operation counts, average duration, and error tracking
- **Performance Tracking**: Calculates total/avg duration, identifies slowest and fastest operations
- **Error Detection**: Captures and records all error interactions with service, operation, error message, and timestamp
- **Mock Comparison**: Compares captured real responses against predefined mock responses to validate test fidelity

## Key Quotes
> "Compares captured real service interactions with mock responses."

## Connections
- [[LLMResponseCapture]] — source of captured interaction data
- [[IntegrationTestPattern]] — uses the integration test framework for test setup

## Contradictions
- []
