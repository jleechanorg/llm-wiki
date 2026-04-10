---
title: "Static Method Testing"
type: concept
tags: [testing, python, coverage, unit-testing]
sources: ["mission-handler-tests-firestore-service"]
last_updated: 2026-04-08
---

## Description
Testing approach for class static methods that don't require class instantiation. In Python unittest, static methods are tested by calling ClassName.method_name() directly without creating instances.

## Key Patterns
- Direct invocation via class: `MissionHandler.initialize_missions_list(state, key)`
- Mock external dependencies (e.g., patch logging_util)
- Test edge cases: missing keys, invalid types, empty collections
- Validate state mutations after method execution

## Coverage Target
This test suite targets improving coverage from 61% to 70% for the MissionHandler class.

## Related
- [[MissionHandler]] — the class being tested
- [[Unit Testing]] — broader testing concept
- [[FirestoreService]] — module containing the tested class
