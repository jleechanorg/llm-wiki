---
title: "LLMResponse"
type: concept
tags: [class, response-wrapper, pydantic]
sources: ["mock-gemini-service-wrapper"]
last_updated: 2026-04-08
---

## Description
Python class (likely Pydantic model) that wraps LLM API responses. Used throughout the mock service for consistent response handling.

## Connections
- [[NarrativeResponse]] — specific response schema for game narratives
- [[MockLLMClient]] — produces LLMResponse instances
