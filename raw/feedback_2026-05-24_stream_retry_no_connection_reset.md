---
name: stream-retry-no-connection-reset
description: Stream (mutating) path must not retry ConnectionResetError — server already processed the action; retrying duplicates game effects
type: feedback
bead: none
---

## Rule

The stream path (`/interaction/stream`) executes **mutating operations** — it advances game state in Firestore. If a `ConnectionResetError` occurs after the server has processed the request, retrying will duplicate the action (double dice rolls, double story entries, etc.).

The non-stream path (idempotent reads) can safely retry `ConnectionResetError`.

## Fix (commit c02561c7b1)

Added `is_retryable_fn` parameter to `_run_with_transport_retry` in `testing_mcp/lib/base_test.py`:

```python
def _run_with_transport_retry(
    operation,
    *,
    message_suffix,
    health_warning,
    max_attempts=3,
    is_retryable_fn=_is_mcp_transient_transport_error,  # default = old behavior
) -> Any:
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except transport_errors as exc:
            if not is_retryable_fn(exc) or attempt >= max_attempts:
                raise
```

Stream path passes `is_retryable_fn=_is_stream_retryable_transport_error` which returns `True` only for pre-connection failures (`ConnectionRefused`, `"Errno 61"`), NOT for `ConnectionResetError`.

## Verification

Test `test_stream_process_action_does_not_retry_mutating_transport_failures` confirmed: 1 call (not 3) on `ConnectionResetError`.

**Why:** `_is_mcp_transient_transport_error` incorrectly marked `ConnectionResetError` as retryable for all paths. Stream path needs a stricter function.

**How to apply:** Any new transport retry wrapper for mutating operations must use `_is_stream_retryable_transport_error`, not the default `_is_mcp_transient_transport_error`.

## References

- Commit: `c02561c7b1` in PR #7074
- File: `testing_mcp/lib/base_test.py`
- Functions: `_run_with_transport_retry`, `_is_stream_retryable_transport_error`, `_is_mcp_transient_transport_error`
