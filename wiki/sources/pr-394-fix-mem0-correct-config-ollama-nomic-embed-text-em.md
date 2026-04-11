---
title: "PR #394: fix(mem0): correct config — ollama nomic-embed-text embedder + groq LLM (match existing collection)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-394.md
sources: []
last_updated: 2026-03-24
---

## Summary
PR #389 merged the mem0 hooks but with wrong config values — `text-embedding-3-small` (1536 dims, OpenAI) and `gpt-4o-mini`. The actual `openclaw_mem0` Qdrant collection was built with `nomic-embed-text` (768 dims, Ollama) and the stack uses Groq for LLM inference.

## Metadata
- **PR**: #394
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +11/-10 in 3 files
- **Labels**: none

## Connections
