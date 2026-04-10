---
title: "Context Truncation"
type: concept
tags: [llm-context, memory-management, optimization]
sources: []
last_updated: 2026-04-08
---

## Description
Process of reducing LLM request context to fit within token limits. When truncating, most recent content is preserved as it's most relevant to current state.

## Truncation Strategy
- Keep most recent entries (highest sequence IDs)
- Remove oldest entries first
- Apply budget caps AFTER measurement on same context used for construction

## Related
- [[SequenceIDBudgetEnforcement]]
- [[TokenBudgetCalculation]]
- [[LLMRequestContext]]
