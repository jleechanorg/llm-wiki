---
title: "Gemini 2.5 Pro"
type: entity
tags: [model, google, llm]
sources: ["output-token-budget-regression-tests"]
last_updated: 2026-04-08
---

## Description
Google's Gemini 2.5 Pro model with 1M token context window. Used as DEFAULT_GEMINI_MODEL in the codebase. The context window is 3.3x larger than the old GEMINI_COMPACTION_TOKEN_LIMIT (300K), which caused the output token starvation bug when input exceeded 300K tokens.

## Connection
- [[OutputTokenBudgetRegressionTests]] — model with 1M context that this test validates
