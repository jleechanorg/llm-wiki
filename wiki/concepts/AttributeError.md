---
title: "AttributeError"
type: concept
tags: [python, error, type-safety]
sources: ["mode-parameter-type-validation-tests"]
last_updated: 2026-04-08
---

## Summary
Python runtime error that occurs when code attempts to call a method or access an attribute that doesn't exist on an object. Common when assuming wrong type (e.g., calling .lower() on a dict instead of string).

## Prevention
- Type validation before method calls
- isinstance() checks for expected types
- Default parameter handling for missing/invalid types

## Related Bugs
- [[Mode Parameter Type Validation]] — 'dict' object has no attribute 'lower'
