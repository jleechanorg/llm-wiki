---
title: "PR #5849: Enable OpenRouter streaming in continue_story_streaming"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5849.md
sources: []
last_updated: 2026-03-08
---

## Summary
- enable `openrouter` in `continue_story_streaming` provider allowlist (Gemini/OpenClaw behavior unchanged)
- route phase-1 and phase-2 streaming calls through `openrouter_provider.generate_content_stream_sync`
- add OpenRouter provider-level SSE streaming implementation using OpenAI-compatible stream payload parsing
- add tests for OpenRouter streaming routing and provider allowlist behavior

## Metadata
- **PR**: #5849
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +1266/-58 in 20 files
- **Labels**: none

## Connections
