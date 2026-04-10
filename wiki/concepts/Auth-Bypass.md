---
title: "Auth Bypass"
type: concept
tags: [testing, authentication, environment-variables]
sources: []
last_updated: 2026-04-08
---

## Description
Testing technique using TESTING_AUTH_BYPASS environment variable to disable authentication verification in end-to-end tests, allowing tests to run without real Firebase auth tokens.

## Usage
- Set os.environ["TESTING_AUTH_BYPASS"] = "true" before creating app
- Also set TEST_USER_ID to define the authenticated user
- Used in conjunction with auth patch targeting main.auth.verify_id_token

## Related
- [[TestVisitCampaignEnd2End]] - uses this pattern
- [[End-to-End Testing]] - testing methodology
