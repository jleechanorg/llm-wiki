---
title: "Output Token Reserve"
type: concept
tags: [token-budget, context-management, resource-allocation]
sources: ["output-token-budget-regression-tests"]
last_updated: 2026-04-08
---

## Description
A portion of the model's context window reserved for output generation. Default ratio is 20% (OUTPUT_TOKEN_RESERVE_RATIO). Minimum reserve is OUTPUT_TOKEN_RESERVE_MIN (1024 tokens). When input exceeds 80% of safe context, raises ValueError since there's insufficient room for quality output.

## Formula
```
safe_context = model_context * CONTEXT_WINDOW_SAFETY_RATIO (0.9)
output_reserve = safe_context * OUTPUT_TOKEN_RESERVE_RATIO (0.2)
max_input = safe_context - output_reserve  # = 80% of safe context
```

## Connection
- [[OutputTokenBudgetRegressionTests]] — core concept being tested
- [[ContextWindowSafetyRatio]] — related ratio concept
