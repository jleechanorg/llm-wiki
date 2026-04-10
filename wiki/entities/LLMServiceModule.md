---
title: "LLMServiceModule"
type: entity
tags: [module, llm-service]
sources: ["tdd-tests-classify-raw-narrative-helper"]
last_updated: 2026-04-08
---

## Description
`mvp_site.llm_service` — Python module containing LLM service logic including the `_classify_raw_narrative` helper function that determines whether text should be used as a streaming narrative fallback.

## Related Pages
- [[TDDTestsClassifyRawNarrativeHelper]] — test suite defining the helper's contract
- [[NarrativeResponseSchema]] — defines `JSON_PARSE_FALLBACK_MARKER` constant
