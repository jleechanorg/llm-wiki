---
title: "test_base_test_provenance.py"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/test_base_test_provenance.py
---

## Summary
TDD test verifying test_file is properly defined and passed to capture_provenance() in MCPTestBase.run(). Also tests server bootstrap behavior, test user email handling, and trace log enforcement via environment variables.

## Key Claims
- test_file should be defined when calling capture_provenance
- capture_provenance should receive test_file as a parameter that ends with .py
- local start_server should enforce classifier dependency bootstrap
- MCPTestBase should not hardcode default test user email (defaults to empty)
- MCP_TEST_USER_EMAIL env var should be passed to local server headers
- REQUIRE_FULL_TRACE_LOGS enforced by default even when disabled at class level
- MCP_FORCE_FULL_TRACE_LOGS=false allows relaxation
- Strict trace logging should force fresh local server (not reuse)

## Key Connections
- [[mvp-site-testing-mcp-base-test]] — MCPTestBase class being tested
- [[mvp-site-capture-provenance]] — Provenance capture function
- [[mvp-site-world-content]] — System instruction integration

## Test Structure
- `test_test_file_is_defined_when_calling_capture_provenance` — Verifies test_file parameter passed
- `test_start_server_bootstraps_classifier_dependencies` — Verifies dependency bootstrap
- `test_base_test_default_user_email_is_empty_when_not_configured` — Verifies no hardcoded email
- `test_start_server_sets_test_user_email_header_from_env` — Verifies email header from env
- `test_require_full_trace_logs_forced_true_by_default` — Verifies default enforcement
- `test_require_full_trace_logs_can_be_relaxed_with_env_override` — Verifies env override
- `test_start_server_does_not_reuse_existing_server_when_strict_trace_enabled` — Verifies fresh server

## Related Sources
- [[mvp-site-test-basic-validation]] — Basic framework validation
- [[mvp-site-mvp-site-testing-mcp]] — Testing MCP integration