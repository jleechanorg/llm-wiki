---
title: "Type Coercion"
type: concept
tags: [programming, types, conversion]
sources: ["safe-arithmetic-utils-mvp-site"]
last_updated: 2026-04-08
---

## Description
Automatic or explicit conversion of values from one type to another. The `add_safe` function uses type coercion to accept ints, floats, and numeric strings, converting them to a common numeric type before addition while preserving integer return type when appropriate.

## Related Concepts
- [[DefensiveProgramming]] — safe coercion rather than strict type checking
- [[TypeGuards]] — runtime type verification

## Examples
- `"2"` coerced to `2` (int) before addition
- `"2.5"` coerced to `2.5` (float)
