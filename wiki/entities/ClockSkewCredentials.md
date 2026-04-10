---
title: "Clock Skew Credentials"
type: entity
tags: [jwt, authentication, configuration]
sources: ["clock-skew-deployment-validation-tests"]
last_updated: 2026-04-08
---

## Description
Module in `mvp_site.clock_skew_credentials` handling JWT clock skew configuration and deployment validation for Firebase/Google authentication.

## Key Functions
- `get_clock_skew_seconds()` — returns hardcoded 720 seconds
- `validate_deployment_config()` — validates credential/env var combinations
- `CLOCK_SKEW_SECONDS` — constant set to 720

## Related
- [[JWT Clock Skew Auto-Retry]]
- [[Authentication Resilience]]
