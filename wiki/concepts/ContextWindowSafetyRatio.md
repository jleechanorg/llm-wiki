---
title: "ContextWindowSafetyRatio"
type: concept
tags: [tokens, safety, models]
sources: ["context-budgeting-allocation-tdd-tests"]
last_updated: 2026-04-08
---

## Description
Safety ratio applied to model context window to determine safe maximum input tokens. Prevents hitting hard limits by reserving buffer space.

## Formula
```
safe_tokens = context_window_tokens × CONTEXT_WINDOW_SAFETY_RATIO
```

## Fallback
For unknown models/providers, uses DEFAULT_CONTEXT_WINDOW_TOKENS × CONTEXT_WINDOW_SAFETY_RATIO
