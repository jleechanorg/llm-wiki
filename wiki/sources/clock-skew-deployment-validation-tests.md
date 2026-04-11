---
title: "Clock Skew Settings and Deployment Validation Tests"
type: source
tags: [python, testing, jwt, authentication, clock-skew, deployment]
source_file: "raw/test_clock_skew_deployment_validation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating clock skew configuration and deployment validation for JWT authentication resilience. Clock skew is hardcoded to 720 seconds (12 minutes) to compensate for local clock being ahead of Google's servers. Tests verify credential validation rules prevent accidental production use of dev credentials.

## Key Claims
- **Hardcoded Clock Skew**: `get_clock_skew_seconds()` always returns 720 seconds regardless of environment
- **Dev Mode Guard**: `WORLDAI_GOOGLE_APPLICATION_CREDENTIALS` requires `WORLDAI_DEV_MODE=true` to prevent accidental production use
- **Production Behavior**: Without any `WORLDAI_*` variables, validation passes and returns False (production mode)
- **Testing Mode兼容**: Clock skew remains 720 even when `TESTING_AUTH_BYPASS=true`

## Key Quotes
> "The clock skew is now hardcoded to 720 seconds (12 minutes) for all environments." — validates consistent behavior across all deployment contexts

## Connections
- [[JWT Clock Skew Auto-Retry]] — validates retryCount, isClockSkewError detection, and forceRefresh behavior
- [[Authentication Resilience]] — tests for clock skew and credential validation

## Contradictions
- None identified
