---
title: "Core Application Code Breakdown"
type: source
tags: [worldarchitect, code-metrics, architecture, production-lines, codebase]
sources: []
date: 2025-10-02
source_file: /Users/jleechan/repos/worldarchitect/loc_simple.sh
last_updated: 2026-04-07
---

## Summary
The WorldArchitect core application comprises **29,994 production lines** of code across Python, JavaScript, and HTML. The breakdown spans 9 major runtime areas: API gateway/MCP bridge (3,084 LOC), gameplay orchestration (2,089 LOC), AI generation pipeline (3,904 LOC), entity/narrative validation (3,772 LOC), persistence/memory services (2,938 LOC), diagnostics/developer tooling (1,949 LOC), mocks/harnesses (1,557 LOC), testing framework (3,049 LOC), and front-end presentation (7,652 LOC).

## Key Claims

- **29,994 production LOC** — measured by `loc_simple.sh` counting Python, JavaScript, and HTML files in `mvp_site/`
- **API Gateway & MCP Bridge (3,084 LOC)** — Flask REST endpoints forwarding to MCP tool server, includes `main.py`, `mcp_api.py`, `mcp_client.py`, `start_flask.py`, `main_parallel_dual_pass.py`, `unified_api_examples.py`, `inspect_sdk.py`
- **Gameplay Orchestration (2,089 LOC)** — Central mission flow loading player state, preparing prompts, rendering exports/pitches; modules: `world_logic.py`, `document_generator.py`, `prompt_utils.py`, `dual_pass_generator.py`, `world_loader.py`
- **AI Generation Pipeline (3,904 LOC)** — Gemini request orchestration, retries, JSON parsing, token budgeting for story beats; modules: `llm_service.py`, `gemini_request.py`, `gemini_response.py`, `robust_json_parser.py`, `token_utils.py`
- **Entity & Narrative Validation (3,772 LOC)** — Campaign state guards validating characters, stats, narrative events; modules: `entity_validator.py`, `entity_preloader.py`, `entity_instructions.py`, `entity_tracking.py`, `entity_utils.py`, `narrative_response_schema.py`, `narrative_sync_validator.py`
- **Persistence & Memory Services (2,938 LOC)** — Firestore access, numeric hygiene enforcement, MCP memory store sync; modules: `firestore_service.py`, `game_state.py`, `numeric_field_converter.py`, `file_cache.py`, `json_utils.py`, `memory_integration.py`
- **Diagnostics & Developer Tooling (1,949 LOC)** — Capture scripts, logging helpers, debug parsers exercising Gemini/MCP flows; modules: `analysis/`, `debug_hybrid_system.py`, `debug_json_response.py`, `debug_mode_parser.py`
- **Mocks & Capture Harnesses (1,557 LOC)** — Drop-in Firestore and Gemini fakes plus fixture packs for local capture sessions
- **Testing Framework & Capture CLI (3,049 LOC)** — Python harnesses driving MCP capture sessions, validating example migrations, reusable factories; modules: `testing_framework/`, `testing_ui/`
- **Front-end Presentation (7,652 LOC)** — Legacy JS client, shared HTML templates, Tailwind configuration, static fallbacks shipped with Flask server; covers `frontend_v1/`, `frontend_v2/`, `templates/`, `static/`
- **TypeScript Gap** — React application under `mvp_site/frontend_v2/src/` adds ~16K lines not counted by `loc_simple.sh`, making total shipped client code ~27.6K LOC
- **Thin HTTP Layer** — Architecture emphasizes minimal HTTP handling with heavy logic in downstream services

## Key Quotes
> "loc_simple.sh only counts .py, .js, and .html files"

> "The React application under mvp_site/frontend_v2/src/ is TypeScript-first, contributing another ~16K lines that are not part of the Core Application bucket"

## Connections
- [[Claude Code Integration Design]] — related to MCP bridge architecture
- [[Milestone 2: Firebase Authentication Configuration Fix]] — relates to Firestore service layer
- [[OpenClaw Gateway Integration Design + Implementation Plan]] — related to API gateway patterns
- [[Context Optimization Plan for /converge System]] — architectural context for system design

## Contradictions
- None detected with existing wiki content