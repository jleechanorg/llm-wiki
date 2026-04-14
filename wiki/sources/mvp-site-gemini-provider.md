---
title: "mvp_site gemini_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/gemini_provider.py
---

## Summary
Gemini provider implementation using response_mime_type="application/json" for JSON format enforcement. Documents SDK limitation where response_schema cannot be used with additionalProperties=true for dynamic game state keys. Isolated from llm_service for clean architecture.

## Key Claims
- Uses response_mime_type="application/json" for JSON enforcement (not response_schema)
- SDK limitation: google-genai Python SDK rejects additionalProperties:true at client level
- BYOK (Bring Your Own Key) client caching: _MAX_BYOK_CLIENTS=100 to prevent memory growth
- _DICE_TOOL_NAMES filters dice tools in code_execution mode (handled via Python random instead)
- Thread-safe Gemini HTTP capture with _GEMINI_HTTP_CAPTURE_LOCK

## Connections
- [[LLMIntegration]] — Gemini API provider
- [[DiceMechanics]] — dice tool filtering in code execution mode
