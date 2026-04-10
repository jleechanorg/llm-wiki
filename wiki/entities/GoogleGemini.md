---
title: "Google Gemini"
type: entity
tags: [google, ai, llm, generative]
sources: ["real-service-provider-tests", "real-browser-settings-game-integration-test", "cerebras-qwen-command-matrix-tdd-tests"]
last_updated: 2026-04-08
---

Google's Gemini LLM API. RealServiceProvider uses it via get_gemini() to create actual client instances. Tests verify client creation succeeds or fails gracefully on auth issues.

## Related
- [[RealServiceProvider]] — creates Gemini client
