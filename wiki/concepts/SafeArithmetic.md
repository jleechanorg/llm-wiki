---
title: "Safe Arithmetic"
type: concept
tags: [utilities, defensive-programming, floating-point]
sources: ["status-code-safe-arithmetic-utils-tests"]
last_updated: 2026-04-08
---

## Definition
A utility pattern for performing arithmetic operations with type coercion, null safety, and floating-point precision handling.

## Key Characteristics
- **Type Coercion**: Handles int, float, and numeric strings uniformly
- **Null Safety**: Treats None and invalid inputs as 0 or returns default
- **Precision Guard**: Uses `math.isclose` for floating-point comparisons
- **Mixed Type Support**: Can add strings to floats, ints to strings

## Implementation Pattern
```python
import math

def add_safe(a, b, default=0):
    try:
        # Attempt numeric coercion
        result = float(a) + float(b)
        # Return int if both inputs were int-like
        if isinstance(a, int) and isinstance(b, int):
            return int(result)
        return result
    except (TypeError, ValueError):
        return default
```

## Floating-Point Precision
The classic 0.1 + 0.2 ≠ 0.3 problem requires careful comparison:
```python
math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12)
```

## Related Concepts
- [[StatusCodeNormalization]] — similar defensive utility pattern
- [[DefensiveProgramming]] — overarching design philosophy
