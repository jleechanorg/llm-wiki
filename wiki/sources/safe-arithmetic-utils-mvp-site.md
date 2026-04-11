---
title: "Safe Arithmetic Utils for mvp_site"
type: source
tags: [python, utilities, defensive-programming, type-safety]
source_file: "raw/mvp_site_utils.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility module providing defensive arithmetic functions for mvp_site, including `add_safe` for type-coerced addition with caller-provided defaults on invalid inputs, complementing the existing `normalize_status_code` utility.

## Key Claims
- **add_safe**: Defensively adds two numeric-like values (int/float/str), returns `default` on failure
- **Type Preservation**: Returns `int` if both inputs are integral post-coercion, otherwise `float`
- **Invalid Input Handling**: Returns `default` when inputs are `None`, non-numeric, or non-finite
- **Complements normalize_status_code**: Similar scope and defensive style for HTTP status coercion

## Key Quotes
> "Centralizing safe addition reduces duplication and edge-case bugs"

## Connections
- [[UnifiedAPIImplementation]] — uses these utilities for request/response handling
- [[ValidationModule]] — defensive validation patterns for game state


## Contradictions
- None
