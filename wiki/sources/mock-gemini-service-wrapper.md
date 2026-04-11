---
title: "Mock Gemini Service Wrapper"
type: source
tags: [python, mock, testing, gemini, llm-service]
source_file: "raw/mock-gemini-service-wrapper.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a mock implementation of the Gemini LLM service for testing purposes. Mirrors the interface of the real llm_service module, enabling tests to run in isolation without making actual API calls to Gemini.

## Key Claims
- **Interface Parity**: Mock functions accept identical parameters to real service (temperature, max_output_tokens, top_p, top_k, response_mime_type, response_schema) for seamless swapping
- **Module-Level Singleton**: Uses global `_client` instance for consistent state across function calls
- **Fallback Narrative**: Contains embedded fallback story content with Sir Kaelan the Adamant character when fixtures unavailable
- **Structured Response Support**: Returns NarrativeResponse objects matching production schema

## Key Functions
- **get_client()**: Returns singleton MockLLMClient instance
- **generate_content()**: Mock API call accepting all standard Gemini parameters
- **get_initial_story()**: Returns predefined campaign narrative with session header and state updates

## Connections
- [[MockLLMClient]] — underlying mock client implementation
- [[LLMResponse]] — response wrapper class
- [[NarrativeResponse]] — structured response schema for game narratives
- [[structured_fields_fixtures]] — predefined test response data
