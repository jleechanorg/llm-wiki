---
title: "mem0 dim mismatch + Groq LLM fix — qdrant 1536→768, idempotent recovery"
type: source
tags: [mem0, qdrant, groq, hermes, dim-mismatch, red-green, root-cause]
date: 2026-06-22
source_file: raw/project_2026-06-22_mem0_dim_mismatch_and_groq_fix.md
---

## Summary

mem0 had been silently broken for months — the qdrant `hermes_mem0` collection was sized at 1536 dims (leftover from when mem0 used an OpenAI embedder, ~the `openclaw_mem0` era) while the configured embedder was Ollama `nomic-embed-text` @ 768 dims. Every `m.add(...)` returned `400 Bad Request: Vector dimension error: expected dim: 1536, got 768`. The documented Groq LLM fallback was also dead because the `groq` pip package was never installed in either `~/.local/orch-venv` or `~/.hermes/.venv`, even though `GROQ_API_KEY` was exported in shell env. Root-cause fix: recreate collection at 768 dims, install `groq`, switch `MEM0_CONFIG["llm"]` from `ollama` to `groq`, wrap `m.add` with one-shot idempotent dim-recovery that drops + recreates the collection at the embedder's declared `embedding_dims` and retries.

## Key Claims

- **The dim mismatch was the silent blocker**: collection created at 1536 dims predates the Ollama embedder switch; insert fails before any LLM extraction completes, so mem0 looked like it was "always timing out" or "broken in production".
- **mem0 ships a first-class Groq LLM provider** (`mem0.llms.groq.GroqLLM`) — it only needs the `groq` pip package installed. Per the 2026-06-09 memory entry, this was the intended fallback for the historical Ollama `gemma2:2b` flakiness.
- **Idempotent dim-recovery is durable**: any future embedder dim change will self-heal on the next write via `_recreate_collection_at_embedder_dim()` + one-shot `_DIM_RECREATE_DONE` guard.
- **End-to-end smoke now PASSES 5/5**: `groq package` + `qdrant dim == 768` + `mem0 LLM == groq` + `add_memory(infer=True)` + `search_memory()`. `python3 ~/.hermes/scripts/mem0_health_check.py` is the new canary.

## Key Quotes

> "Vector dimension error: expected dim: 1536, got 768" — qdrant error, every mem0 add since the embedder swap (silent)

> "mem0 client currently broken (`groq` import error) — fix before relying on Phase-5 saves" — project_2026-06-09_dark_factory_spec_gen_dispatch.md

## Connections

- [[Mem0PathHermesNotOpenclaw]] — mem0 helpers live at `~/.hermes/...`, not `~/.openclaw/...`
- [[Project2026-06-09DarkFactorySpecGenDispatch]] — earlier memory entry that flagged "mem0 client currently broken (`groq` import error)"
- [[HermesMemorySystem]] — the broader hermes mem0 plugin config
- [[QdrantLocalDocker]] — the qdrant container that holds `hermes_mem0`

**Bead:** rev-jb53t (closed)
