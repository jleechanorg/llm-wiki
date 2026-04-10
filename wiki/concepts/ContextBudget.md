---
title: "Context Budget"
type: concept
tags: [context-management, model-limits]
sources: [adaptive-context-truncation-tests]
last_updated: 2026-04-08
---

## Description
The maximum number of tokens allowed for model input, determined by the model's context window size. For models with smaller limits (e.g., Cerebras 131K), adaptive truncation ensures content fits within this budget.

## Connections
- [[Token Estimation]] — measures content against budget
- [[Adaptive Context Truncation]] — responds to budget constraints
- [[Cerebras]] — example model with 131K context limit
