---
title: "Status Code Normalization"
type: concept
tags: [http, utilities, defensive-programming]
sources: ["status-code-safe-arithmetic-utils-tests"]
last_updated: 2026-04-08
---

## Definition
A utility pattern for normalizing HTTP status codes with type coercion, range validation, and configurable default fallback values.

## Key Characteristics
- **Type Coercion**: Converts numeric strings ("200") to integers
- **Range Validation**: Validates codes fall within 100-599 HTTP status range
- **Default Fallback**: Returns configurable default on invalid input
- **Graceful Degradation**: Never raises exceptions; always returns valid code


## Implementation Pattern
```python
def normalize_status_code(value, default=200):
    if value is None:
        return default
    if isinstance(value, int):
        return value if 100 <= value <= 599 else default
    if isinstance(value, str) and value.isdigit():
        return int(value) if 100 <= int(value) <= 599 else default
    return default
```

## Related Concepts
- [[SafeArithmetic]] — similar defensive pattern for numeric operations
- [[DefensiveProgramming]] — overarching design philosophy
