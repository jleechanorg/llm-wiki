---
title: "mvp_site clock_skew_credentials"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/clock_skew_credentials.py
---

## Summary
Clock-skew adjustment workaround for Google Auth library. Monkey-patches google.auth._helpers.utcnow() to return adjusted time when local clock is ahead of Google's servers. Also validates production credential configuration to prevent development credential usage.

## Key Claims
- apply_clock_skew_patch() patches utcnow() to subtract 720 seconds (12 minutes) for clock skew
- get_clock_skew_seconds() detects environment: disables patch on Cloud Run/production, enables for local dev
- validate_deployment_config() prevents use of WORLDAI_GOOGLE_APPLICATION_CREDENTIALS without WORLDAI_DEV_MODE=true
- UseActualTime context manager temporarily restores original time for token verification

## Connections
- [[Validation]] — deployment configuration validation
