---
title: "Zero-Hardcoded-Secrets Pattern"
type: concept
tags: [security, secrets, best-practices, git-safe]
sources: [service-account-credentials-loader]
last_updated: 2026-04-08
---

A coding pattern where credential structures are defined as templates in source code, with actual sensitive values injected from environment variables at runtime. This allows the code to be safely committed to git while keeping secrets out of the repository.

## Why It Works
- The credential dict structure is a TEMPLATE, not actual values
- Environment variables live in .env, CI secrets, or cloud settings
- Only non-sensitive structure is committed, not secrets
- Code can be open-sourced without exposing credentials

## Implementation
```python
# Safe to commit — this is just the structure template
def get_credentials():
    return {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_PROJECT_ID"],
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"],
    }
```
