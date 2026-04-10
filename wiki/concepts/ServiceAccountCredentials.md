---
title: "Service Account Credentials"
type: concept
tags: [authentication, google-cloud, credentials, security]
sources: [service-account-credentials-loader]
last_updated: 2026-04-08
---

A JSON dictionary containing Google Cloud service account authentication data, including project_id, client_email, private_key, and optional key_id and client_id. These credentials are used to authenticate with Google Cloud APIs (Firebase, Cloud Storage, Vertex AI, BigQuery).

## Loading Patterns

### File-based
Load from serviceAccount.json file downloaded from GCP Console.

### Environment Variables
Pull values from environment variables at runtime — enables git-safe code since no secrets are hardcoded.

## Security Considerations
- Never commit credential files to version control
- Use Secret Manager in production
- Rotate keys regularly
- Never log or print credential values
