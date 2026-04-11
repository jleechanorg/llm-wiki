---
title: "Fake Firestore Implementation for Testing"
type: source
tags: [python, testing, firestore, fake-objects, json-serialization]
source_file: "raw/fake-firestore-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing stateful test doubles for Firestore, returning real data structures instead of Mock objects to avoid JSON serialization issues. Implements FakeFirestoreDocument and FakeQuery classes that simulate real Firestore behavior including deep copy semantics.

## Key Claims
- **Deep Copy Semantics**: Makes deep copies of data to simulate real Firestore behavior where stored data is independent of the original dict — critical for catching bugs where code modifies a dict after persisting it
- **Nested Field Support**: Handles dot-notation field updates like 'settings.gemini_model' for nested data structures
- **Query Chain Interface**: FakeQuery supports chaining (.where().order_by().limit()) matching Firestore SDK fluent API
- **Field Selection**: Implements .select() for projecting specific fields, reducing data transfer

## Key Classes
- `FakeFirestoreDocument`: Simulates document with set(), update(), get(), exists(), to_dict(), collection() methods
- `FakeQuery`: Fluent query builder with order_by, limit, where, start_after, select operations

## Connections
- Related to [[Fake Firebase Auth Service]] — same "Fake" pattern for test doubles
- Related to [[Service Provider Factory]] — used in test provider factory for database layer
- Implements concept: [[Fake Pattern]] — stateful test doubles vs traditional mocks

## Contradictions
- None identified
