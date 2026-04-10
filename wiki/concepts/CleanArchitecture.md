---
title: "Clean Architecture"
type: concept
tags: [architecture, design-patterns, separation-of-concerns]
sources: ["llm-response-gemini-api-wrapper.md"]
last_updated: 2026-04-08
---

## Definition
Software design pattern that separates concerns into distinct layers, keeping business logic independent of frameworks and delivery mechanisms.

## Application
In the LLMResponse class, clean architecture separates the AI service layer (Gemini API) from the main application by providing a standardized wrapper that abstracts provider-specific details and exposes a consistent interface.

## Related Concepts
- [[Structured Response Handling]]
- [[API Wrapper Patterns]]
