---
title: "CredentialLoading"
type: concept
tags: [credentials, loading, gcp, service-accounts]
sources: [service-account-loader-unit-tests]
last_updated: 2026-04-08
---

The process of loading GCP service account credentials from various sources.

## Loading Strategies

### File-based Loading
- Reads JSON service account file from disk
- Supports `~` (tilde) path expansion
- Parses JSON and extracts credential fields
- Validates required fields present

### Environment Variable Loading
- Loads from `GOOGLE_PROJECT_ID`
- Loads from `GOOGLE_CLIENT_EMAIL`
- Loads from `GOOGLE_PRIVATE_KEY`
- Loads from `GOOGLE_PRIVATE_KEY_ID`
- Loads from `GOOGLE_CLIENT_ID`
- Also checks `WORLDAI_GOOGLE_APPLICATION_CREDENTIALS`

### Fallback Chain
1. First tries file path if provided
2. Falls back to environment variables if enabled
3. Uses Application Default Credentials as final fallback

## Error Handling
- `ServiceAccountLoadError` raised with descriptive message
- Distinguishes between file not found, invalid JSON, and missing required fields
- Preserves original exception context in error messages
