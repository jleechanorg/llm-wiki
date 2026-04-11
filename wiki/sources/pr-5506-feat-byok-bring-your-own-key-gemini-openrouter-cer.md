---
title: "PR #5506: feat: BYOK (Bring Your Own Key) - Gemini/OpenRouter/Cerebras with navigation-safe settings persistence"
type: source
tags: []
date: 2026-02-15
source_file: raw/prs-worldarchitect-ai/pr-5506.md
sources: []
last_updated: 2026-02-15
---

## Summary
**Surgical BYOK extraction from main branch** - Adds complete Bring Your Own Key (BYOK) support for Gemini, OpenRouter, and Cerebras providers with end-to-end validation, secure storage, and comprehensive testing.

- ✅ **User-supplied API keys**: Settings UI + backend validation + secure Firestore storage with redaction
- ✅ **LLM routing context**: Provider/key/model threaded through `llm_service.py` → `*_provider.py` → API clients
- ✅ **Navigation race fix**: Settings persistence during SPA nav

## Metadata
- **PR**: #5506
- **Merged**: 2026-02-15
- **Author**: jleechan2015
- **Stats**: +6681/-546 in 50 files
- **Labels**: none

## Connections
