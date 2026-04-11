---
title: "PR #2296: Remove LLM fallback retries and surface context errors"
type: source
tags: [codex]
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2296.md
sources: []
last_updated: 2025-12-03
---

## Summary
- remove model and context fallback chains and convert LLM calls to single-shot attempts
- raise explicit LLMRequestError instances for context overflow and provider overload cases and surface them through world_logic responses
- add coverage ensuring context-too-large and overload errors are surfaced without retries

## Metadata
- **PR**: #2296
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +279/-276 in 11 files
- **Labels**: codex

## Connections
