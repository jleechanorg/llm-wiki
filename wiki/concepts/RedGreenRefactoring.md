---
title: "Red/Green Refactoring"
type: concept
tags: [tdd, testing, refactoring, methodology]
sources: []
last_updated: 2026-04-08
---

## Description
A test-driven development technique where:
1. **RED phase**: Write a test that fails, reproducing the bug
2. **GREEN phase**: Write minimal code to make test pass
3. **REFACTOR**: Improve code while keeping tests passing

## Application
Used to identify root causes by starting with a failing test that captures the exact bug scenario, then implementing the fix to make it pass.
