---
title: "Code Execution + JSON Mode"
type: concept
tags: [gemini, code-execution, json, structured-output, capabilities]
sources: ["shared-constants-configuration"]
last_updated: 2026-04-08
---

Technical capability enabling LLM to execute code AND return structured JSON in a single inference call. UNIQUE TO GEMINI 3.x among major providers.

## Provider Comparison
- **Gemini 3.x**: ✅ Single-inference code execution + JSON
- **OpenAI GPT-4o**: Cannot combine Code Interpreter with Structured Outputs
- **Anthropic Claude**: Uses orchestration-based approach (programmatic tool calling)

## Use Cases
- Running calculations and returning results as JSON
- Dynamic code execution with structured output
- Combined tool use with JSON responses

## Related
- [[Gemini]] — only provider with this capability
- [[Shared Constants Configuration]] — defines MODELS_WITH_CODE_EXECUTION set
