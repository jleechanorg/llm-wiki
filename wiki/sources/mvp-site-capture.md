---
title: "mvp_site capture"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/capture.py
---

## Summary
Data capture framework for recording real service interactions (API calls and responses) for mock validation and analysis. Provides CaptureManager, CaptureFirestoreClient, CaptureGeminiClient wrappers that intercept and record all interactions with sanitization of sensitive fields.

## Key Claims
- CaptureManager provides context manager capture_interaction() for wrapping service calls
- record_response() attaches response data to captured interactions
- save_captures() persists interactions to timestamped JSON files
- _sanitize_data() redacts sensitive fields (password, secret, token, api_key, private_key)
- CaptureFirestoreClient wraps Firestore client operations (collection, document references)
- CaptureGeminiClient wraps Gemini generate_content calls with prompt/response capture
- cleanup_old_captures() removes capture files older than specified days

## Connections
- [[LLMIntegration]] — captures Gemini API interactions
- [[Serialization]] — JSON serialization for capture files
- [[Validation]] — mock validation against real captured data
