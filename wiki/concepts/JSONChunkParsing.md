---
title: "JSON Chunk Parsing"
type: concept
tags: [json, parsing, streaming, llm, incremental]
sources: []
last_updated: 2026-04-08
---

## Definition
JSON chunk parsing refers to the challenge of extracting meaningful data from incomplete JSON fragments as they arrive via LLM streaming responses. The StreamingClient must handle partial JSON chunks where the LLM has not yet completed sending the full response.

## Key Challenges
- **Partial Keys**: Extracting thinking content when only partial key names or values have arrived
- **Incomplete Structures**: Detecting when JSON is missing closing braces or quotes
- **Streaming Accumulation**: Progressive accumulation of content across multiple chunks
- **Escape Handling**: Managing escaped characters within partial strings

## Key Patterns
- **Partial Value Extraction**: Extract thinking text even when quote is unclosed
- **Incomplete Detection**: `_looksLikeIncompleteStructuredEnvelope` checks for missing braces
- **Progressive Accumulation**: Append chunks to build complete values over time

## Related Concepts
- [[UnitTesting]] — testing parsing functions
- [[StreamingProtocol]] — SSE streaming protocols

## Sources
- [[StreamingClient Unit Tests for Extraction Functions]] — tests for parsing functions
