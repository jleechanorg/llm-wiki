---
title: "Settings Page - AI Provider Selection"
type: source
tags: [settings, ai-providers, model-selection, gemini, openrouter, cerebras, openclaw, html-templates]
source_file: "raw/settings-page-ai-provider-selection.md"
sources: []
last_updated: 2026-04-08
---

## Summary
HTML template for WorldAI settings page enabling users to select their preferred LLM provider and model. Supports four providers: Gemini (Google), OpenRouter, Cerebras, and OpenClaw Gateway (local HTTP). Each provider has specific model options optimized for tabletop RPG storytelling.

## Key Claims
- **Four AI Providers** — Gemini, OpenRouter, Cerebras, and OpenClaw Gateway with radio button selection
- **Provider-Specific Models** — Each provider shows only relevant models in dropdown selection
- **Dynamic UI** — Model selection dropdowns toggle based on provider selection
- **Default Selection** — Gemini 3 Flash as default model for best value/performance balance
- **Local Gateway Option** — OpenClaw Gateway for local HTTP inference (default port 18789)

## Key Quotes
> "Choose which LLM provider powers your adventures."

> "Community frontier models tuned for tabletop creativity." — OpenRouter description

> "Direct Cerebras inference for low-latency frontier models (Qwen, GLM, Llama)." — Cerebras description

## Connections
- [[Gemini]] — Google LLM service with structured output capability
- [[OpenRouter]] — Aggregator service for frontier models
- [[Cerebras]] — Low-latency inference provider
- [[OpenClaw Gateway]] — Local HTTP gateway for open-source models
- [[Llama]] — Meta's open-source model series
- [[GLM]] — Z-AI's large language model
- [[Grok]] — xAI's flagship model with 2M context

## Contradictions
- []
