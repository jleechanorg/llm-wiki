---
title: "Fake LLM Provider"
type: concept
tags: [testing, mocking, llm]
sources: []
last_updated: 2026-04-08
---

Fake LLM Provider is a test double that mimics LLM behavior for controlled testing. The test patches `gemini_provider.generate_content_with_code_execution` to return predefined responses that reproduce specific bug scenarios.

## Test Usage
- Mocked at provider level for deterministic test behavior
- Allows reproduction of edge cases (embedded JSON in narrative)
- Controlled via environment variables for test isolation
