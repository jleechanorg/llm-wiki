---
title: "Structured Fields Fixtures"
type: concept
tags: [testing, fixtures, predefined-data]
sources: ["mock-gemini-service-wrapper"]
last_updated: 2026-04-08
---

## Description
Predefined test response data module containing FULL_STRUCTURED_RESPONSE and INITIAL_CAMPAIGN_RESPONSE constants. Provides deterministic test data for mock LLM responses.

## Purpose
Enables tests to use consistent, known responses rather than relying on mock randomness. Part of the test fixture pattern for game narrative generation.

## Connections
- [[MockGeminiServiceWrapper]] — imports and uses these fixtures
- [[MockLLMClient]] — may use fixtures for response generation
