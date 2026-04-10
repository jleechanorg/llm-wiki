---
title: "Provider-Agnostic Extraction"
type: concept
tags: [llm-providers, abstraction, extraction]
sources: [faction-minigame-state-access-utilities]
last_updated: 2026-04-08
---

The design pattern of creating utilities that work across multiple LLM providers (Gemini, OpenRouter, Cerebras, OpenClaw) without requiring provider-specific logic. Provider-agnostic extraction abstracts away the differences in how each provider structures prompt_contents and game_state data.
