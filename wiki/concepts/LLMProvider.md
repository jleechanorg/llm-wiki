---
title: "LLM Provider"
type: concept
tags: [llm, provider, api, configuration]
sources: ["shared-constants-configuration"]
last_updated: 2026-04-08
---

Configuration system for selecting and managing LLM backends. Supports multiple providers with standardized interfaces: Gemini (default), OpenRouter, Cerebras, and OpenClaw.

## Provider Details
- **Gemini**: Default, uses gemini-3-flash-preview model
- **OpenRouter**: Gateway to many models
- **Cerebras**: High-performance inference
- **OpenClaw**: Local model support via gateway on port 18789

## Related
- [[Shared Constants Configuration]] — defines provider constants
- [[Gemini]] — default provider
- [[OpenClaw]] — local model option
