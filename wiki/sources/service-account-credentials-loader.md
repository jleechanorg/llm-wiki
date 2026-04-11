---
title: "Service Account Credentials Loader - Secure Google Cloud Authentication"
type: source
tags: [authentication, google-cloud, security, environment-variables, firebase, service-accounts, credentials, secure-coding]
source_file: "raw/service-account-credentials-loader.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing flexible service account credential loading for Google Cloud services (Firebase Admin, Cloud Storage, Vertex AI, BigQuery) with zero hardcoded secrets. Supports both file-based and environment variable loading methods.

## Key Claims
- **Two Loading Methods** — file-based (serviceAccount.json) and environment variable loading
- **Zero Hardcoded Secrets** — credentials dict is a template that pulls values from env vars at runtime
- **Git-Safe Pattern** — no sensitive values committed; env vars live in .env or CI secrets
- **Claude.ai Compatible** — works in cloud IDEs via environment variable configuration

## Environment Variables

### Required
- GOOGLE_PROJECT_ID: GCP project ID
- GOOGLE_CLIENT_EMAIL: Service account email
- GOOGLE_PRIVATE_KEY: Full private key PEM string with \\n escape sequences

### Optional
- GOOGLE_PRIVATE_KEY_ID: Private key ID
- GOOGLE_CLIENT_ID: Client ID

## Usage Patterns

### Try file first, fallback to env vars (recommended)
```python
from mvp_site.service_account_loader import get_service_account_credentials
creds = get_service_account_credentials(
    file_path="~/serviceAccountKey.json",
    fallback_to_env=True
)
```

### Env vars only (sandbox/serverless)
```python
creds = get_service_account_credentials(
    file_path=None,
    fallback_to_env=True,
    require_env_vars=True
)
```

## Security Notes
- Never commit .env files or serviceAccount.json to git
- Never hardcode credentials in source code
- Never log or print credential values
- Use Secret Manager in production
- Rotate service account keys regularly

## Connections
- [[EnvironmentVariableConfiguration]] — how to set up env vars
- [[ServiceAccountCredentials]] — core credential concept
- [[GoogleCloudAuthentication]] — authentication patterns for GCP
