---
title: "PR #2194: Add GLM-4.6 200k context (OpenRouter/Cerebras), tighten Gemini compaction, align smoke runner"
type: source
tags: [codex]
date: 2025-12-01
source_file: raw/prs-worldarchitect-ai/pr-2194.md
sources: []
last_updated: 2025-12-01
---

## Summary
- add GLM 4.6 to OpenRouter (zai-org/glm-4.6) and Cerebras (zai-glm-4.6) with 200k token context windows
- expose GLM 4.6 in settings UI for both providers
- clamp Gemini compaction budget to 300k; other providers stay at 0.9× window (Llama/Qwen ~118k, GLM 4.6 ~180k)
- add scripts/run_smoke_local.sh wrapper to mirror the /smoke CI workflow (defaults to MCP_TEST_MODE=real)
- refreshed WorldAI auth token and re-ran full REAL MCP smoke suite against preview; all providers passed end-to-end

## Metadata
- **PR**: #2194
- **Merged**: 2025-12-01
- **Author**: jleechan2015
- **Stats**: +2465/-468 in 38 files
- **Labels**: codex

## Connections
