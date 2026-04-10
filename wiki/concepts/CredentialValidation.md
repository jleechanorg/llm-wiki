---
title: "CredentialValidation"
type: concept
tags: [validation, credentials, gcp, service-accounts]
sources: [service-account-loader-unit-tests]
last_updated: 2026-04-08
---

The process of validating GCP service account credential format.

## Required Fields
- `type`: Must be `"service_account"`
- `project_id`: GCP project identifier
- `private_key_id`: Key identifier
- `private_key`: RSA private key in PEM format
- `client_email`: Service account email address
- `client_id`: OAuth client identifier
- `auth_uri`: OAuth authorization endpoint
- `token_uri`: OAuth token endpoint

## Validation Checks
- JSON structure validity
- Required field presence
- Field type correctness
- Private key PEM format ( Begins with `-----BEGIN PRIVATE KEY-----`)

## Error Cases
- Missing required fields
- Invalid JSON format
- Malformed private key
- Incorrect credential type
