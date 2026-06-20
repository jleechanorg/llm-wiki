---
title: "CredentialValidation"
type: concept
tags: [validation, credentials, gcp, service-accounts, env-vars, providers]
sources: [service-account-loader-unit-tests, mem0-embedder-wafer-ollama-2026-06-06]
last_updated: 2026-06-06
---

The process of validating GCP service account credential format.

## Provider/credential mismatch in environment variables

A credential can be syntactically present yet semantically wrong for the consumer.
A token for **provider A** stored in **provider B's** environment variable fails at
the API call, not at startup, and the failure can be silent.

Case (2026-06-06): `OPENAI_API_KEY` held a **Wafer** token (`wfr_…`). Wafer is an
Anthropic-compatible gateway, not OpenAI, so the mem0 openai embedder rejected it
and fact-extraction/embedding silently failed. Compounding it, the intended override
in `~/.hermes/config.yaml` never applied because the loader parsed YAML with
`json.loads()` and swallowed the resulting exception — a silent no-op. See
[mem0-embedder-wafer-ollama-2026-06-06](../sources/mem0-embedder-wafer-ollama-2026-06-06.md).

Rules:
- Never store a provider-A token in a provider-B env var. Validate the token *prefix*
  against the expected provider (`sk-` openai, `wfr_` Wafer/Anthropic gateway, etc.).
- Config loaders that swallow parse exceptions become silent no-ops; match the parser
  to the file format (YAML ≠ `json.loads`) and surface the error rather than gating it
  behind a debug flag.

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
