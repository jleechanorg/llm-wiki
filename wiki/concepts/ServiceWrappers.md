---
title: "Service Wrappers"
type: concept
tags: [testing, capture-framework, architecture]
sources: [capture-framework-documentation]
last_updated: 2026-04-08
---

Transparent wrapper classes (CaptureFirestoreClient, CaptureGeminiClient) that wrap existing services without changing test code. Automatically used when RealServiceProvider is in capture mode, enabling interaction recording as a cross-cutting concern.

**Related:** [[CaptureFirestoreClient]], [[CaptureGeminiClient]], [[CaptureManager]]
