---
title: "Token Budget Calculation"
type: concept
tags: [tokens, budget, performance]
sources: []
last_updated: 2026-04-08
---

## Description
Process of calculating token budgets for different components of LLM request context (story, sequence IDs, system prompts). Uses `estimate_tokens` function to measure text length and enforce budget limits.

## Key Points
- Story context bounded to 20% of total for sequence ID measurement
- Allocated budget from `budget_result` determines max sequence IDs
- Must measure and cap on same context to avoid mismatch


## Related
- [[SequenceIDBudgetEnforcement]]
- [[ContextTruncation]]
- [[token_utils]]
