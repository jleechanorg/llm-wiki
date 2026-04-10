---
title: "Boundary-Level Mocking"
type: concept
tags: [testing, mocking, architecture]
sources: []
last_updated: 2026-04-08
---

## Definition
A testing pattern where only the lowest-level external API (e.g., Gemini generate_content_stream_sync) is mocked, while all internal logic (routing, prompt-building, JSON-parsing, orchestration) runs normally.

## Context
This pattern enables full-stack testing while maintaining test reliability. By mocking only at the boundary (the actual API call), tests can validate:
- Internal routing logic
- Prompt building
- JSON parsing
- Error handling in orchestrators

This is contrasted with mocking entire service modules, which masks internal bugs.

## Related
- [[empty-phase2-streaming-response-e2e-tests]]
- [[streaming-sse-contract-e2e-tests]]
