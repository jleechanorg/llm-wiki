---
title: "Test Environment Variables"
type: concept
tags: [testing, configuration, environment, environment-variables]
sources: ["global-pytest-configuration-mvp-site-tests", "test-configuration-management"]
last_updated: 2026-04-08
---

## Definition
Environment variables that control test behavior, enabling configuration-driven testing without code changes. They govern service modes, authentication bypass, API keys, and feature flags.

## Key Variables in WorldArchitect.AI Tests
| Variable | Purpose |
|---|---|
| TESTING_AUTH_BYPASS | Skip authentication in tests |
| USE_MOCKS | Enable mock service implementations |
| MOCK_SERVICES_MODE | Comprehensive mock mode |
| WORLDAI_DEV_MODE | Enable development-mode behavior |
| GEMINI_API_KEY | API key for Gemini (mocked in tests) |
| GOOGLE_API_KEY | API key for Google services (mocked in tests) |
| TEST_FIRESTORE_PROJECT | Firestore project for tests |
| TEST_GEMINI_API_KEY | Gemini API key for real service tests |

## Related Concepts
- [[TestConfigurationManagement]] — Python class for managing test configuration
- [[TestIsolation]] — using environment variables to isolate test execution

## Best Practices
1. Use descriptive variable names with TEST_ or MOCK_ prefixes
2. Provide sensible defaults for local development
3. Validate required variables at test startup
4. Document all variables in conftest.py or configuration files
