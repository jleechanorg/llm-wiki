---
title: "Main.py Structured Response Building Tests"
type: source
tags: [python, testing, api, structured-response, flask]
source_file: "raw/test_main_structured_response_building.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for main.py structured response building. Tests validate that the /api/campaigns/{id}/interaction endpoint returns the correct structure with all required fields from the LLMResponse object.

## Key Claims
- **Response includes all required fields**: state_updates, entities_mentioned, location_confirmed, debug_info are all included in API responses
- **Graceful handling of missing fields**: Responses remain valid when optional structured_response fields are missing
- **Debug info conditional on debug mode**: debug_info is only included when debug_mode is True

## Key Quotes
> "Add structured response fields as main.py does"

## Connections
- [[LLMResponse]] — structured response object containing narrative, entities, state updates
- [[APIInteractionEndpoint]] — /api/campaigns/{id}/interaction endpoint in main.py
- [[DebugMode]] — conditional debug info display based on debug_mode flag

## Contradictions
- None detected
