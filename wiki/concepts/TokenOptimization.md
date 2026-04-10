---
title: "Token Optimization"
type: concept
tags: [token-reduction, context-management, optimization]
sources: ["context-optimization-implementation-plan", "context-budget-design-document", "context-components-reference"]
last_updated: 2026-04-08
---

## Summary
Systematic approach to reducing token consumption in LLM conversations through multiple techniques: output compression, context monitoring, and intelligent truncation.

## Techniques
1. **Output Trimming**: Compress slash command outputs via hook system
2. **Context Monitoring**: Track token usage with health levels (Green/Yellow/Orange/Red)
3. **Smart Truncation**: Preserve start/end turns, summarize middle (25%/10%/60% split from [[Context Budget Design Document]])
## Target Reductions
- Command outputs: 50-70% via trimming
- Context: 20% safety margin per [[Context Budget Design Document]]
- Story: 50-60% budget allocation
