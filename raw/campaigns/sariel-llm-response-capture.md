---
title: "Sariel LLM Response Capture Script"
type: source
tags: [python, testing, llm, flask, worldai]
source_file: "raw/sariel-llm-response-capture.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python script that captures actual LLM responses by running tests in the main project environment where Flask dependencies exist. Uses Flask test client to create campaigns and execute interactions, then saves captured responses to JSON for analysis.

## Key Claims
- **Environment Isolation** — Runs in main project (`mvp_site/`) where Flask dependencies are available
- **Test Client Usage** — Uses Flask test client (`app.test_client()`) for API testing without network calls
- **Campaign Creation** — Creates campaigns via POST to `/api/campaigns` endpoint
- **Interaction Capture** — Captures LLM responses from `/api/campaigns/{id}/interaction` endpoint
- **JSON Output** — Saves captured responses to `sariel_real_responses.json` with metadata

## Key Code Elements
- Test user ID: `'test-llm-capture'`
- Bypass auth header: `'X-Test-Bypass-Auth': 'true'`
- Campaign prompt: `'Start a campaign with Sariel in a throne room'`
- Interaction modes: `'character'`
- Test prompts dir: `temp_prompts_dir` via `IntegrationTestSetup`

## Test Interactions
1. `"continue"` — Throne Room, expects Sariel
2. `"ask for forgiveness. tell cassian i was scared and helpless"` — Throne Room, expects Sariel/Cassian (marks as cassian_problem)
3. `"2"` — Valerius's Study, expects Sariel/Valerius

## Connections
- [[IntegrationTestRunnerRealAPICalls]] — Real API integration testing
- [[SarielTestSuiteConsolidation]] — Related test consolidation work
- [[Flask]] — Web framework used

## Contradictions
- None identified
