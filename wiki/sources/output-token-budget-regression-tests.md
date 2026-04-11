---
title: "Output Token Budget Regression Tests"
type: source
tags: [python, testing, regression, token-budget, llm-service, context-window]
source_file: "raw/output-token-budget-regression-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Regression tests for output token budget calculation. These tests ensure the output token budget is calculated correctly based on the actual model context window (e.g., 1M for Gemini 2.5 Pro), not the compaction limit (300K). The bug being tested: previously when input exceeded 300K tokens, output was starved to just 1 token.

## Key Claims
- **Output budget calculation**: Uses actual model context window, not GEMINI_COMPACTION_TOKEN_LIMIT (300K) — fixes starvation bug when input > 300K
- **Output reserve minimum**: At least OUTPUT_TOKEN_RESERVE_MIN (1024) tokens when there's context headroom
- **Context exceeded error**: Raises ValueError when input exceeds 80% of safe context (reserving 20% for output)
- **Independence principle**: Output token budget independent of input size, capped at JSON_MODE_MAX_OUTPUT_TOKENS

## Key Quotes
> "Output budget uses ACTUAL model context window, not compaction limit. Compaction limit is only for INPUT compaction decisions." — explains the fix for the regression

> "Bug: When input > 300K (GEMINI_COMPACTION_TOKEN_LIMIT), remaining was calculated as: remaining = max(1, 300K - 301K) = 1 token - starving output completely!" — the original bug

## Connections
- [[LLMServiceTokenManagement]] — related token management tests
- [[LLMServiceErrorHandling]] — related LLM service tests
- [[ContextWindowSafetyRatio]] — related concept for context calculations

## Contradictions
- Contradicts earlier implementation that used COMPACTION_TOKEN_LIMIT for output calculations
