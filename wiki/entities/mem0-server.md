---
title: "mem0-server"
type: entity
tags: [project, python, fastapi, hermes-prod, memory, ollama, qdrant]
date: 2026-06-26
local_path: ~/.hermes_prod/mem0_server.py
---

# mem0-server

**Definition**: A FastAPI-based memory service that wraps the `mem0ai` Python package to provide long-term memory storage for AI agents. Uses Ollama for embedding (local) and Qdrant (port 6333) for vector storage. Lives in the Hermes Prod environment (`~/.hermes_prod/`).

## Identity

- **Source**: `~/.hermes_prod/mem0_server.py`
- **Config**: `~/.hermes_prod/mem0.json`
- **Service**: Hermes Prod memory layer (used by Claude, Codex, and other agents via the mem0 MCP server)
- **Embedding**: Ollama local embedder (no OpenAI API key required)
- **LLM extraction**: Groq (via `GROQ_API_KEY` env var)
- **Vector store**: Qdrant at `http://localhost:6333`

## Port history

- **Originally**: port 8000 (hardcoded at `mem0_server.py:236`)
- **Currently**: port 8100 (moved 2026-06-26 to free 8000 for [[ccproxy_api]])

The hardcoded port caused a conflict with ccproxy-api (both wanted 8000). Resolution: change `uvicorn.run(app, host="0.0.0.0", port=8000)` to `port=8100` AND update `mem0.json` `host: "http://localhost:8000"` → `"http://localhost:8100"`.

## Endpoints

- `GET /health` — `{"status": "ok"}` (the mem0 service discriminator)
- `POST /memory/add` — append a memory
- `POST /memory/search` — query memories by semantic similarity

## Service discriminator

`GET http://127.0.0.1:8100/health` returns `{"status": "ok"}`. Used as a fallback discriminator when port 8000 is occupied by ccproxy-api.

## Relationship to other services

| Service | Port | Role |
|---|---|---|
| mem0-server | 8100 | Long-term memory storage |
| ccproxy-api | 8000 | OAuth-injecting LLM proxy |
| llm-inspector | 9000 | HTTP capture proxy |

All three must be running for the full Claude Code capture chain with memory-backed agent behavior.

## Related entities

- [[ccproxy_api]] — formerly conflicted on port 8000
- [[llm_inspector]] — captures traffic from mem0-using agents

## Related concepts

- [[ServiceDiscrimination]] — port 8000 ambiguity resolution (mem0 vs ccproxy)
- [[MacOSKeychainOAuthStorage]] — not directly related, but same class of "service can't start because dependency missing" issue