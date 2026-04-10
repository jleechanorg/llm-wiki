---
title: "Race Condition"
type: concept
tags: [concurrency, bug, threading]
sources: [lazy-module-thread-safety-tests]
last_updated: 2026-04-08
---

## Description
A bug that occurs when code behavior depends on the relative timing of concurrent operations. In the lazy loading context, a race condition occurs when two threads check _real_module is None simultaneously and both trigger importlib.import_module(), causing double imports.

## Key Properties
- Timing-dependent bug
- Multiple threads access shared state
- Can cause double imports, data corruption
- Prevented with locking

## Connections
- [[ThreadSafety]] — the solution to race conditions
- [[LazyLoading]] — context where race conditions occur
- [[MvpSite]] — the module being tested for race conditions
