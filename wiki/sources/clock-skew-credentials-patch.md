---
title: "Clock Skew Credentials Patch for Google Auth"
type: source
tags: [google-auth, jwt, firebase, clock-skew, credentials, deployment-validation]
source_file: "raw/clock-skew-credentials-patch.md"
sources: []
last_updated: 2026-04-08
---

## Summary
A monkey-patch module that adjusts Google Auth's internal clock to compensate for systems where local time runs ahead of Google's servers beyond the ~5 minute JWT tolerance. Implements a context manager for temporary bypass and deployment validation to prevent dev credentials in production.

## Key Claims
- **Hardcoded 12-minute adjustment**: CLOCK_SKEW_SECONDS = 720 compensates for local clock being ahead
- **Context manager bypass**: UseActualTime allows temporary real-time for operations requiring accurate timestamps
- **Production detection**: Automatically disables patch on Cloud Run (K_SERVICE env var) and production environments
- **Deployment validation**: Prevents production credential misconfiguration via WORLDAI_GOOGLE_APPLICATION_CREDENTIALS + WORLDAI_DEV_MODE

## Key Quotes
> "This compensates for local clock being ahead of Google's servers. Safe for both local development and production - Firebase handles actual time."

> "In Cloud Run/Production, system time is synchronized (NTP) and correct. Applying a 12-minute skew causes 'Token used too early' errors."

## Connections
- [[FirebaseAuthentication]] — Firebase Auth initialization with dev test bypass
- [[ClockSkewDetection]] — client-server time sync via /api/time endpoint with automatic compensation
- [[ServicesLayerArchitecture]] — part of Firebase Integration Services layer

## Contradictions
- None identified. Complements existing clock skew detection system rather than conflicts.
