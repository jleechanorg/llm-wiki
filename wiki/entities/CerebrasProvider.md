---
title: "Cerebras Provider"
type: entity
tags: [llm-provider, cerebras, api]
sources: []
last_updated: 2026-04-08
---

## Description
LLM provider module for Cerebras API. Lazy-loaded via `__getattr__` to optimize cold-start performance.

## Connections
- [[LLMProviderColdStartOptimization]] — implemented as lazy-loaded submodule
