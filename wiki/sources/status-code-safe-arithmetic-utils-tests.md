---
title: "Status Code and Safe Arithmetic Utils Tests"
type: source
tags: [testing, utils, tdd, mvp-site]
source_file: "raw/status_code_utils_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating two utility functions in `mvp_site/utils.py`: `normalize_status_code` for HTTP status code normalization with coercion and fallback defaults, and `add_safe` for safe arithmetic operations with type coercion and floating-point precision handling.

## Key Claims
- **Status Code Normalization**: Valid integer codes pass through unchanged; numeric strings are coerced to int
- **Default Handling**: None and invalid values return configurable default (default: 200)
- **Range Validation**: Status codes outside 100-599 range return default
- **Safe Arithmetic**: `add_safe` handles integers, floats, numeric strings with type coercion
- **Precision Guard**: Floating-point precision issues handled with `math.isclose` for comparisons
- **Graceful Degradation**: Invalid inputs return default value instead of raising exceptions

## Test Coverage
- `test_valid_int_passthrough`: Valid 200, 404, 500 returned unchanged
- `test_string_numeric_converted`: "200" -> 200, "404" -> 404
- `test_none_returns_default`: None returns default (200 or custom)
- `test_invalid_value_returns_default": "ok", [], {} return default
- `test_out_of_range_returns_default`: 99, 600, 0 return default
- `test_boundary_values`: 100 and 599 are valid boundaries
- `test_add_integers`: 2 + 3 = 5, returns int
- `test_add_floats`: 2.5 + 0.5 = 3.0, returns float
- `test_add_numeric_strings": "2" + "3" = 5
- `test_add_mixed_types": "2" + 3.5 = 5.5
- `test_none_or_invalid_returns_default`: None/bad inputs return 0
- `test_float_precision_guard`: 0.1 + 0.2 ≈ 0.3

## Connections
- [[StatusCodeNormalization]] — related concept for HTTP status code handling
- [[SafeArithmetic]] — related concept for defensive arithmetic operations
- [[DefensiveProgramming]] — design pattern embodied by these utilities
