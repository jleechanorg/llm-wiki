---
title: "JSON_MODE_MAX_OUTPUT_TOKENS"
type: entity
tags: [constant, token-limit, llm-service]
sources: ["output-token-budget-regression-tests"]
last_updated: 2026-04-08
---

## Description
Constant defining the maximum output tokens when JSON mode is enabled. Referenced in output budget calculation as a cap on the output token limit independent of input size.

## Connection
- [[OutputTokenBudgetRegressionTests]] — uses this as ceiling for output budget
