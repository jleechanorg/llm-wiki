---
title: "Two-Stage Inference"
type: concept
tags: [llm-providers, inference-pattern, tool-calls]
sources: []
last_updated: 2026-04-08
---

An inference pattern where the LLM makes two passes: first to determine if a tool (like dice roll) should be called, second to process the tool result and generate the final narrative. The Cerebras provider uses this for dice rolling in the game system.

## Related Pages
- [llm-provider-tool-request-tests](../sources/llm-provider-tool-request-tests.md) — tests validating this pattern
- [ToolRequestHandling](ToolRequestHandling.md) — general concept
- [Cerebras](../entities/Cerebras.md) — implements two-stage inference for dice rolling
