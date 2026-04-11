---
title: "LazyModule Thread Safety Tests"
type: source
tags: [python, testing, thread-safety, lazy-loading, concurrency]
source_file: "raw/test_lazy_module_thread_safety.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite verifying that _LazyModule handles concurrent access safely without causing double imports. Tests confirm a race condition scenario where multiple threads could trigger importlib.import_module() simultaneously, and validate that _load_real_module is idempotent.

## Key Claims
- **No double imports under concurrency**: 10 concurrent threads should trigger only ONE module import
- **Race condition protection**: Thread A and B checking _real_module is None before A finishes is handled
- **_load_real_module idempotent**: Multiple calls return the exact same module object
- **Mock import simulates slow load**: 0.01s wait increases race window to expose the bug

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| concurrent_loading_does_not_double_import | 10 threads access lazy module | import_count == 1 |
| load_real_module_is_idempotent | 3 calls to _load_real_module | result1 is result2 is result3 |

## Connections
- [[ThreadSafety]] — the core concept being tested
- [[LazyLoading]] — the pattern _LazyModule implements
- [[RaceCondition]] — the bug the tests expose
