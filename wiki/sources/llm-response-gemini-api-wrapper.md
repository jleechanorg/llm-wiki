---
title: "LLMResponse Class for Gemini API Responses"
type: source
tags: [gemini, response-handling, clean-architecture, pydantic, serialization]
source_file: "raw/llm-response-gemini-api-wrapper.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Gemini Response wrapper providing clean architecture between AI service and main application. Handles structured response parsing from Pydantic models, JSON serialization with datetime handling, and budget warning tracking for system instruction overages.

## Key Claims
- **Clean Architecture Pattern**: Separates AI service layer from application with `LLMResponse` wrapper class
- **Pydantic Model Serialization**: Uses `model_dump(mode="json")` for proper datetime and type serialization
- **Backward Compatibility**: Supports both new `NarrativeResponse` Pydantic objects and legacy formats
- **Budget Warnings**: Tracks system instruction budget overages (e.g., >40% of total budget) for UI display
- **Debug Metadata**: Stores raw response text, processing metadata, and debug tag detection results

## Key Code Patterns
```python
# Serialization with Pydantic support
serialized = response.model_dump(mode="json") if hasattr(response, "model_dump") else response.dict()

# Budget warnings for system instruction overage
budget_warnings.append({"type": "system_instruction_overage", "percentage": 42})
```

## Connections
- [[NarrativeResponse]] — Pydantic model parsed from LLM output
- [[JSON Serialization]] — handles datetime and non-JSON types via custom serializer
- [[LLMRequest Class for Structured JSON Input to Gemini API]] — paired class for request/response handling

## Contradictions
- None identified
