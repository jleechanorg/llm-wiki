---
title: "Narrative Parsing Fallbacks"
type: concept
tags: [llm, parsing, error-handling]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Multi-layer fallback approach in `narrative_response_schema.py` for constructing `NarrativeResponse` from potentially malformed LLM output.

## Fallback Layers
1. Extract known fields from malformed JSON
2. Regex-parse narrative text
3. Clean JSON-like strings

## Rationale
LLM responses are nondeterministic and untrusted. User-facing flows need readable output rather than crashes. Does NOT hide configuration errors.
