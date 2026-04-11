---
title: "PR #517: feat: mem0 embedding fix, minimax config tests, docs, AO progress"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldai_claw/pr-517.md
sources: []
last_updated: 2026-04-06
---

## Summary
Bundles harness improvements that were pending on `main` working tree (targeted `git add` only — no workspace screenshots).

### Included
- **mem0**: `scripts/mem0_shared_client.py` — pass OpenAI `dimensions` for 768-d Qdrant collections; `check_compatibility=false` for qdrant-client. Unit tests in `src/tests/test_mem0_shared_client.py`.
- **openclaw-mem0 plugin**: postinstall patch for upstream mem0ai OpenAI embedder (`dimensions: this.embeddingDims`); vitest for patch idempotency; `npm run pos

## Metadata
- **PR**: #517
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +418/-28 in 10 files
- **Labels**: none

## Connections
