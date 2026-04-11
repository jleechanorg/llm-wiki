---
title: "Capture Framework Tests"
type: source
tags: [python, testing, capture, firestore, gemini, unittest]
source_file: "raw/test_capture_framework.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest and pytest test suite for the capture framework, which records and analyzes service interactions with Firestore and Gemini API calls. Tests cover CaptureManager, CaptureFirestoreClient, CaptureGeminiClient, and CaptureAnalyzer components with error handling, data sanitization, and session management.

## Key Claims
- **Context Manager Capture**: capture_interaction context manager tracks service operations with automatic cleanup on exit
- **Response Recording**: record_response captures response data and calculates duration_ms for each interaction
- **Error Tracking**: Captures error type, message, and status for failed interactions
- **Data Sanitization**: _sanitize_data redacts password and api_key fields, protecting sensitive credentials
- **Session Management**: save_captures persists interactions to JSON with session_id and timestamp
- **Mock Baseline**: create_mock_baseline generates test fixtures for analyzer validation

## Key Test Methods
- test_initialization — validates capture directory creation
- test_capture_interaction_success — validates successful service call recording
- test_capture_interaction_error — validates error type/message capture
- test_save_captures — validates JSON persistence with metadata
- test_sanitize_data — validates credential redaction
- test_get_summary — validates statistics aggregation

## Connections
- [[CaptureManager]] — main capture orchestrator
- [[CaptureFirestoreClient]] — Firestore operation capture
- [[CaptureGeminiClient]] — Gemini API capture
- [[CaptureAnalyzer]] — interaction analysis

## Contradictions
[]
