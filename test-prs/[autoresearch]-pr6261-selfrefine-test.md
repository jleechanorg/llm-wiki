---
title: "SelfRefine Test: PR 6261"
type: test-result
pr: 6261
technique: SelfRefine
run_session: 2026-04-14
sources: []
tags: [selfrefine, pr-6261, autoresearch]
---

## PR Context
**Title:** refactor(rewards): migrate to centralized robust numeric extraction & simplify chaining
**Status:** MERGED

Two major fixes:
1. **Streaming passthrough normalization fix:** When streaming completion resolves without level-up signal, rewards box must still pass through `normalize_rewards_box_for_ui` for schema coercions (gold → gold_pieces).
2. **Robust numeric extraction:** DefensiveNumericConverter handles "500 XP", "1,000", "unknown", fractions like "10/20" via regex. Also adds OverflowError to exception handler.

## SelfRefine Iteration 1: Generate

### Predicted Fix 1: Streaming Passthrough
The bug: raw rewards_box was passed directly when `_has_level_up_ui_signal` was False, bypassing normalization.

Prediction: The fix would call `normalize_rewards_box_for_ui()` on the raw_box before assigning to canonical_stream when there's no level-up signal.

```python
# Old (buggy):
canonical_stream_rewards_box = raw_structured_rewards_box

# Predicted fix:
if not world_logic._has_level_up_ui_signal(...):
    canonical_stream_rewards_box = normalize_rewards_box_for_ui(raw_structured_rewards_box)
else:
    canonical_stream_rewards_box = raw_structured_rewards_box
```

### Predicted Fix 2: Robust Numeric Extraction
Prediction: Add regex to extract first number from string values like "500 XP", "1,000".

```python
# Predicted:
if isinstance(value, str):
    # Remove commas, extract first number
    match = re.search(r"\d+", value.replace(",", ""))
    if match:
        converted = int(match.group())
```

## SelfRefine Iteration 2: Critique

### What I Got Right
1. The core issue: passthrough bypasses normalization
2. Numeric extraction needed for string values with units
3. OverflowError should be caught

### What I Got Wrong / Missed
1. **Streaming logic complexity**: The actual fix is far more sophisticated - it refactors the entire resolution logic to use `_resolve_canonical_level_up_ui_pair()` as the primary path, not as a fallback. The function now always resolves first, then branches based on whether resolved_rb is None.

2. **Suppressed vs Resolved distinction**: I didn't anticipate the need to distinguish between:
   - `resolved_rb = None` because suppressed (has level-up UI signal but suppressed)
   - `resolved_rb = None` because no signal at all (normal passthrough)

3. **Regex pattern**: The actual regex `r"[-+]?[0-9]*\.?[0-9]+"` is more complete than my prediction - handles negatives, decimals, and edge cases.

4. **The key fix**: The canonical assignment moved INSIDE the resolution block - the raw box is no longer the default; resolution is always attempted first.

## SelfRefine Iteration 3: Revise

### Improved Predictions

**Streaming fix**: Not just a conditional wrap, but a complete refactor:
```python
# Actual pattern (simplified):
resolved_rb, resolved_pb = _resolve_canonical_level_up_ui_pair(...)
if resolved_rb is not None:
    canonical_stream_rewards_box = resolved_rb  # normalized
else:
    canonical_stream_rewards_box = None
    # then check suppressed vs no-signal
```

**Numeric extraction**: Matches actual implementation:
```python
value_no_commas = value.replace(",", "")
match = re.search(r"[-+]?[0-9]*\.?[0-9]+", value_no_commas)
if not match:
    raise ValueError(f"No numeric content found in '{value}'")
converted = int(float(match.group(0)))
```

## Actual Diff

### Defensive Numeric Converter
```diff
+import re
...
-        # Try to convert to integer
+        # Robust extraction: handle "500 XP", "1,000", "unknown", etc.
         try:
-            converted = int(value)
+            if isinstance(value, str):
+                value_no_commas = value.replace(",", "")
+                match = re.search(r"[-+]?[0-9]*\.?[0-9]+", value_no_commas)
+                if not match:
+                    raise ValueError(f"No numeric content found in '{value}'")
+                converted = int(float(match.group(0)))
+            else:
+                converted = int(value)
...
-        except (ValueError, TypeError):
+        except (ValueError, TypeError, OverflowError):
```

### Streaming Orchestrator
```diff
-                canonical_stream_rewards_box = raw_structured_rewards_box
-                canonical_stream_planning_block = raw_structured_planning_block
                 canonical_stream_suppressed = False
-                if world_logic._has_level_up_ui_signal(...):
+                (resolved_rb, resolved_pb) = world_logic._resolve_canonical_level_up_ui_pair(...)
+                if resolved_rb is not None:
+                    canonical_stream_rewards_box = resolved_rb
+                    canonical_stream_planning_block = resolved_pb
+                else:
+                    canonical_stream_rewards_box = None
+                    if world_logic._has_level_up_ui_signal(...):
                         canonical_stream_suppressed = True
-                        canonical_stream_rewards_box = None
```

## Diff Comparison

| Aspect | Prediction | Actual | Match |
|--------|-----------|--------|-------|
| Regex for numeric | `\d+` | `[-+]?[0-9]*\.?[0-9]+` | Partial |
| OverflowError catch | Mentioned | Added | ✓ |
| Normalization call | Conditional wrap | Full refactor to resolve-first | ✗ |
| Raw assign default | Removed | Removed | ✓ |
| Planning block handling | Not predicted | Separate branches | ✗ |

## Score

| Dimension | Weight | Score (0-10) | Weighted |
|-----------|--------|-------------|---------|
| Naming & Consistency | 15% | 8 | 1.2 |
| Error Handling & Robustness | 20% | 8 | 1.6 |
| Type Safety / Architecture | 20% | 7 | 1.4 |
| Test Coverage & Clarity | 15% | 7 | 1.05 |
| Documentation | 10% | 8 | 0.8 |
| Evidence-Standard Adherence | 20% | 8 | 1.6 |
| **TOTAL** | 100% | | **7.65** |

## Analysis

SelfRefine partially predicted this PR. The technique correctly identified:
- The need for numeric extraction from strings
- The normalization bypass bug in streaming

However, it underestimated:
- The complexity of the streaming orchestrator refactor (resolve-first pattern)
- The distinction between suppressed vs resolved-None cases
- The regex pattern details

The numeric extraction fix was well-predicted. The streaming fix was more sophisticated than anticipated - a full refactor rather than a simple conditional wrap. This PR demonstrates that SelfRefine works better when the fix is a targeted addition rather than a architectural refactor.
