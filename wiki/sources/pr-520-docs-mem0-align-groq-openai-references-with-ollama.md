---
title: "PR #520: docs(mem0): align Groq/OpenAI references with Ollama LLM + OpenAI embeddings"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldai_claw/pr-520.md
sources: []
last_updated: 2026-04-06
---

## Summary
The jleechanclaw harness was previously using Groq for fact extraction in mem0 hooks, which introduced external API dependencies and costs. To improve local-first capabilities and reduce reliance on third-party providers for extraction tasks, we are transitioning to using local OSS LLMs (specifically Ollama with llama3.2:3b) as the default fact-extraction provider.

## Metadata
- **PR**: #520
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +309/-60 in 14 files
- **Labels**: none

## Connections
