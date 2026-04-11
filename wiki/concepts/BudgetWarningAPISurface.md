---
title: "Budget Warning API Surface"
type: concept
tags: [api, budget-allocation, llm, context, compaction]
sources: []
last_updated: 2026-04-11
---

## Description
LLM budget warnings are computed and stored in the `LLMResponse` object but never serialized to the API response. The `to_dict()` method exists but is never called in the main serialization path, silently discarding warning data.

## Symptoms
- Budget warnings computed in `llm_service.py:4315` and added to `LLMResponse`
- `LLMResponse.to_dict()` method exists with budget warning data
- Main API serialization in `main.py:2285` never calls `to_dict()`, returning raw object
- `warnings_count=0` in evidence bundles despite actual warnings

## Root Cause
The API response path serializes the `LLMResponse` object directly instead of calling `to_dict()`. The `to_dict()` method was added as an afterthought but the serialization code was not updated to use it.

## Evidence
```
# llm_service.py:4315 — warnings added to response
response.budget_warnings = warnings
response.warnings_count = len(warnings)

# main.py:2285 — to_dict() never called
return response  # raw object, no to_dict()
```

## Fix
Call `response.to_dict()` in the API serialization path, or add `warnings_count` and `budget_warnings` fields directly to the API response object.

## Connections
- [[Compaction]] — budget warnings are generated during compaction
- [[Context-Bloat]] — budget warnings exist to detect context overflow
