---
title: "Real Service Provider"
type: source
tags: [testing, real-services, firestore, gemini]
sources: [mvp-site-real-provider]
last_updated: 2025-01-15
---

## Summary

Real service provider implementation using actual Firestore and Gemini APIs with test isolation and cleanup.

## Key Claims

- **RealServiceProvider**: Uses real Google Cloud Firestore and Gemini APIs
- **Capture mode**: Optionally wraps clients to capture interactions
- **Test isolation**: Tracks and cleans up test collections
- **Early validation**: Validates configuration at initialization
- **Batch cleanup**: Deletes test data in batches to avoid timeout

## Services

- **Firestore**: google.cloud.firestore.Client with test project
- **Gemini**: google.genai.Client with API key
- **Auth**: Simple test auth object with test user/session IDs

## Capture Support

Can wrap clients with CaptureFirestoreClient/CaptureGeminiClient to record real interactions for replay.

## Connections

- [[mvp-site-service-provider]] - Base class
- [[mvp-site-firestorm-service]] - Firestore service
