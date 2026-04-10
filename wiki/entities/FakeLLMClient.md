---
title: "FakeLLMClient"
type: entity
tags: [testing, llm, mocking, fake-service, gemini]
sources: [fake-services-unit-tests]
last_updated: 2026-04-08
---

A fake LLM client implementation created via `create_fake_llm_client()` for testing. Generates realistic JSON responses mimicking Gemini API behavior.

## Purpose
Enables isolated testing of LLM-dependent code without calling actual API endpoints.

## Key Capabilities
- Campaign creation prompt handling
- Story continuation with context preservation
- Structured JSON output with narrative, mechanics, scene fields
- Matches Gemini model API surface

## Connected To
- [[FakeFirestoreClient]] — stores generated content
- [[FakeFirebaseAuth]] — provides user context
- [[FakeServicesPattern]] — testing methodology
- [[GeminiAPI]] — real API being mocked
