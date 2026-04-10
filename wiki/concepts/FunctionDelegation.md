---
title: "Function Delegation"
type: concept
tags: [programming-patterns, python, refactoring]
sources: [code-centralization-testing-utils-deduplication]
last_updated: 2026-04-08
---

Pattern where a function in one module simply calls an equivalent function in another module rather than re-implementing the logic. In Python, often achieved via import statements that bring the function into the local namespace.

## Example
```python
# Before (duplication):
def _get_next_iteration():
    # implementation here

# After (delegation):
from testing_utils.evidence import get_next_iteration as _get_next_iteration
```

## Verification
Tests verify delegation by checking that the imported function is the exact same object (`is`) as the canonical implementation, confirming no reimplementation exists.

## Related Concepts
- [[CodeCentralization]] — broader pattern
- [[ImportPatterns]] — Python module mechanics
- [[InterfaceSegregation]] — SOLID principle
