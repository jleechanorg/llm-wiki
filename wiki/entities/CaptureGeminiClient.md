---
title: "CaptureGeminiClient"
type: entity
tags: [testing, capture, gemini, llm]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Specialized capture client for Google Gemini API operations. Records generateContent calls and their responses for testing, debugging, and session replay.

## Key Operations
- `gemini.generate` — content generation requests
- `gemini.embed` — embedding generation

## Related
- [CaptureManager](CaptureManager.md) — parent orchestrator
- [CaptureFirestoreClient](CaptureFirestoreClient.md) — parallel client for Firestore
- [CaptureAnalyzer](CaptureAnalyzer.md) — operation analysis
