---
title: "mvp_site openai_compatible_provider_core"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/openai_compatible_provider_core.py
---

## Summary
Shared core for OpenAI-compatible chat-completions providers. Centralizes message building, payload shape, tool_calls detection, and robust first-choice parsing. Each provider focuses on endpoint + auth + response_format.

## Key Claims
- generate_openai_compatible_content() calls OpenAI-compatible endpoints
- Centralized: message building, payload shape, tool_calls detection
- Each provider implements: endpoint, auth headers, response_format choice, provider-specific postprocessing
- extract_text_from_message_fn and postprocess_text_fn hooks for customization

## Connections
- [[LLMIntegration]] — shared provider core
