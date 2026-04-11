---
title: "Fake LLM Service for Testing"
type: source
tags: [python, testing, llm, fake-objects, mock, gemini]
source_file: "raw/fake-llm-service-for-testing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing stateful test doubles for LLM/Gemini responses, returning realistic response structures instead of Mock objects to avoid JSON serialization issues. Implements FakePart, FakeLLMResponse, FakeGenerationConfig, and FakeModelAdapter classes that mimic the real Gemini SDK response interface.

## Key Claims
- **Fake Pattern**: Stateful test doubles that behave like real LLM responses, not just verifying call assertions
- **Complete Response Interface**: FakeLLMResponse implements full response interface with text, usage_metadata, parts, candidates, and content attributes
- **Generation Config Support**: FakeGenerationConfig mirrors real config with temperature, max_output_tokens, and response_schema
- **Response Templates**: FakeModelAdapter provides predefined templates for campaign_creation and story_continuation with placeholder substitution

## Key Classes
- **FakePart**: Fake part object for Gemini response structure with text and function_call attributes
- **FakeLLMResponse**: Full LLM response mock with text, usage_metadata, parts, candidates, and content
- **FakeGenerationConfig**: Generation config with temperature, max_output_tokens, response_schema
- **FakeModelAdapter**: Model adapter with response templates for common game scenarios

## Connections
- [[Fake Firestore Implementation]] — similar fake pattern for Firestore test doubles
- [[Realistic Firebase Auth test doubles]] — similar fake pattern for Firebase Auth
- [[Service Provider Factory for Tests]] — factory for creating test providers including this fake LLM

## Contradictions
- None identified
