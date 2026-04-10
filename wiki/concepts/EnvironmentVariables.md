---
title: "Environment Variables"
type: concept
tags: [configuration, testing, environment]
sources: ["test-configuration-management"]
last_updated: 2026-04-08
---

Configuration values sourced from the operating system environment rather than hardcoded in application code. Used in test configuration to provide runtime flexibility and test isolation by allowing different service credentials per test environment.

## Related Concepts
- [[Test Isolation]] — keeping test environments separate from production
- [[Configuration Management]] — organizing and providing configuration to applications

## Examples from Wiki
- TEST_FIRESTORE_PROJECT
- TEST_GEMINI_API_KEY
- test_user_id / test_session_id
