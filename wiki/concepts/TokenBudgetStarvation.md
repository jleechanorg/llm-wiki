---
title: "Token Budget Starvation"
type: concept
tags: [bug, regression, token-budget]
sources: ["output-token-budget-regression-tests"]
last_updated: 2026-04-08
---

## Description
A bug where output tokens are starved to near-zero when input tokens exceed a threshold. The original bug: when input exceeded GEMINI_COMPACTION_TOKEN_LIMIT (300K), the remaining calculation was `max(1, 300K - 301K) = 1 token`, completely starving output.

## The Fix
Use actual model context window (1M for Gemini 2.5 Pro) instead of compaction limit for output calculation. This ensures output has minimum OUTPUT_TOKEN_RESERVE_MIN tokens when there's headroom.

## Connection
- [[OutputTokenBudgetRegressionTests]] — tests for this bug fix
- [[ModelContextWindow]] — related concept that provides the proper limit
