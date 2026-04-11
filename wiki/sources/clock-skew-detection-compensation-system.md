---
title: "Clock Skew Detection and Compensation System"
type: source
tags: [clock-skew, api, time-synchronization, firebase, authentication, timeout]
source_file: "raw/clock-skew-detection.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Browser-based system for detecting and compensating clock skew between client and server. Uses `/api/time` endpoint to measure time difference, applies automatic compensation delays before token generation, and handles clock skew errors from the server with enhanced detection logic.

## Key Claims
- **Clock Skew Detection**: Uses `/api/time` endpoint to measure client-server time difference, calculating offset from request/response round-trip time
- **Compensation Delays**: Adds 500ms buffer when client is behind server time before token generation
- **Error-Based Updates**: Updates clock skew offset from server clock_skew errors containing server_time_ms
- **Fallback Detection**: Triggers initial detection on module load if no prior skew data exists
- **Severe Skew Handling**: Adds 1000ms extra delay when detected skew exceeds 2000ms
- **Test Mode Bypass**: Supports test_mode URL parameter for development without Firebase auth
- **Request Timeout**: 10-minute default timeout (600000ms) aligned with backend and Cloud Run limits

## Key Functions
- `detectClockSkew()` — Fetches server time and calculates client-server offset
- `applyClockSkewCompensation()` — Waits before token generation if client behind server
- `handleClockSkewError(errorData)` — Updates skew from server errors, triggers fallback detection
- `fetchApi(path, options)` — API caller with timeout, abort signal, auth token, and retry logic

## Connections
- [[Firebase]] — Authentication provider for user tokens
- [[RequestTimeout]] — Centralized timeout configuration aligned with backend limits
- [[TokenTiming]] — Token generation timing that benefits from skew compensation

## Contradictions
- None identified
