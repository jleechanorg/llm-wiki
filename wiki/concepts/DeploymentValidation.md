---
title: "Deployment Validation"
type: concept
tags: [devops, configuration, security, environment]
sources: [clock-skew-credentials-patch]
last_updated: 2026-04-08
---

Deployment validation ensures correct environment configuration, preventing accidental use of development credentials in production. The validate_deployment_config() function checks WORLDAI_GOOGLE_APPLICATION_CREDENTIALS + WORLDAI_DEV_MODE.

## Validation Rules
- If WORLDAI_GOOGLE_APPLICATION_CREDENTIALS is set, WORLDAI_DEV_MODE must be "true"
- TESTING_AUTH_BYPASS=true unconditionally bypasses all validation
- MOCK_SERVICES_MODE also bypasses for hermetic testing

## Environment Detection
- Cloud Run: K_SERVICE env var present
- Production: FLASK_ENV=production or ENVIRONMENT=production

## Related
- [[ClockSkewCredentialsPatch]] — implements validation
- [[EnvironmentConfiguration]] — broader config management
- [[CredentialSecurity]] — credential handling best practices
