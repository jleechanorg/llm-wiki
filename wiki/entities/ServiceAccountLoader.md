---
title: "ServiceAccountLoader"
type: entity
tags: [module, credentials, gcp]
sources: [service-account-loader-unit-tests]
last_updated: 2026-04-08
---

Python module responsible for loading GCP service account credentials from files or environment variables.

## Functions
- `get_service_account_credentials()` — Main entry point, accepts `file_path` and `fallback_to_env` parameters
- `_load_credentials_from_env()` — Internal function loading from environment variables
- `_validate_credentials_dict()` — Internal function validating credential format
- `ServiceAccountLoadError` — Custom exception raised on load failures

## Credential Sources (Priority Order)
1. File path (via `file_path` parameter)
2. Environment variables (`GOOGLE_PROJECT_ID`, `GOOGLE_CLIENT_EMAIL`, etc.)
3. Default credentials via Application Default Credentials (ADC)

## Key Features
- JSON service account file parsing
- Private key newline conversion for PEM format
- Tilde (`~`) path expansion
- Comprehensive error messages

## Connected Pages
- [[CredentialLoading]] — loading mechanism
- [[CredentialValidation]] — validation logic
