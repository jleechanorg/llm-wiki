---
title: "Clock Skew Compensation"
type: concept
tags: [authentication, time-sync, jwt, security]
sources: [clock-skew-credentials-patch, clock-skew-detection]
last_updated: 2026-04-08
---

Clock skew compensation adjusts system time to match external server time for JWT token validation. Google Auth allows ~5 minutes of tolerance; systems with larger drift require manual adjustment.

## Mechanisms
- **Credential patch**: Adjusts google.auth._helpers.utcnow() globally
- **API endpoint**: /api/time endpoint for client-server sync (see [[ClockSkewDetection]])

## Production Considerations
- Cloud Run and production environments have NTP-synchronized time — patch must be disabled
- The patch detects K_SERVICE env var for Cloud Run detection

## Related
- [[JWT]] — tokens that require time validation
- [[GoogleAuth]] — library being patched
- [[ClockSkewCredentialsPatch]] — implementation using monkey-patching
- [[ClockSkewDetection]] — complementary client-side detection system
