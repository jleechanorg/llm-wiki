---
title: "Regression Testing"
type: concept
tags: [testing, quality-assurance, bugs]
sources: [css-variable-definition-validation-tests]
last_updated: 2026-04-08
---

## Definition
Regression testing is a type of software testing that ensures new changes do not break existing functionality. It involves re-running previously executed tests to verify that previously working features still work correctly after code changes.

## Purpose
- **Catch bugs early**: Detect issues before they reach production
- **Ensure stability**: Verify fixes don't introduce new problems
- **Safeguard features**: Prevent previously fixed bugs from reappearing

## CSS Regression Examples
- **Undefined variables**: A variable used in one CSS file isn't defined anywhere, causing silent failures
- **Theme breaking**: Changing a color variable breaks components expecting specific values
- **Layout shifts**: CSS changes cause elements to reflow unexpectedly

## Related Concepts
- [[CSSCustomProperties]] — common source of regression when undefined
- [[UnitTesting]] — granular tests that catch specific regression scenarios
- [[AutomatedTesting]] — CI-based regression guards that run on every change
