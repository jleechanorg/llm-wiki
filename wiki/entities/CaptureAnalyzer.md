---
title: "CaptureAnalyzer"
type: entity
tags: [testing, capture, analysis]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Analyzes captured interaction sessions to identify patterns, errors, and performance characteristics. Part of capture_analysis module.

## Key Methods
- `create_mock_baseline()` — generates test fixtures for validation
- Analyzes error rates, response times, and service call distribution

## Related
- [[CaptureManager]] — data source
- [[CaptureFirestoreClient]] — Firestore analysis
- [[CaptureGeminiClient]] — Gemini analysis
