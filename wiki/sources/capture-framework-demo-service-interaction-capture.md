---
title: "Capture Framework Demo — Real Service Interaction Capture"
type: source
tags: [worldarchitect, testing, capture-framework, service-mocking, demo-script]
source_file: "raw/capture-framework-demo.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python demonstration script showing how to use the capture framework for recording real service interactions. Demonstrates capture mode configuration, service provider initialization, and JSON-based interaction logging for testing and debugging purposes.

## Key Claims
- **Capture Mode**: Enables TEST_MODE=capture environment variable to record all service interactions to JSON files
- **Service Provider**: Uses get_service_provider() factory with 'capture' mode to create providers that log all operations
- **Capture Directory**: TEST_CAPTURE_DIR environment variable controls where capture files are stored
- **Multi-Service Recording**: Captures Firestore, Gemini, and Auth service operations with timestamps and metadata
- **Capture Summary**: Provider exposes get_capture_summary() for retrieving aggregated interaction data
- **Mock Fallback**: Demonstrates graceful degradation to mock capture data when real services aren't configured

## Key Quotes
> "Capture mode enabled: {provider.capture_mode}"

> "Capture summary: {json.dumps(summary, indent=2)}"

## Connections
- [[CaptureAnalyzer]] — analyzes captured JSON files for performance metrics and error tracking
- [[CaptureAnalysisCLI]] — command-line tool for comparing captured data against mock baselines
- [[ServiceProviderPattern]] — factory pattern for creating service clients in different modes

## Contradictions
- None identified
