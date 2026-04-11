---
title: "README for AI Assistants"
type: source
tags: [architecture, json-mode, gemini-api, debugging, worldarchitect]
source_file: "raw/README-AI-Assistants.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Critical system architecture documentation for WorldArchitect.AI explaining the intentional use of JSON mode for all Gemini API responses, the data flow pipeline from API to frontend, and the proper debugging workflow for JSON display issues.

## Key Claims
- **JSON Mode is Intentional** — The system uses JSON mode for ALL Gemini API responses; this is not a bug but a required feature for state management
- **Data Flow Pipeline** — Gemini API → llm_service.py (parses JSON, extracts narrative) → main.py → firestore_service.py → Frontend (displays "Scene #X" prefix)
- **User-Facing Output** — Users should ONLY see narrative text, never raw JSON structure
- **JSON Display Bug Symptom** — Users see raw JSON like `Scene #2: {"narrative": "..."}` instead of formatted text

## Key Technical Details
| Component | Role |
|-----------|------|
| `narrative_response_schema.py` | Defines JSON structure and parsing logic |
| `llm_service.py` | Calls Gemini API and processes responses |
| `main.py` | Orchestrates flow and saves to database |
| `app.js` | Frontend that adds "Scene #" prefix to displayed text |

## Debugging Checklist
1. Is Gemini returning valid JSON? (Check logs)
2. Is parse_structured_response extracting the narrative?
3. Is GeminiResponse.narrative_text containing just narrative or full JSON?
4. Is main.py passing the correct field to firestore?
5. Is the frontend receiving narrative or JSON?


## Connections
- [[JSON Mode]] — Core architectural pattern using structured JSON for all API responses
- [[Narrative Extraction]] — Process of extracting narrative text from structured JSON responses
- [[Parse Structured Response]] — Function that parses valid JSON and extracts narrative field
- [[State Management]] — JSON mode enables state updates through structured response parsing

## Contradictions
- None currently documented
