---
title: "Context Budget Design Document"
type: source
tags: [token-management, context-window, truncation, llm, architecture]
source_file: "raw/context-budget-design.md"
sources: ["PR #2311"]
last_updated: 2026-04-08
---

## Summary
Detailed architecture for token budget allocation in WorldArchitect.AI's LLM API calls. The system ensures story context fits within model-specific token limits while preserving narrative coherence. Implemented via PR #2311 with a December 2025 timeline log fix.

## Key Claims
- **No auto-fallback**: Automatic fallback to larger context models explicitly removed in PR #2311 — improve truncation instead
- **90% safety margin**: System uses 90% of model context window, reserving 20% for output generation
- **Percentage-based allocation**: Story budget divided as 25% start turns, 10% middle summary, 60% end turns
- **Fixed entity tracking**: 10,500 tokens fixed reserve for entity data added post-truncation
- **Variable turn handling**: Unlike fixed 20+20 truncation, percentage-based approach handles variable turn lengths

## Key Quotes
> "Context too large for model zai-glm-4.6: input uses 95,622 tokens, max allowed is 94,372 tokens (80% of 117,964)"

> "DO NOT add automatic fallback to larger context models. If ContextTooLargeError occurs, the solution is to improve truncation logic."

## Architecture Details
- **Context Budget Hierarchy**: Model Context Window → Safety Margin (90%) → Output Reserve (20%) → Max Input (80%) → Scaffold + Story Budget
- **Component Token Targets**: System instruction (5-8K), game state JSON (2-4K), checkpoint (1-2K), core memories (2-3K), entity tracking (10.5K fixed)
- **Algorithm**: Calculate safe budget → subtract output reserve → subtract scaffold → remaining is story budget → allocate by percentage

## Model Support
| Model | Context | Max Input (80%) |
|-------|---------|-----------------|
| gemini-2.0-flash | 1,000,000 | 720,000 |
| zai-glm-4.6 (Cerebras) | 131,072 | 94,372 |
| qwen-3-235b (Cerebras) | 131,072 | 94,372 |
| llama-3.3-70b (Cerebras) | 65,536 | 47,186 |

## Connections
- [[PR #2311]] — implementation that removed auto-fallback
- [[Context Window]] — concept for model token limits
- [[Token Management]] — system for allocating context budget
- [[Story Truncation]] — mechanism for fitting context within limits

## Contradictions
- None identified
