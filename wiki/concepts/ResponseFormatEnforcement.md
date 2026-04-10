---
title: "Response Format Enforcement"
type: concept
tags: [prompt-engineering, json-validation, structured-output]
sources: ["llm-api-call-capture-gemini-logging"]
last_updated: 2026-04-08
---

## Description
Prompt technique requiring the LLM to output valid JSON with a specific schema. The prompt explicitly states the required structure and validates that all required fields are present in the response.

## Schema Enforced
```json
{
  "narrative": "Your narrative text here...",
  "entities_mentioned": ["Sariel"],
  "location_confirmed": "The current location name"
}
```

## Validation Points
- narrative: the actual story text
- entities_mentioned: list of all entities referenced
- location_confirmed: must match manifest

## Connections
- [[NarrativeResponseSchema]] — the schema being enforced
- [[EntityManifest]] — validates entities_mentioned against
- [[LLMProviderColdStartOptimization]] — can affect latency

## Source Evidence
"RESPONSE FORMAT REQUIREMENT: You must format your response as valid JSON with exactly this structure"
