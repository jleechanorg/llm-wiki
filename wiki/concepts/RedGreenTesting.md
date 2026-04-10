---
title: "Red/Green Testing"
type: concept
tags: [tdd, testing, methodology, red-green]
sources: [campaign-wizard-reset-red-green-test-html]
last_updated: 2026-04-08
---

## Description
Red/Green testing is a TDD (Test-Driven Development) methodology where tests are written in two phases: first the test fails (Red state), then implementation is added to make it pass (Green state). This HTML test interface is explicitly designed to start in Red state — the test is expected to fail initially.

## Application
Used for validating wizard reset functionality where:
- Red: Test fails because reset logic not yet implemented
- Green: Test passes after forceCleanRecreation and replaceOriginalForm are properly implemented

## Related Concepts
- [[TestDrivenDevelopment]] — broader methodology
- [[DOMManipulation]] — testing technique used
