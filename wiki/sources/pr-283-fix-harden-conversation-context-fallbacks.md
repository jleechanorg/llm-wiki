---
title: "PR #283: fix: harden conversation context fallbacks"
type: source
tags: [codex]
date: 2025-10-11
source_file: raw/prs-/pr-283.md
sources: []
last_updated: 2025-10-11
---

## Summary
- load entire stored conversation history by default when prompting the single-model chat LLM
- paginate conversation MCP context fetching and expose cursor support through the conversation agent
- build second-opinion prompts from full transcripts and extend regression coverage for the new behavior
- trim configurable system prompts, always include the latest user turn when history retrieval fails, randomize synthetic message IDs, and cap pagination requests to the configured page size

## Metadata
- **PR**: #283
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +18/-10 in 4 files
- **Labels**: codex

## Connections
