---
title: "Test Skip Policy - Middle Ground Approach"
type: source
tags: [testing, skip-policy, ci, quality-assurance, python]
sources: []
source_file: worldarchitect.ai-docs-test-skip-policy.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Defines a policy distinguishing legitimate environmental test skips (external dependencies, missing resources) from inappropriate lazy skips (implementation avoidance, unmocked dependencies). Provides clear patterns for when `self.skipTest()` is appropriate versus when tests should be fixed or mocked.

## Key Claims
- **Legitimate Skips**: Environmental unavailability (missing fonts, Git, credentials) and CI limitations warrant `self.skipTest()` rather than failing tests
- **Forbidden Skips**: Lazy implementation avoidance patterns like unmocked dependencies, "sometimes fails" tests, or "too hard" setup issues must be fixed, not skipped
- **Enforcement**: Scripts detect `self.fail()` with "skip" in message (should be `self.skipTest()`) and mockable skips that avoid proper test isolation
- **Format Standardization**: Skip messages must follow format "RESOURCE not available: SPECIFIC_REASON, skipping TEST_PURPOSE"

## Key Quotes
> "Skip reason is environmental, not implementation laziness" — code review checklist requirement
> "Skip could not be reasonably replaced with mocking" — mandatory check before allowing skip

## Connections
- [[Authentication Resilience Test Suite - CI Run]] — related testing policies in same project
- [[V1 vs V2 Integration Test Comparison]] — test execution patterns

## Contradictions
- None identified — this policy complements existing test practices

## Files Requiring Fixes
1. `mvp_site/tests/test_generator_isolated.py:69`
2. `mvp_site/tests/test_infrastructure.py:161`
3. `mvp_site/tests/test_infrastructure.py:210`

All use `self.fail()` with "skip" message instead of `self.skipTest()`.