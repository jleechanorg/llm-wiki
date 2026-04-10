---
title: "MagicMock"
type: concept
tags: [python, mocking, unittest, testing]
sources: []
last_updated: 2026-04-08
---

## Definition
MagicMock is a Python unittest.mock class that creates flexible mock objects that mimic any attribute or method access. It automatically creates attributes on access, allowing test code to chain method calls (e.g., mock.collection().document().get()) without implementing the full interface.

## Use Case
Isolating unit tests from external dependencies like databases, APIs, or file systems by providing controlled mock objects that return predictable values.

## Related
- [[UnitTesting]]
- [[FirestoreMocking]]
- [[PythonUnittest]]
