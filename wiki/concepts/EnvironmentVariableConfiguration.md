---
title: "Environment Variable Configuration"
type: concept
tags: [configuration, environment, testing, pattern]
sources: []
last_updated: 2026-04-08
---

## Summary
A configuration pattern where a default value is used when an environment variable is not set, but the env var takes precedence when provided. Enables both local development defaults and CI/CD overrides.


## Pattern
```python
import os
DEFAULT_VALUE = "fallback@example.com"
actual = os.environ.get("ENV_VAR_NAME", DEFAULT_VALUE)
```

## Use Cases
- Test user emaildefaults in testing frameworks
- API keys with development vs production variants
- Feature flags for CI vs local environments
