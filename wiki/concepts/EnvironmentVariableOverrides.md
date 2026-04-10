---
title: "Environment Variable Overrides"
type: concept
tags: [configuration, testing, environment]
sources: [provider-settings-selection-tests]
last_updated: 2026-04-08
---

Environment Variable Overrides allow runtime configuration to take precedence over stored user settings for testing and operational flexibility.

## Relevant Variables
| Variable | Behavior |
|----------|----------|
| `FORCE_PROVIDER` | Overrides user LLM provider selection |
| `TESTING_AUTH_BYPASS` | Enables test mode (does NOT force provider) |
| `MOCK_SERVICES_MODE` | Enables service mocking |
| `FORCE_TEST_MODEL` | Forces specific model for testing |

## Testing Notes
- `TESTING_AUTH_BYPASS` only bypasses auth, NOT provider selection
- User settings are still respected in test mode
- This was a behavioral change from earlier implementations

## Connections
- [[ProviderSelection]] — affected by env var overrides
- [[LLMService]] — reads environment variables
