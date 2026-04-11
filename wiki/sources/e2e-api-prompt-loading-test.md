---
title: "End-to-End API Test for Prompt Loading via /interaction"
type: source
tags: [python, testing, e2e, api, flask, prompt-loading, firestore]
source_file: "raw/test_end2end_prompt_loading_api.py"
sources: []
last_updated: 2026-04-08
---

## Summary
API-level end-to-end test validating prompt loading through the Flask pipeline. Tests the `/api/campaigns/{campaign_id}/interaction` endpoint to ensure selected prompts from campaign configuration are passed to the LLM provider.

## Key Claims
- **API interaction endpoint**: POST to `/api/campaigns/{campaign_id}/interaction` with JSON payload `{"input": "Continue", "mode": "character"}` should return 200 status.
- **Prompt loading from Firestore**: Campaign documents store `selected_prompts` array (e.g., `["narrative"]`) which must be passed to the LLM.
- **Prompt contents propagation**: The `prompt_contents` kwarg passed to the LLM provider must include the selected prompts from campaign config.
- **Narrative prompt validation**: When campaign has `selected_prompts: ["narrative"]`, the LLM request payload should include `"narrative"` in its `selected_prompts` field.
- **Mock service integration**: Test uses FakeFirestoreClient and FakeLLMResponse for controlled testing without external dependencies.

## Key Quotes
> "Expected prompt contents for API interaction." — validates that prompt_contents is populated
> "Narrative prompt should be selected for API interaction." — asserts selected_prompts propagation

## Connections
- [[Flask API Pipeline]] — the Flask application route handling /interaction endpoint
- [[Prompt Loading]] — mechanism for loading selected prompts from campaign config
- [[Firestore Campaign Storage]] — where selected_prompts is stored and retrieved
- [[Gemini Provider]] — LLM provider that receives prompt_contents kwarg

## Contradictions
- None identified — this test documents expected behavior for prompt loading
