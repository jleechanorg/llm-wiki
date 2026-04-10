---
title: "Idempotent"
type: concept
tags: [programming, mathematics, testing]
sources: [lazy-module-thread-safety-tests]
last_updated: 2026-04-08
---

## Description
A property of an operation where multiple identical requests have the same effect as a single request. _load_real_module is idempotent because calling it multiple times returns the exact same module object (using `is` comparison), not creating new objects each time.

## Key Properties
- Multiple calls return same result
- Used for cache/initialization patterns
- Verified via `result1 is result2 is result3`
- Important for thread-safe code

## Connections
- [[LazyLoading]] — _load_real_module should be idempotent
- [[ThreadSafety]] — idempotent operations are easier to make thread-safe
