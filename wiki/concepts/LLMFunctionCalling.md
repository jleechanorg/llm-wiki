---
title: "LLM Function Calling"
type: concept
tags: [llm, function-calling, gemini, api, tools]
sources: [faction-tool-definitions-lambda]
last_updated: 2026-04-08
---

Pattern where LLM calls backend Python functions instead of manually applying formulas from prompts. Backend executes calculations and returns results to LLM for narrative integration.

## Why Use Function Calling
- **Accuracy**: Backend executes deterministic calculations
- **Consistency**: Same logic regardless of prompt variation
- **Performance**: Backend code more efficient than LLM computation

## Related Patterns
- [[DicePy]] — similar pattern for dice rolling
- [[FactionToolDefinitions]] — faction-specific tools
- [[GeminiAPI]] — underlying API for function calling
