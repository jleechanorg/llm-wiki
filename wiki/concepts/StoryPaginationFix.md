---
title: "StoryPaginationFix"
type: concept
tags: [testing, firestore, pagination, test-stability, determinism, rewards-box]
sources: [pr-6272-stabilize-story-pagination-tests]
last_updated: 2026-04-14
---

## Pattern

Add deterministic precondition guards to tests that depend on fake/in-memory implementations (e.g., `FakeFirestoreClient`). The guard verifies the fake is active before proceeding, failing fast with a clear message instead of producing subtle false-pass/false-fail results.

## FakeFirestore Guard Pattern

```python
# Deterministic guard: verify FakeFirestore is active before making pagination calls.
if not isinstance(firestore_service.get_db(), FakeFirestoreClient):
    self.fail("FakeFirestore not active — real Firestore in use (precondition)")
```

**Why this works:** When `FIRESTORE_EMULATOR_HOST` is not set, tests fall back to real Firestore, which has different pagination behavior than the in-memory fake. Without the guard, tests silently use wrong Firestore and produce incorrect results.

**Why `self.fail` instead of `assert`:** `self.fail` clearly signals a precondition violation at test setup time, distinct from assertion failures in the test body itself. This is intentional signaling, not error handling.

## Improved Assertion Messages

Replace bare assertions with diagnostic-rich messages:

```python
# Before
assert first_page["has_older"] is True

# After
assert first_page["has_older"] is True, (
    f"Expected has_older=True with 4 entries and limit=2, "
    f"got has_older={first_page['has_older']} (fetched={first_page.get('fetched_count')}, "
    f"total={first_page['total_count']})"
)
```

## `_coerce_first_valid` Helper

Refactors repetitive inline `max(0, coerce_int(...))` patterns into a testable helper that:

1. Takes a field key + multiple candidate values
2. Returns first candidate that coerces to a **positive** integer
3. Skips string-encoded zeros/invalids (`"0"`, `"0.0"`, `"n/a"`, `"none"`, `"null"`, `"unknown"`)
4. Skips regex-matched zero patterns (`"0 XP"`, `" 0 "`)
5. Honors literal `0` as an explicit award (returns it, not skipped)
6. Skips `None`, `bool`, and non-finite float

```python
def _coerce_first_valid(field_key: str, *candidates: Any) -> int:
    """Return the first candidate that coerces to a non-negative integer."""
    for val in candidates:
        if val is None or isinstance(val, bool):
            continue
        if isinstance(val, (int, float)) and val == 0:
            return _DNC.convert_value(field_key, val)
        if isinstance(val, str):
            stripped = val.strip().lower()
            if not stripped:
                continue
            if stripped in ("0", "0.0", "n/a", "none", "null", "unknown"):
                continue
            if re.match(r"^\s*0(?:\.0+)?(?:\s*[a-z%]*)?\s*$", stripped):
                continue
        if isinstance(val, float) and not math.isfinite(val):
            continue
        converted = _DNC.convert_value(field_key, val)
        if converted > 0:
            return converted
    return 0
```

**Test coverage:** 6 cases — empty string primary with secondary fallback, explicit zero, string-encoded combat rewards, rewards_pending precedence, zero-like strings rejected, unknown strings rejected.

## MCP Server Stop Guard

```python
try:
    self.server.stop()
except Exception as e:
    print(f"⚠️ Failed to stop shared local MCP server: {e}")
```

Prevents test crashes when MCP server stop fails (e.g., port already freed, permission issues).

## Anti-Pattern: Duplicate Imports from Failed Merge

This pattern's PR (#6272) introduced an anti-pattern: **unresolved git merge conflict markers committed directly into source code**. The PR branch has triple-duplicate `_DNC` imports grown from a failed merge that was never cleaned up. This caused `SyntaxError` on parse and is a BLOCKER for the PR.

**Prevention:** Never commit merge results with `<<<<<<< HEAD` conflict markers. Always resolve before committing.

## Connections

- [[dice-authenticity-standards]] — test determinism is a form of authenticity guarantee
- [[streaming-evidence-standards]] — video evidence gate; related to test stability
- [[PRWatchdog]] — monitors PR review state
- [[CanonicalCodePatterns]] — Python error handling patterns (try/except MCP server stop)
- [[Normalization Bypass via Streaming Passthrough]] — [[normalize_rewards_box_for_ui]] normalization atomicity; `_coerce_first_valid` prevents normalization bypass via zero-like strings
