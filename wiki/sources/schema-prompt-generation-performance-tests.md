---
title: "Schema Prompt Generation Performance Tests"
type: source
tags: [performance, schema, prompt-injection, caching, latency]
source_file: "raw/test_schema_prompt_performance.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Performance tests validating dynamic schema-to-prompt generation meets latency targets: schema doc generation at startup (<50ms per type, <500ms total), prompt loading with injection (<5ms overhead), and minimal server startup impact (<100ms).

## Key Claims
- **Cache Initialization**: init_schema_doc_cache() completes in <500ms for 10+ types, <50ms per individual type
- **Cached Retrieval**: get_cached_schema_doc() returns in <1ms on cache hits
- **Injection Overhead**: _inject_dynamic_schema_docs() adds <5ms vs baseline
- **Full Load Time**: Prompt loading with injection completes in <20ms

## Key Quotes
> "Schema doc generation at startup: <50ms per type, <500ms total for 10 types" — performance targets

> "Prompt loading with injection: <5ms overhead vs baseline" — injection performance

## Connections
- [[Schema Enforcement End-to-End Tests]] — schema validation infrastructure
- [[Prompt Loading Service Tests]] — prompt loading service behavior

## Contradictions
- None
