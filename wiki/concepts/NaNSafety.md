---
title: "NaN Safety"
type: concept
tags: [python, floating-point, edge-cases, validation]
sources: [centralized-numeric-conversion-utilities]
last_updated: 2026-04-08
---

## Definition
Handling of NaN (Not a Number) values in numeric conversions. In Python, `float('nan')` raises ValueError when passed to `int()`.

## Implementation Pattern
```python
try:
    return int(float(value))
except (ValueError, TypeError, OverflowError):
    return default
```

## Why It Matters
NaN values from LLM responses or JSON parsing can cause runtime errors if not handled explicitly.
