---
title: "Real Service Provider Implementation"
type: source
tags: [testing, service-provider, firestore, gemini, google-cloud, test-isolation]
source_file: "raw/real-service-provider-implementation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Implements a RealServiceProvider class that uses actual Google Cloud services (Firestore, Gemini) for testing with proper test isolation and cleanup. Supports optional capture mode for recording service interactions and includes early configuration validation.

## Key Claims
- **Real Service Integration** — Uses `google.cloud.firestore` and `google.genai` for actual service calls with configurable project_id and API key
- **Capture Mode** — Optional wrapper that records Firestore and Gemini interactions via CaptureManager for debugging and replay
- **Test Isolation** — Tracks created test collections and provides cleanup method to delete test data in batches
- **Early Validation** — Validates configuration at initialization to fail fast if required credentials are missing
- **Fallback Interface** — Provides identical interface to TestServiceProvider abstract class for seamless dual-mode testing

## Key Quotes
> "google-cloud-firestore is required for real service testing. Install with: pip install google-cloud-firestore"

> "google-generativeai is required for real service testing. Install with: pip install google-generativeai"

## Connections
- [[TestServiceProvider]] — Abstract base class this implements
- [[CaptureManager]] — Manages recording of service interactions when capture_mode is enabled
- [[MockFirestoreServiceWrapper]] — Alternative using in-memory mock instead of real Firestore
- [[MockGeminiServiceWrapper]] — Alternative using mock LLM responses instead of real Gemini API

## Contradictions
- []
