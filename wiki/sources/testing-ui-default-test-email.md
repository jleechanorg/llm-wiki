---
title: "Testing UI Default Test Email"
type: source
tags: [testing, python, configuration, environment]
source_file: "raw/testing-ui-default-test-email.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating DEFAULT_TEST_EMAIL defaults to jleechantest@gmail.com when TEST_USER_EMAIL and BYOK_TEST_USER_EMAIL environment variables are unset. Tests verify BrowserTestBase and ByokBrowserTestBase base classes correctly pick up default email when no env var is set, and respect env var overrides when present.

## Key Claims
- **Default Email**: Both test base classes default to jleechantest@gmail.com when their respective env vars (TEST_USER_EMAIL, BYOK_TEST_USER_EMAIL) are not set
- **Env Override**: TEST_USER_EMAIL env var overrides BrowserTestBase default; BYOK_TEST_USER_EMAIL env var overrides ByokBrowserTestBase default
- **Test Isolation**: Tests use testing_auth_bypass=True to avoid real authentication during test execution

## Key Quotes
> "BrowserTestBase defaults to jleechantest@gmail.com when TEST_USER_EMAIL not set"

## Connections
- [[testing_ui]] — the testing module these test base classes belong to
- [[BrowserTestBase]] — base class for browser tests with configurable test user email
- [[ByokBrowserTestBase]] — BYOK variant of browser test base class

## Contradictions
- None identified
