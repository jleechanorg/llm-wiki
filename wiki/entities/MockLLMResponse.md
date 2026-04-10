---
title: "MockLLMResponse"
type: entity
tags: [python, mock, testing, gemini-api]
sources: [mock-gemini-api-service-function-testing]
last_updated: 2026-04-08
---

## Description
Mock response object that mimics the real Gemini API response structure. Used in test environments to simulate LLM responses without making actual API calls.

## Attributes
- **text**: String containing the response content

## Usage
Used by [[MockLLMClient]] to return mock responses in tests.

## Related
- [[MockLLMClient]] — creates MockLLMResponse instances
- [[MockGeminiServiceWrapper]] — alternative mock service implementation
