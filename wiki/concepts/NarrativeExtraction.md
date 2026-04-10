---
title: "Narrative Extraction"
type: concept
tags: [data-processing, gemini-api, text-extraction, frontend]
sources: ["readme-ai-assistants-critical-system-architecture"]
last_updated: 2026-04-08
---

## Definition
Narrative Extraction is the process of extracting the narrative text from structured JSON responses returned by the Gemini API. The extracted narrative is what users see displayed in the frontend.

## Process
1. Gemini API returns valid JSON with a `narrative` field
2. `llm_service.py` parses the JSON using `parse_structured_response()`
3. The `narrative` field is extracted from the GeminiResponse object
4. `main.py` passes the narrative text to firestore_service.py
5. Frontend displays the narrative with "Scene #X" prefix

## Common Issues
- **JSON Display Bug** — Users see raw JSON instead of extracted narrative
- **Extraction Failure** — Narrative not being extracted correctly in llm_service.py
- **Frontend Display** — Frontend receiving full JSON instead of narrative text

## Related Concepts
- [[JSON Mode]]
- [[Parse Structured Response]]
- [[Data Flow Pipeline]]
