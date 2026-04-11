---
title: "PR #174: feat(mem0): switch embedder to local Ollama (nomic-embed-text, 768 dims)"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-174.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Replace OpenAI embedding API calls with local Ollama `nomic-embed-text`
- 5 TDD tests (red → green): provider dispatch, regression, live dims, raw client, config round-trip
- Qdrant collection recreated at 768 dims

## Metadata
- **PR**: #174
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +692/-39 in 4 files
- **Labels**: none

## Connections
