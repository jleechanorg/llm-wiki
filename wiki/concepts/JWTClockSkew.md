---
title: "JWT Clock Skew"
type: concept
tags: [jwt, authentication, time-tolerance]
sources: ["clock-skew-deployment-validation-tests"]
last_updated: 2026-04-08
---

## Definition
JWT clock skew is the acceptable time difference between the local client clock and the token issuer server clock. When a JWT's `exp` or `nbf` claims are validated, clock skew provides a tolerance window to account for clock drift.

## Key Details
- **Hardcoded Value**: 720 seconds (12 minutes) — compensates for local clock being ahead of Google's servers
- **Environment Independent**: No longer depends on `WORLDAI_DEV_MODE` or `TESTING_AUTH_BYPASS`
- **Purpose**: Prevents JWT validation failures due to minor clock differences between client and server

## Related Concepts
- [[JWT Authentication]]
- [[Authentication Resilience]]
- [[Firebase Authentication]]
