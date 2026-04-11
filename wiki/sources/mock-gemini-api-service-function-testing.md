---
title: "Mock Gemini API Service for Function Testing"
type: source
tags: [python, mock, testing, gemini, llm-service, api-mocking]
source_file: "raw/mock-gemini-api-service-function-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a mock implementation of the Gemini LLM service for testing purposes. Provides realistic AI responses without making actual API calls, enabling tests to run in isolation with configurable response patterns.

## Key Claims
- **Interface Parity**: MockLLMClient accepts identical parameters to real Gemini client (model, temperature, max_output_tokens, top_p, top_k) for seamless swapping
- **Pattern-Based Responses**: Uses prompt content analysis to determine response type (initial_story, continue_story, hp_discrepancy, location_mismatch, mission_completion, validation_prompt)
- **Forced Response Modes**: Can be configured to trigger specific scenarios for testing edge cases
- **Call Tracking**: Tracks call_count and last_prompt for test verification

## Key Classes
- **MockLLMResponse**: Mimics real Gemini API response with text attribute
- **MockLLMClient**: Main mock client with generate_content method

## Key Functions
- **generate_content**: Generates mock responses based on prompt patterns
- **_determine_response_type**: Analyzes prompt to select appropriate response type
- **Response generators**: _generate_initial_story, _generate_continue_story, _generate_hp_discrepancy, _generate_location_mismatch, _generate_mission_completion, _generate_validation_response

## Connections
- [[MockLLMResponse]] — mock response object
- [[MockLLMClient]] — main mock client class
- [[SAMPLE_AI_RESPONSES]] — sample response fixtures
- [[FULL_STRUCTURED_RESPONSE]] — structured response fixture
- [[GOD_MODE_RESPONSE]] — god mode response fixture

## Contradictions
- None identified
