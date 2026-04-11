---
title: "Service Account Loader Unit Tests"
type: source
tags: [unit-testing, credentials, service-accounts, gcp, tdd]
source_file: "raw/service-account-loader-unit-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive unit tests for the `service_account_loader.py` module, covering file-based and environment variable credential loading, fallback behavior, error handling, validation, and private key newline conversion.

## Key Claims
- **File-based Credential Loading**: Tests verify credentials can be loaded from JSON service account files
- **Environment Variable Loading**: Tests cover loading credentials from `GOOGLE_*` environment variables
- **Fallback Behavior**: Validates fallback chain: file path → environment variables → default credentials
- **Error Handling**: Tests ensure proper error messages when credentials are missing or invalid
- **Validation**: Verifies credential format validation including required fields
- **Private Key Handling**: Tests private key newline conversion for proper PEM formatting
- **Tilde Expansion**: Validates `~` path expansion in file paths

## Connections
- [[ServiceAccountLoader]] — module being tested
- [[CredentialLoading]] — the loading mechanism
- [[CredentialValidation]] — validation of credential formats

## Contradictions
- []
