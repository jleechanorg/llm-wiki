---
title: "Data Flow Pipeline"
type: concept
tags: [architecture, system-design, data-processing, worldarchitect]
sources: ["readme-ai-assistants-critical-system-architecture"]
last_updated: 2026-04-08
---

## Definition
The Data Flow Pipeline describes the complete path a Gemini API response takes from the API call to what users see displayed in the frontend.

## Pipeline Stages
```
1. Gemini API
   ↓ (returns JSON)
2. llm_service.py
   ↓ (parses JSON, extracts narrative)
3. main.py
   ↓ (receives GeminiResponse object)
4. firestore_service.py
   ↓ (saves narrative text)
5. Frontend (app.js)
   ↓ (adds "Scene #X" prefix)
6. User Display
```

## Key Files at Each Stage
| Stage | File | Role |
|-------|------|------|
| 1 | Gemini API | Returns structured JSON |
| 2 | `llm_service.py` | Parses JSON, extracts narrative |
| 3 | `main.py` | Orchestrates flow |
| 4 | `firestore_service.py` | Saves to database |
| 5 | `app.js` | Adds prefix, displays to user |

## Debugging Across Pipeline
To debug issues, trace through EACH stage of the pipeline:
1. Is Gemini returning valid JSON?
2. Is parse_structured_response extracting narrative?
3. Is main.py passing correct field?
4. Is frontend receiving narrative or JSON?


## Related Concepts
- [[JSON Mode]]
- [[Narrative Extraction]]
- [[Parse Structured Response]]
