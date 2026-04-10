---
title: "Model Preference Selection"
type: concept
tags: [llm, gemini, user-settings, model-routing]
sources: []
last_updated: 2026-04-08
---

## Definition
System allowing users to specify their preferred LLM model (e.g., Gemini 2.0 Flash) that is then used for all story generation calls. Implemented via `GEMINI_MODEL_MAPPING` and `_select_provider_and_model()`.

## Key Components
- **user_id parameter**: Passed through to enable per-user model lookup
- **_select_provider_and_model()**: Determines provider and model based on user settings
- **GEMINI_MODEL_MAPPING**: Lookup table from user-facing model names to API model identifiers
- **Test mode guard**: In test mode, returns default model — tests must patch to simulate preferences

## Related Concepts
- [[StructuredResponse]]
- [[LLM-FirstStateManagement]]
