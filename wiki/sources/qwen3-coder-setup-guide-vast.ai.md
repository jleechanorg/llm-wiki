---
title: "Qwen3-Coder Setup Guide with Vast.ai"
type: source
tags: [llm, self-hosted, qwen, vast.ai, ollama, gpu, api-proxy]
source_file: "raw/worldarchitect.ai-qwen_setup.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Complete guide for setting up Qwen3-Coder self-hosted LLM infrastructure using vast.ai GPU instances. Provides automated workflows via `claude_start.sh` scripts with zero-config modes for both cloud (vast.ai) and local (Ollama) setups.

## Key Claims

- **Automated Vast.ai**: `--qwen` flag automatically finds/creates GPU instances and sets up SSH tunnels
- **Local Ollama**: `--qwen-local` runs Qwen3-Coder locally via Ollama without cloud dependencies
- **API Compatibility**: API proxy accepts Claude CLI requests and converts between Anthropic Messages and Ollama Chat formats
- **Semantic Caching**: Redis Cloud integration provides 70-90% cache hit rate for coding tasks
- **Performance**: Qwen3-Coder achieves 20-30 tokens/second on RTX 4090

## Key Quotes

> "**New in v2.0**: Fully automated vast.ai workflow — checks existing instances, connects or creates new, downloads model, sets up SSH tunnel automatically"

> "**Model**: qwen3-coder (Qwen3 Code-specific variant), ~30B parameters (3.3B activated) optimized for coding, requires ~19GB GPU VRAM"

## Connections

- [[Qwen3Coder]] — the model being deployed
- [[Vastai]] — GPU rental platform
- [[Ollama]] — local LLM runtime
- [[RedisCloud]] — semantic caching layer
- [[LlmSelfhost]] — self-hosted LLM project

## Contradictions

- None identified in this source
