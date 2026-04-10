---
title: "Defensive Programming"
type: concept
tags: [programming-pattern, error-handling, validation]
sources: ["safe-arithmetic-utils-mvp-site"]
last_updated: 2026-04-08
---

## Description
Programming practice of anticipating and handling edge cases, invalid inputs, and failure modes rather than allowing exceptions to propagate. The `add_safe` function exemplifies defensive programming by coercing types and returning caller-provided defaults instead of raising exceptions.

## Related Patterns
- [[TypeCoercion]] — converting between types safely
- [[FailFast]] — opposite pattern that crashes on invalid input

## Examples
- `add_safe("bad", 1, default=999)` returns `999` instead of raising ValueError
- `normalize_status_code(None)` returns default 200 instead of crashing
