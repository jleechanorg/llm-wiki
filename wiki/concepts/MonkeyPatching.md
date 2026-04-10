---
title: "Monkey Patching"
type: concept
tags: [python, runtime-modification, testing, authentication]
sources: [clock-skew-credentials-patch]
last_updated: 2026-04-08
---

Monkey patching modifies library functions at runtime without changing source code. This module patches google.auth._helpers.utcnow to return adjusted time.

## Implementation Pattern
```python
_original_utcnow = _helpers.utcnow  # Store original
_helpers.utcnow = _adjusted_utcnow  # Replace with adjusted
```

## Safety Features
- Store original function for restoration
- Apply patch only once (_patch_applied flag)
- Context manager for temporary bypass (UseActualTime)

## Related
- [[ClockSkewCredentialsPatch]] — primary use case
- [[ContextManager]] — Python pattern for temporary state
- [[GoogleAuth]] — library being patched
