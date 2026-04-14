---
title: "mvp_site cerebras_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/cerebras_provider.py
---

## Summary
Cerebras direct API provider using OpenAI-compatible chat completions endpoint. Handles schema echo issues (API returning config instead of content), nested JSON wrapper unwrapping, and model-not-found detection. Supports three tool flows: standard, JSON-first tool requests, and native two-phase.

## Key Claims
- Uses Cerebras OpenAI-compatible endpoint (api.cerebras.ai/v1/chat/completions)
- CerebrasSchemaEchoError detects when API echoes response_format schema instead of content
- _unwrap_nested_json() handles Cerebras wrapper pattern: {"type": "object", "json": {...actual...}}
- generate_content_with_tool_requests() uses JSON-first flow: JSON mode first, then tool execution if needed
- generate_content_with_native_tools() uses native two-phase tool calling for GLM-4.6 models
- Model auto-redirect: 404 model_not_found errors detected and handled

## Connections
- [[LLMIntegration]] — Cerebras as alternative LLM provider
- [[DiceMechanics]] — dice roll tools via tool calling flows
