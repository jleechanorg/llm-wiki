---
title: "Narrative Classification"
type: concept
tags: [classification, text-processing, streaming-fallback]
sources: ["tdd-tests-classify-raw-narrative-helper"]
last_updated: 2026-04-08
---

## Definition
The process of determining whether raw text output from an LLM should be used as a streaming narrative fallback. The `_classify_raw_narrative(text) -> bool` helper implements this logic.

## Classification Rules
| Input Type | Returns | Rationale |
|------------|---------|----------|
| Plain prose ("You wait.") | True | Valid narrative text |
| Short narrative (≤20 chars) | True | Not rejected |
| JSON quoted string | True | `json.loads()` produces str |
| Empty/whitespace | False | No content |
| JSON_PARSE_FALLBACK_MARKER | False | Marker, not content |
| JSON object/array | False | Container, not narrative |
| JSON scalar (null, true, false, number) | False | Not narrative text |
| Text with no alpha chars | False | Not readable prose |
| Malformed JSON ({ or [) | False | Prevents raw JSON being stored as story |

## Related Concepts
- [[JSONParseFallbackMarker]] — marker for fallback responses
- [[StreamingFallback]] — when LLM JSON parsing fails, use raw text
