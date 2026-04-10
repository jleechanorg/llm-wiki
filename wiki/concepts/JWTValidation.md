---
title: "JWT Validation"
type: concept
tags: [authentication, tokens, security, json-web-tokens]
sources: [clock-skew-credentials-patch]
last_updated: 2026-04-08
---

JWT tokens include "issued at" (iat) and "not before" (nbf) claims that must pass time validation against server time. If client clock is ahead, tokens appear to be from the future, causing "Token used too early" errors.

## Clock Skew Tolerance
Google Auth library allows ~5 minutes (300 seconds) of tolerance. Systems with larger clock drift require compensation.

## Related
- [[ClockSkewCompensation]] — solution for JWT validation failures
- [[GoogleAuth]] — performs JWT validation
- [[CredentialToken]] — token type being validated
