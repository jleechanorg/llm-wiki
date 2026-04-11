---
title: "Provider-aware Settings Persistence E2E Tests"
type: source
tags: [python, testing, e2e, settings, persistence, providers]
source_file: "raw/test_provider_settings_persistence_e2e.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test suite validating that the settings API correctly persists and round-trips LLM provider preferences across Gemini, OpenRouter, and Cerebras providers. Tests verify default provider selection, model switching, and state preservation through Firestore.

## Key Claims
- **Default Gemini provider**: Initial settings fetch returns Gemini as default provider with `constants.DEFAULT_GEMINI_MODEL`
- **OpenRouter persistence**: Switching to OpenRouter with `meta-llama/llama-3.1-70b-instruct` model persists correctly
- **Cerebras persistence**: Switching to Cerebras with `llama-3.3-70b` model (updated from 3.1-70b) persists correctly
- **Full round-trip validation**: Settings can be switched between all providers and values are preserved accurately

## Key Test Flow
| Step | Action | Expected |
|------|--------|----------|
| 1 | GET /api/settings | `llm_provider: "gemini"`, `gemini_model: default` |
| 2 | POST OpenRouter settings | 200 OK |
| 3 | GET /api/settings | `llm_provider: "openrouter"`, `openrouter_model: ...` |
| 4 | POST Cerebras settings | 200 OK |
| 5 | GET /api/settings | `llm_provider: "cerebras"`, `cerebras_model: ...` |
| 6 | POST Gemini revert | 200 OK |
| 7 | GET /api/settings | `llm_provider: "gemini"`, `gemini_model: default` |

## Connections
- [[Gemini]] — default provider
- [[OpenRouter]] — alternative LLM provider
- [[Cerebras]] — alternative LLM provider
- [[Firestore]] — persistence layer
- [[SettingsAPI]] — API endpoint under test
